import psutil
import time
import json
import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- 1. Monitor de Archivos (Sin cambios) ---
class FileMonitor(FileSystemEventHandler):
    def __init__(self):
        self.activity_log = []

    def on_created(self, event):
        if not event.is_directory:
            self.activity_log.append({
                "action": "created",
                "path": event.src_path,
                "timestamp": time.time()
            })

    def on_modified(self, event):
        if not event.is_directory:
            self.activity_log.append({
                "action": "modified",
                "path": event.src_path,
                "timestamp": time.time()
            })

# --- 2. Motor de Análisis Mejorado ---
def run_analysis(target_path, duration=10):
    report = {
        "target": target_path,
        "network_activity": [],
        "file_activity": [],
        "process_tree": []
    }

    file_handler = FileMonitor()
    observer = Observer()
    observer.schedule(file_handler, path=".", recursive=False)
    observer.start()

    print(f"[*] Iniciando análisis V2 de: {target_path}")
    
    try:
        proc = psutil.Popen(["python", target_path])
        start_time = time.time()
        
        # Lista de PIDs que ya hemos registrado para no duplicar
        seen_pids = set()

        while (time.time() - start_time) < duration:
            if not proc.is_running():
                break

            # A. Obtener lista de procesos a vigilar (Padre + Hijos)
            try:
                children = proc.children(recursive=True)
                all_procs = [proc] + children
            except psutil.NoSuchProcess:
                break

            for p in all_procs:
                # 1. Registrar Procesos Nuevos en el Árbol
                if p.pid not in seen_pids:
                    try:
                        p_info = {
                            "pid": p.pid,
                            "name": p.name(),
                            "parent": p.ppid(),
                            "cmdline": " ".join(p.cmdline())
                        }
                        report["process_tree"].append(p_info)
                        seen_pids.add(p.pid)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass

                # 2. Monitoreo de Red (CORREGIDO y aplicado a hijos también)
                try:
                    # Usamos net_connections() para arreglar el warning
                    connections = p.net_connections(kind='inet')
                    for conn in connections:
                        conn_data = {
                            "process": p.name(), # Saber QUIÉN hizo la conexión
                            "pid": p.pid,
                            "laddr": f"{conn.laddr.ip}:{conn.laddr.port}",
                            "raddr": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "0.0.0.0:0",
                            "status": conn.status
                        }
                        
                        # Evitar duplicados exactos en el reporte
                        is_duplicate = False
                        for entry in report["network_activity"]:
                            if (entry["pid"] == conn_data["pid"] and 
                                entry["raddr"] == conn_data["raddr"] and
                                entry["status"] == conn_data["status"]):
                                is_duplicate = True
                                break
                        
                        if not is_duplicate:
                            report["network_activity"].append(conn_data)

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # B. Polling más rápido (0.05s) para atrapar conexiones fugaces
            time.sleep(0.05)

    except Exception as e:
        print(f"[!] Error crítico: {e}")

    finally:
        print("[*] Deteniendo monitores...")
        observer.stop()
        observer.join()
        
        # Kill switch recursivo (matar padre e hijos)
        if proc.is_running():
            for child in proc.children(recursive=True):
                try: child.kill() 
                except: pass
            proc.kill()
        
        report["file_activity"] = file_handler.activity_log

    return report

if __name__ == "__main__":
    target = "sample.py"
    if not os.path.exists(target):
        sys.exit(1)
    
    final_report = run_analysis(target, duration=10)
    print("\n" + "="*40)
    print(json.dumps(final_report, indent=4))
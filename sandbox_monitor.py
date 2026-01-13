import psutil
import time
import json
import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- 1. Monitor de Archivos ---
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

# --- 2. Motor de Análisis ---
def run_analysis(target_path, duration=10):
    report = {
        "target": target_path,
        "network_activity": [],
        "file_activity": [],
        "process_tree": []
    }

    # Iniciar monitor de archivos
    file_handler = FileMonitor()
    observer = Observer()
    observer.schedule(file_handler, path=".", recursive=False)
    observer.start()

    print(f"[*] Iniciando análisis V2 de: {target_path}")
    
    proc = None
    try:
        # Ejecutar el malware (sample.py)
        proc = psutil.Popen(["python", target_path])
        start_time = time.time()
        seen_pids = set()

        # Bucle de monitoreo (Dura 'duration' segundos)
        while (time.time() - start_time) < duration:
            if not proc.is_running():
                break

            # Capturar árbol de procesos
            try:
                children = proc.children(recursive=True)
                all_procs = [proc] + children
            except psutil.NoSuchProcess:
                break

            for p in all_procs:
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

                # Capturar Red
                try:
                    connections = p.net_connections(kind='inet')
                    for conn in connections:
                        conn_data = {
                            "process": p.name(),
                            "pid": p.pid,
                            "laddr": f"{conn.laddr.ip}:{conn.laddr.port}",
                            "raddr": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "0.0.0.0:0",
                            "status": conn.status
                        }
                        
                        # Evitar duplicados exactos
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
            
            # Pequeña pausa para no saturar CPU
            time.sleep(0.1)

    except Exception as e:
        print(f"[!] Error crítico en ejecución: {e}")

    finally:
        print("[*] Finalizando monitoreo...")
        observer.stop()
        observer.join()
        
        # Matar procesos si siguen vivos
        if proc and proc.is_running():
            try:
                proc.kill()
                for child in proc.children(recursive=True):
                    try: child.kill() 
                    except: pass
            except: pass
        
        report["file_activity"] = file_handler.activity_log

    return report

# --- 3. PUNTO DE ENTRADA (ESTO ES LO QUE FALTABA) ---
if __name__ == "__main__":
    # El archivo siempre se llamará 'sample.py' porque controller.py lo inyecta con ese nombre
    TARGET = "sample.py"
    
    # Esperamos un momento a que el archivo exista (seguridad)
    if not os.path.exists(TARGET):
        print(f"Error: No encuentro {TARGET}")
        sys.exit(1)

    # Corremos el análisis
    results = run_analysis(TARGET, duration=60)
    
    # IMPORTANTE: Imprimimos el JSON en una sola línea para que controller.py lo lea
    print(json.dumps(results))
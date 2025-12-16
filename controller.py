import docker
import json
import os
import tarfile
import io
import hashlib
import re

# Configuración
IMAGE_NAME = "malware-sandbox:latest"
SAMPLE_FILENAME = "sample.py"
MONITOR_FILENAME = "sandbox_monitor.py"

# --- MÓDULO 1: ANÁLISIS ESTÁTICO ---
def get_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def extract_strings(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
    regex = rb"[ -~]{4,}"
    matches = re.findall(regex, content)
    strings = [m.decode("utf-8", errors="ignore") for m in matches]
    return strings[:20]

def perform_static_analysis(file_path):
    print(f"[*] Realizando análisis estático...")
    return {
        "static_analysis": {
            "filename": os.path.basename(file_path),
            "filesize_bytes": os.path.getsize(file_path),
            "sha256": get_sha256(file_path),
            "interesting_strings": extract_strings(file_path)
        }
    }

# --- MÓDULO 2: ANÁLISIS DINÁMICO (DOCKER) ---
def get_docker_client():
    client = docker.from_env()
    try:
        # Intentamos obtener la imagen directamente
        client.images.get(IMAGE_NAME)
        print(f"[*] Imagen '{IMAGE_NAME}' encontrada. Saltando construcción.")
    except docker.errors.ImageNotFound:
        # Solo construimos si NO existe
        print(f"[*] Imagen no encontrada. Construyendo {IMAGE_NAME}...")
        client.images.build(path=".", tag=IMAGE_NAME, rm=True)
    return client

def analyze_dynamic(client, sample_path):
    print(f"[*] Iniciando Sandbox...")
    
    container = client.containers.create(
        IMAGE_NAME,
        command=f"python {MONITOR_FILENAME}", 
        tty=True,
        network_disabled=False
    )

    try:
        # Inyectar Sample
        with open(sample_path, 'rb') as f:
            data = f.read()
        tar_stream = io.BytesIO()
        with tarfile.open(fileobj=tar_stream, mode='w') as tar:
            tar_info = tarfile.TarInfo(name=SAMPLE_FILENAME)
            tar_info.size = len(data)
            tar.addfile(tar_info, io.BytesIO(data))
        tar_stream.seek(0)
        container.put_archive('/app/', tar_stream)

        # Arrancar
        container.start()
        
        # Esperar máximo 15 segundos (Si el malware tarda más, lo cortamos)
        result = container.wait(timeout=15)
        
        # Leer Logs
        logs = container.logs().decode('utf-8')
        
        # --- AGREGA ESTO PARA VER EL ERROR EN TU CONSOLA ---
        print("\n" + "="*20 + " LOGS DEL CONTENEDOR " + "="*20)
        print(logs)
        print("="*60 + "\n")
        # ---------------------------------------------------
        
        json_start = logs.find('{')
        json_end = logs.rfind('}') + 1
        
        if json_start == -1: 
            return {"error": "No JSON output", "logs": logs}
            
        return json.loads(logs[json_start:json_end])

    except Exception as e:
        return {"error": str(e)}
    finally:
        try:
            container.remove(force=True)
        except:
            pass

# --- ORQUESTADOR ---
if __name__ == "__main__":
    pass
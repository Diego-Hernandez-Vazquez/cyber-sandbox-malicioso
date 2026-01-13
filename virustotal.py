import requests
import os

# Carga la API Key de una variable de entorno para mayor seguridad
API_KEY = "YOUR_API_KEY_HERE"  # Reemplaza con tu clave real

BASE_URL = "https://www.virustotal.com/api/v3/files"

def get_reputation(file_hash):
    if API_KEY == "YOUR_API_KEY_HERE":
        print("[VT] ADVERTENCIA: La API Key de VirusTotal no está configurada.")
        return {"found": False, "error": "API Key no configurada."}
        
    print(f"[VT] Consultando inteligencia global para: {file_hash}...")
    
    headers = {
        "x-apikey": API_KEY
    }
    
    try:
        response = requests.get(f"{BASE_URL}/{file_hash}", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            attributes = data['data']['attributes']
            
            stats = attributes['last_analysis_stats']
            malicious = stats['malicious']
            total = sum(stats.values())
            
            return {
                "found": True,
                "malicious_count": malicious,
                "total_engines": total,
                "permalink": data['data']['links']['self'],
                "scan_date": attributes.get('last_analysis_date', 'Desconocido')
            }
            
        elif response.status_code == 404:
            print("[VT] Archivo no encontrado en la base de datos global.")
            return {"found": False, "error": "Hash desconocido (Archivo nuevo/Zero-day)"}
            
        elif response.status_code == 429:
            print("[VT] Límite de cuota excedido.")
            return {"found": False, "error": "Cuota API excedida (4 peticiones/min)"}
            
        else:
            return {"found": False, "error": f"Error HTTP {response.status_code}"}
            
    except Exception as e:
        print(f"[VT ERROR] {str(e)}")
        return {"found": False, "error": "Error de conexión"}
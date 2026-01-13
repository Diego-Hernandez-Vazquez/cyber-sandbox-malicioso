import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def analyze_report(report_json):
    print(f"[IA] Consultando al contenedor Ollama ({MODEL})...")
    
    # Prompt diseñado para Ciberseguridad
    # Prompt diseñado para Ciberseguridad + Inteligencia de Amenazas
    prompt = f"""
    Actúa como un Analista de Malware Senior de un SOC.
    Tienes dos fuentes de verdad:
    1. REPUTACIÓN GLOBAL (VirusTotal): Qué dicen los motores antivirus del mundo.
    2. COMPORTAMIENTO LOCAL (Sandbox): Qué hizo el archivo realmente al ejecutarse.

    REPORTE TÉCNICO (JSON):
    {json.dumps(report_json, indent=2)}

    INSTRUCCIONES DE RESPUESTA (Formato Markdown):
    
    1. 🛡️ **Veredicto Unificado**:
       - ¿Es malicioso? (SÍ/NO/SOSPECHOSO)
       - Explica la relación: "VirusTotal lo detecta como X y el Sandbox confirmó Y..." o "VirusTotal no lo conoce pero el Sandbox detectó..."
    
    2. 🌍 **Análisis de Inteligencia**:
       - Menciona si es una amenaza conocida (basado en el score de VirusTotal) o una posible amenaza nueva (Zero-Day).
    
    3. 🔍 **Evidencia Técnica**:
       - Lista las acciones clave (IPs contactadas, archivos creados).

    4. 💡 **Recomendación**:
       - Acción inmediata para el usuario.

    IMPORTANTE: Responde SIEMPRE en Español. Sé directo y profesional.
    """

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=600)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Error: La IA devolvió una respuesta vacía.")
        else:
            return f"⚠️ Error HTTP {response.status_code}: El contenedor Ollama respondió con error."
            
    except requests.exceptions.ConnectionError:
        return """
        ⚠️ ERROR DE CONEXIÓN CON DOCKER
        No pude conectar a http://localhost:11434.
        Verifica:
        1. ¿Tu contenedor de Ollama está corriendo?
        2. ¿Tiene el puerto 11434 expuesto? (docker ps)
        """
    except Exception as e:
        return f"Error inesperado en módulo IA: {str(e)}"
def chat_with_analyst(question, report_context):
    print(f"[IA CHAT] Pregunta recibida: {question}")
    
    # Prompt dinámico: Le damos el reporte y la pregunta específica
    prompt = f"""
    Actúa como un Experto en Ciberseguridad (SOC Analyst).
    Tienes acceso al siguiente reporte técnico de un malware analizado en tu Sandbox:
    
    REPORTE TÉCNICO:
    {json.dumps(report_context, indent=2)}
    
    PREGUNTA DEL USUARIO:
    "{question}"
    
    INSTRUCCIONES:
    1. Responde basándote ÚNICAMENTE en la evidencia del reporte.
    2. Si la pregunta no tiene sentido con el reporte, dilo amablemente.
    3. Sé breve, técnico pero claro.
    4. Responde siempre en Español.
    """

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.5 # Un poco más creativo para conversar
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=600)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "La IA no respondió nada.")
        else:
            return f"Error HTTP {response.status_code}"
    except Exception as e:
        return f"Error en chat: {str(e)}"
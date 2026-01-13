# 🛡️ Cyber-Sentinel: AI-Powered Malware Sandbox

![Project Status](https://img.shields.io/badge/Status-MVP_Complete-success)
![Python](https://img.shields.io/badge/Backend-FastAPI-blue?logo=fastapi)
![React](https://img.shields.io/badge/Frontend-React_Vite-61DAFB?logo=react)
![Docker](https://img.shields.io/badge/Isolation-Docker-2496ED?logo=docker)
![AI](https://img.shields.io/badge/Intelligence-Ollama_Llama3-orange)

> **Plataforma de análisis forense automatizado que integra detonación segura en contenedores aislados, inteligencia de amenazas global (VirusTotal) e inteligencia artificial generativa local (On-Premise) para la interpretación de incidentes en tiempo real.**

---

## 📸 Demo Dashboard

![Dashboard Overview Ransomware Detection](screenshots/hero-shot-detected.png)
*(Vista principal mostrando un análisis crítico: La IA correlaciona el comportamiento de Ransomware local con la inteligencia global de VirusTotal)*

---

## 🚀 Propuesta de Valor

En el panorama actual de ciberseguridad, la **fatiga de alertas** es un problema crítico. Los analistas de SOC Nivel 1 reciben miles de logs técnicos que requieren demasiado tiempo para interpretar manualmente.

Este proyecto soluciona ese problema mediante una tríada de análisis:

1.  **Automatización y Aislamiento:** Ejecución segura de malware (Scripts Python en esta versión) en entornos Docker efímeros que se destruyen tras el análisis, garantizando cero persistencia.
2.  **Inteligencia Híbrida:** Combina la reputación global de una muestra (**VirusTotal API**) con su comportamiento real en el sandbox.
3.  **Privacidad y Soberanía de Datos:** Uso de LLMs locales (**Llama3 vía Ollama**) para interpretar los logs. La información sensible del análisis *nunca* sale de la infraestructura propia hacia APIs de terceros como OpenAI.

---

## 🏗️ Arquitectura del Sistema

El sistema sigue una arquitectura de microservicios desacoplada para garantizar escalabilidad y seguridad.

```mermaid
graph TD
    User[Usuario Frontend] -->|Subir Archivo & Chat| API[Backend: FastAPI]
    
    subgraph "Motor de Análisis (Backend)"
    API -->|1. Análisis Estático| FS[Sistema de Archivos / Hash calc]
    API -->|2. Reputación Global| VT[API VirusTotal]
    API -->|3. Detonación Dinámica| Docker[Docker Engine (Sandbox)]
    end
    
    subgraph "Capa de Inteligencia (AI)"
    Docker -->|Logs Crudos (Red/Archivos/Procesos)| API
    API -->|Contexto Completo (Logs + VT)| Ollama[Ollama: Llama3 Local]
    Ollama -->|Reporte Ejecutivo & Respuestas Chat| API
    end

    API -->|Resultados Unificados| User

    style Docker fill:#ff9900,stroke:#333,stroke-width:2px,color:white
    style Ollama fill:#00e1ff,stroke:#333,stroke-width:2px,color:black
Tecnologías Clave:
Core Engine: Python 3.10 + FastAPI (Procesamiento asíncrono).

Sandbox: Contenedores Docker (Aislados por red, efímeros).

Threat Intel: Integración con API de VirusTotal para scoring de reputación.

AI Module: Ollama corriendo Llama3 (8B Instruct) localmente para análisis semántico y correlación de logs.

Frontend: React + Vite con diseño UI Cyberpunk/Terminal (CSS personalizado).

Forensics: Librerías psutil, watchdog y análisis de hash SHA256.

✨ Características Principales
1. Análisis Estático, Dinámico y Global
Estático: Extracción inmediata de metadatos, cálculo de Hash (SHA256) y extracción de "Interesting Strings" ofuscados.

Global (VirusTotal): Consulta automática de la reputación del hash en 70+ motores antivirus, presentado en un widget táctico visual.

Dinámico (Sandbox): Detonación controlada monitoreando en tiempo real:

Tráfico de Red: Conexiones a IPs/Dominios sospechosos (C2).

Sistema de Archivos: Detección de patrones Ransomware (creación de notas de rescate, modificación masiva).

Árbol de Procesos: Visualización de comandos ejecutados y procesos hijos.

2. SOC Analyst Virtual (IA Generativa)
Motor de Correlación: La IA no solo resume; cruza los datos de VirusTotal con el comportamiento del Sandbox para identificar falsos positivos o potenciales amenazas Zero-Day.

Reportes Ejecutivos: Genera un resumen claro en lenguaje natural clasificando el riesgo (Bajo/Medio/Crítico).

Chat Táctico Interactivo: Interfaz de chat integrada donde el analista humano puede preguntar estrategias de mitigación específicas basadas en el contexto exacto del malware analizado.

🛠️ Instalación y Despliegue Local
Prerrequisitos
Docker Desktop instalado y corriendo (con soporte para Linux containers).

Python 3.9+

Node.js & npm.

Ollama instalado y el modelo Llama3 descargado (ollama pull llama3).

Una API Key gratuita de VirusTotal.

1. Clonar el Repositorio
Bash

git clone [https://github.com/TU_USUARIO/cyber-sandbox.git](https://github.com/TU_USUARIO/cyber-sandbox.git)
cd cyber-sandbox
2. Backend Setup
Bash

# 1. Crear entorno virtual (Recomendado)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API Key de VirusTotal
# Abre virustotal.py y coloca tu API KEY en la variable correspondiente.

# 4. Iniciar el Servidor
python api_server.py
3. Frontend Setup
Bash

cd sandbox-frontend
npm install
npm run dev
4. Verificar IA
Asegúrate de que Ollama esté corriendo en el puerto 11434 y tenga el modelo cargado.

Bash

ollama serve
# En otra terminal, verifica que responda (opcional "calentamiento"):
ollama run llama3 "Hola system check"
🧪 Ejemplo de Uso
Abrir el dashboard en http://localhost:5173.

Subir un archivo sospechoso (ej. el script de prueba test_virus.py incluido).

Observar la animación de terminal mientras Docker detona el archivo.

Revisar el Hero Grid: El reporte de la IA a la izquierda correlacionado con el puntaje de VirusTotal a la derecha.

Utilizar el chat inferior para preguntar: "¿Qué IPs debo bloquear en el Firewall según este análisis?".

🔮 Roadmap / Futuras Mejoras
[x] Integración con base de datos de firmas (VirusTotal API) - ¡Completado!

[x] Chat interactivo con contexto del reporte - ¡Completado!

[ ] Soporte para análisis de binarios Windows (.exe) usando Wine en contenedores Docker.

[ ] Base de datos local (SQLite/PostgreSQL) para histórico de análisis.

[ ] Exportación de reportes finales en PDF.

👨‍💻 Autor
Diego Hernández Vázquez Estudiante de Ingeniería en Sistemas Computacionales | Especialidad en Ciberseguridad Desarrollador Full Stack & Cloud Enthusiast
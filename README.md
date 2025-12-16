# 🛡️ Cyber-Sandbox

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![React](https://img.shields.io/badge/React-Vite-61DAFB)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)

## Descripción
**Cyber-Sandbox** es una plataforma de análisis de malware híbrida (Estático + Dinámico). Permite a los investigadores de seguridad detonar archivos sospechosos en un entorno aislado (Docker) y visualizar su comportamiento en tiempo real a través de un dashboard moderno.

Este proyecto fue diseñado para automatizar la detección de **IOCs** (Indicadores de Compromiso) como conexiones de red sospechosas y persistencia en el sistema de archivos.

## Características Principales
* **Análisis Estático:** Cálculo de Hash (SHA256) y extracción de cadenas de texto (Strings) sospechosas antes de la ejecución.
* **Sandbox Aislado:** Uso de contenedores Docker efímeros que se destruyen tras cada análisis para evitar contaminación.
* **Análisis Dinámico:** Monitoreo en tiempo real de:
    * Tráfico de Red (Conexiones C2).
    * Sistema de Archivos (Creación/Modificación de archivos).
    * Árbol de Procesos.
* **Interfaz Cyberpunk:** Dashboard desarrollado en React con Vite para visualizar los reportes forenses.

## Tecnologías (Tech Stack)
* **Backend:** Python, FastAPI, Docker SDK.
* **Frontend:** React, Vite, CSS3 (Custom Cyberpunk UI).
* **Motor de Análisis:** Psutil, Watchdog.
* **Infraestructura:** Docker Desktop.

## Requisitos Previos
* Python 3.10 o superior.
* Node.js y npm.
* Docker Desktop (Instalado y Corriendo).
* Habilitar virtualización en BIOS/Windows.

## Instalación y Uso

### 1. Clonar el repositorio
git clone [https://github.com/Diego-Hernandez-Vazquez/cyber-sandbox.git]
cd cyber-sandbox

### 2. Configurar el Backend

# Instalar dependencias
pip install fastapi uvicorn docker psutil watchdog python-multipart

# Iniciar el servidor API
python api.py

### 3. Configurar el Frontend
cd sandbox-frontend
npm install
npm run dev

### 4. Analizar un archivo

- Abre el navegador en http://localhost:5173.
- Sube un archivo de prueba.
- Observa cómo Docker crea el entorno, detona el archivo y genera el reporte.

## DISCLAIMER
Este proyecto fue creado con fines estrictamente educativos y de investigación. El autor no se hace responsable del mal uso de esta herramienta. Nunca ejecutes malware real en tu máquina host sin las debidas precauciones.

Hecho por Diego Hernández Vázquez.

## NOTA DE ALCANCE
Actualmente el motor de ejecución soporta scripts de Python. La arquitectura es escalable para soportar PDFs integrando herramientas como poppler-utils o qpdf en el Dockerfile y añadiendo un 'dispatcher' en el controlador que elija el comando de ejecución según la extensión del archivo

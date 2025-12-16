from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
import controller 

app = FastAPI(title="Malware Sandbox API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/scan")
async def scan_file(file: UploadFile = File(...)):
    try:
        # 1. Guardar archivo
        # Guardamos la extensión original para saber qué es
        original_filename = file.filename
        file_ext = os.path.splitext(original_filename)[1].lower()
        
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"[API] Recibido: {original_filename} ({file_ext})")

        # 2. ANÁLISIS ESTÁTICO (Universal - Funciona para TODO)
        # Esto sacará Hash y Strings aunque sea una imagen o PDF
        report = controller.perform_static_analysis(file_path)
        
        # Sobreescribimos el nombre en el reporte para que se vea el original
        report["static_analysis"]["filename"] = original_filename

        # 3. ANÁLISIS DINÁMICO (Condicional)
        # Solo ejecutamos si es Python
        if file_ext == ".py":
            print("[API] Detectado script Python. Iniciando detonación...")
            docker_client = controller.get_docker_client()
            dynamic_results = controller.analyze_dynamic(docker_client, file_path)
            report["dynamic_analysis"] = dynamic_results
        else:
            print("[API] Archivo no ejecutable. Saltando Sandbox.")
            # Creamos un reporte "dummy" para que el Frontend no se rompa
            report["dynamic_analysis"] = {
                "status": "skipped",
                "reason": f"El tipo de archivo '{file_ext}' no es soportado por el motor de ejecución dinámica actual.",
                "network_activity": [],
                "file_activity": []
            }

        # 4. Limpieza
        if os.path.exists(file_path):
            os.remove(file_path)

        return report

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        print(f"[API ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
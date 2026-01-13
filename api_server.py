from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import shutil
import os
import uuid
import controller 
import ai_analyst
import virustotal

class ChatRequest(BaseModel):
    question: str
    report: Dict[str, Any]

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
        original_filename = file.filename
        file_ext = os.path.splitext(original_filename)[1].lower()
        
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"[API] Recibido: {original_filename} ({file_ext})")

        report = controller.perform_static_analysis(file_path)

        file_hash = report["static_analysis"]["sha256"]

        vt_result = virustotal.get_reputation(file_hash)
        report["virustotal"] = vt_result
        
        report["static_analysis"]["filename"] = original_filename

        if file_ext == ".py":
            print("[API] Detectado script Python. Iniciando detonación...")
            docker_client = controller.get_docker_client()
            dynamic_results = controller.analyze_dynamic(docker_client, file_path)
            report["dynamic_analysis"] = dynamic_results
        else:
            print("[API] Archivo no ejecutable. Saltando Sandbox.")
            report["dynamic_analysis"] = {
                "status": "skipped",
                "reason": f"El tipo de archivo '{file_ext}' no es soportado por el motor de ejecución dinámica actual.",
                "network_activity": [],
                "file_activity": []
            }

        print("[API] Enviando logs al contenedor de IA...")
        report["ai_analysis"] = ai_analyst.analyze_report(report)

        if os.path.exists(file_path):
            os.remove(file_path)

        return report

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        print(f"[API ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        answer = ai_analyst.chat_with_analyst(request.question, request.report)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
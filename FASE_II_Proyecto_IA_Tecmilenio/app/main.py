from pathlib import Path
import re
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="Asistente financiero - prototipo académico", version="1.0.0")
BASE = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")
FAQ = [
    ("horario", "El horario de atención depende del canal. Consulte los canales oficiales de la institución.", "FAQ-001"),
    ("contraseña", "Para recuperar su contraseña, utilice exclusivamente el flujo oficial de recuperación de acceso.", "FAQ-002"),
    ("tarjeta", "Para reportar una tarjeta extraviada, contacte inmediatamente los canales oficiales de atención.", "FAQ-003"),
    ("estado de cuenta", "Consulte su estado de cuenta desde la aplicación o portal oficial de su institución.", "FAQ-004"),
]
class Question(BaseModel):
    question: str = Field(min_length=1, max_length=500)

@app.get("/")
def home():
    return FileResponse(BASE / "static" / "index.html")

@app.get("/health")
def health():
    return {"status": "ok", "mode": "demo_rules", "version": "1.0.0"}

@app.post("/api/chat")
def chat(payload: Question):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="La consulta no puede estar vacía")
    if re.search(r"\b(?:cvv|nip|pin|contraseña|password)\s*[:=]\s*\S+", question, re.I):
        return {"answer": "No comparta contraseñas, NIP ni CVV. Use canales oficiales.", "source": "SEG-001", "escalate": True, "confidence": 0.0}
    for keyword, answer, source in FAQ:
        if keyword in question.lower():
            return {"answer": answer, "source": source, "escalate": False, "confidence": 1.0}
    return {"answer": "No tengo una respuesta verificada. Le recomiendo contactar a un agente humano.", "source": "ESC-001", "escalate": True, "confidence": 0.0}

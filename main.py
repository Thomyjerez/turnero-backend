from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class TurnoCreate(BaseModel):
    name: str
    phone: str
    email: str
    specialty: str
    preferred_date: str

@app.post("/api/turnos")
async def create_turno(turno: TurnoCreate):
    TELEGRAM_BOT_TOKEN = os.getenv("8711309658:AAHfVnC3GpgJrUvAsJXBcJanHAeI2wBquSA")
    TELEGRAM_CHAT_ID = os.getenv("1604249964")

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise HTTPException(status_code=500, detail="Faltan credenciales de Telegram")

    mensaje_telegram = (
        f"*NUEVO TURNO SOLICITADO*\n\n"
        f"*Paciente:* {turno.name}\n"
        f"*Teléfono:* {turno.phone}\n"
        f"*Email:* {turno.email}\n"
        f"*Especialidad:* {turno.specialty}\n"
        f"*Fecha preferida:* {turno.preferred_date}\n\n"
        f"Por favor, contactar al paciente para confirmar el horario exacto."
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje_telegram,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return {"message": "Turno solicitado con éxito"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error al enviar el mensaje a Telegram")
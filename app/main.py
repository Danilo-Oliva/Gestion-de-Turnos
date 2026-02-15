from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Esto simula una base de datos por ahora
turnos_db = []

# Clase para validar qué datos recibimos
class Turno(BaseModel):
    cliente: str
    servicio: str
    fecha_hora: datetime

@app.get("/")
def home():
    return {"mensaje": "Sistema de Turnos funcionando"}

@app.post("/turnos/")
def crear_turno(turno: Turno):
    turnos_db.append(turno)
    return {"status": "Turno creado", "data": turno}

@app.get("/turnos/")
def obtener_turnos():
    return turnos_db
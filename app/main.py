from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/turnos/", response_model=schemas.Turno)
def crear_turno(turno: schemas.TurnoCreate, db: Session = Depends(get_db)):
    db_turno = models.TurnoModel(
        cliente=turno.cliente, 
        servicio=turno.servicio, 
        fecha_hora=turno.fecha_hora
    )
    db.add(db_turno)
    db.commit()
    db.refresh(db_turno)
    return db_turno

@app.get("/turnos/", response_model=List[schemas.Turno])
def obtener_turnos(db: Session = Depends(get_db)):
    return db.query(models.TurnoModel).all()
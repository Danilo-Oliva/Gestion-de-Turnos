from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Configuramos los orígenes permitidos. 
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"], # Permitir todos los headers
)

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

@app.delete("/turnos/{turno_id}")
def borrar_turno(turno_id: int, db: Session = Depends(get_db)):
    #Buscamos el turno por su ID
    turno = db.query(models.TurnoModel).filter(models.TurnoModel.id == turno_id).first()
    
    #Si no existe, lanzamos un error 404 (No encontrado)
    if turno is None:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    #Si existe, lo borramos y confirmamos los cambios
    db.delete(turno)
    db.commit()
    
    return {"mensaje": "Turno eliminado correctamente"}

@app.put("/turnos/{turno_id}", response_model=schemas.Turno)
def actualizar_turno(turno_id: int, turno_actualizado: schemas.TurnoCreate, db: Session = Depends(get_db)):
    turno_db = db.query(models.TurnoModel).filter(models.TurnoModel.id == turno_id).first()
    
    if turno_db is None:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    # Actualizamos los campos uno por uno
    turno_db.cliente = turno_actualizado.cliente
    turno_db.servicio = turno_actualizado.servicio
    turno_db.fecha_hora = turno_actualizado.fecha_hora
    
    db.commit()
    db.refresh(turno_db)
    
    return turno_db
from pydantic import BaseModel
from datetime import datetime

# Esquema para RECIBIR datos (Lo que el usuario manda)
# No pedimos el ID porque eso lo crea la base de datos sola.
class TurnoCreate(BaseModel):
    cliente: str
    servicio: str
    fecha_hora: datetime

# Esquema para DEVOLVER datos (Lo que el usuario ve)
# Acá sí incluimos el ID que generó la base de datos.
class Turno(TurnoCreate):
    id: int
    # No importa si no es un diccionario, leer los datos desde el objeto de la base de datos
    class Config:
        from_attributes = True
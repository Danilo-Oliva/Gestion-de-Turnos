from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class TurnoModel(Base):
    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String)
    servicio = Column(String)
    fecha_hora = Column(DateTime)
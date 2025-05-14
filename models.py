from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Usina(Base):
    __tablename__ = 'usinas'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    inversores = relationship("Inversor", back_populates="usina")

class Inversor(Base):
    __tablename__ = 'inversores'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    usina_id = Column(Integer, ForeignKey("usinas.id"))
    usina = relationship("Usina", back_populates="inversores")
    leituras = relationship("Leitura", back_populates="inversor")

class Leitura(Base):
    __tablename__ = 'leituras'
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    potencia_ativa = Column(Float)
    temperatura = Column(Float)
    inversor_id = Column(Integer, ForeignKey("inversores.id"))
    inversor = relationship("Inversor", back_populates="leituras")

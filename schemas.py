from pydantic import BaseModel
from datetime import datetime


class UsinaBase(BaseModel):
    nome: str

class UsinaCreate(UsinaBase): pass

class UsinaRead(UsinaBase):
    id: int
    class Config:
        orm_mode = True


class InversorBase(BaseModel):
    nome: str
    usina_id: int

class InversorCreate(InversorBase): pass

class InversorRead(InversorBase):
    id: int
    class Config:
        orm_mode = True

class LeituraBase(BaseModel):
    timestamp: datetime
    potencia_ativa: float
    temperatura: float

class LeituraCreate(LeituraBase):
    inversor_id: int

class LeituraRead(LeituraBase):
    id: int
    inversor_id: int
    class Config:
        orm_mode = True

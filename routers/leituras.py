from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import database, models

router = APIRouter(prefix="/leituras", tags=["Leituras"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/potencia-maxima/")
def potencia_maxima(
    inversor_id: int,
    data_inicio: datetime,
    data_fim: datetime,
    db: Session = Depends(get_db),
):
    try:
        result = (
            db.query(
                func.date(models.Leitura.timestamp).label("data"),
                func.max(models.Leitura.potencia_ativa).label("potencia_maxima")
            )
            .filter(
                models.Leitura.inversor_id == inversor_id,
                models.Leitura.timestamp.between(data_inicio, data_fim)
            )
            .group_by(func.date(models.Leitura.timestamp))
            .order_by("data")
            .all()
        )

        if not result:
            raise HTTPException(status_code=404, detail="Nenhuma leitura encontrada para os parâmetros fornecidos.")

        dados =  [{"data": r[0], "potencia_maxima": r[1]} for r in result]
        return JSONResponse(
            status_code=200,
            content={
                "dados": dados
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular potência máxima: {str(e)}")



@router.get("/media-temperatura/")
def media_temperatura(
    inversor_id: int,
    data_inicio: datetime,
    data_fim: datetime,
    db: Session = Depends(get_db),
):
    try:
        result = (
            db.query(
                func.date(models.Leitura.timestamp).label("data"),
                func.avg(models.Leitura.temperatura).label("temperatura_media")
            )
            .filter(
                models.Leitura.inversor_id == inversor_id,
                models.Leitura.timestamp.between(data_inicio, data_fim)
            )
            .group_by(func.date(models.Leitura.timestamp))
            .order_by("data")
            .all()
        )

        if not result:
            raise HTTPException(status_code=404, detail="Nenhuma leitura encontrada para os parâmetros fornecidos.")

        dados =  [{"data": r[0], "temperatura_media": r[1]} for r in result]
        return JSONResponse(
            status_code=200,
            content={
                "dados": dados
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular média de temperatura: {str(e)}")




@router.get("/geracao-inversor/")
def geracao_inversor(
    inversor_id: int,
    data_inicio: datetime,
    data_fim: datetime,
    db: Session = Depends(get_db),
):
    try:
        result = (
            db.query(func.sum(models.Leitura.potencia_ativa).label("geracao"))
            .filter(
                models.Leitura.inversor_id == inversor_id,
                models.Leitura.timestamp.between(data_inicio, data_fim)
            )
            .scalar()
        )

        dados = {"inversor_id": inversor_id, "geracao": result or 0.0}

        return JSONResponse(
            status_code=200,
            content={
                "dados": dados
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular geração do inversor: {str(e)}")



@router.get("/geracao-usina/")
def geracao_usina(
    usina_id: int,
    data_inicio: datetime,
    data_fim: datetime,
    db: Session = Depends(get_db),
):
    try:
        result = (
            db.query(func.sum(models.Leitura.potencia_ativa).label("geracao"))
            .join(models.Inversor, models.Inversor.id == models.Leitura.inversor_id)
            .filter(
                models.Inversor.usina_id == usina_id,
                models.Leitura.timestamp.between(data_inicio, data_fim)
            )
            .scalar()
        )

        dados =  {"usina_id": usina_id, "geracao": result or 0.0}

        return JSONResponse(
            status_code=200,
            content={
                "dados": dados
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular geração da usina: {str(e)}")


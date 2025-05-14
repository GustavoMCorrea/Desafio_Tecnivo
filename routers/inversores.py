from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database

router = APIRouter(prefix="/inversores", tags=["Inversores"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def criar_inversor(inversor: schemas.InversorCreate, db: Session = Depends(get_db)):
    try:
        if not inversor.nome or inversor.nome.strip() == "":
            raise HTTPException(status_code=400, detail="O nome do inversor é obrigatório.")

        usina = db.query(models.Usina).filter(models.Usina.id == inversor.usina_id).first()
        if not usina:
            raise HTTPException(status_code=400, detail="Usina associada não encontrada.")

        db_inv = models.Inversor(**inversor.dict())
        db.add(db_inv)
        db.commit()
        db.refresh(db_inv)

        return JSONResponse(
            status_code=201,
            content={
                "dados": {
                    "id": db_inv.id,
                    "nome": db_inv.nome,
                    "usina_id": db_inv.usina_id
                }
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar inversor: {str(e)}")


@router.get("/")
def listar_inversores(db: Session = Depends(get_db)):
    try:
        inversores = db.query(models.Inversor).all()
        return JSONResponse(
            status_code=200,
            content={
                "dados": [
                    {
                        "id": inv.id,
                        "nome": inv.nome,
                        "usina_id": inv.usina_id
                    } for inv in inversores
                ]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar inversores: {str(e)}")


@router.get("/{inversor_id}")
def obter_inversor(inversor_id: int, db: Session = Depends(get_db)):
    try:
        inversor = db.query(models.Inversor).filter(models.Inversor.id == inversor_id).first()
        if not inversor:
            raise HTTPException(status_code=404, detail="Inversor não encontrado")

        return JSONResponse(
            status_code=200,
            content={
                "dados": {
                    "id": inversor.id,
                    "nome": inversor.nome,
                    "usina_id": inversor.usina_id
                }
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar inversor: {str(e)}")


@router.put("/{inversor_id}")
def atualizar_inversor(inversor_id: int, dados: schemas.InversorCreate, db: Session = Depends(get_db)):
    try:
        if not dados.nome or dados.nome.strip() == "":
            raise HTTPException(status_code=400, detail="O nome do inversor é obrigatório.")

        inversor = db.query(models.Inversor).filter(models.Inversor.id == inversor_id).first()
        if not inversor:
            raise HTTPException(status_code=404, detail="Inversor não encontrado")

        usina = db.query(models.Usina).filter(models.Usina.id == dados.usina_id).first()
        if not usina:
            raise HTTPException(status_code=400, detail="Usina associada não encontrada.")

        for key, value in dados.dict().items():
            setattr(inversor, key, value)

        db.commit()
        db.refresh(inversor)

        return JSONResponse(
            status_code=200,
            content={
                "dados": {
                    "id": inversor.id,
                    "nome": inversor.nome,
                    "usina_id": inversor.usina_id
                }
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar inversor: {str(e)}")


@router.delete("/{inversor_id}")
def deletar_inversor(inversor_id: int, db: Session = Depends(get_db)):
    try:
        inversor = db.query(models.Inversor).filter(models.Inversor.id == inversor_id).first()
        if not inversor:
            raise HTTPException(status_code=404, detail="Inversor não encontrado")

        db.delete(inversor)
        db.commit()

        return JSONResponse(
            status_code=200,
            content={
                "dados": {"id": inversor.id, "nome": inversor.nome}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar inversor: {str(e)}")


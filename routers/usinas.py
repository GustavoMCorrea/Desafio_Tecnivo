from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
import database, models, schemas



router = APIRouter(prefix="/usinas", tags=["Usinas"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def criar_usina(usina: schemas.UsinaCreate, db: Session = Depends(get_db)):
    try:
        if not usina.nome or usina.nome.strip() == "":
            raise HTTPException(status_code=400, detail="O nome da usina é obrigatório.")

        db_usina = models.Usina(**usina.dict())
        db.add(db_usina)
        db.commit()
        db.refresh(db_usina)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "dados": {"id": db_usina.id, "nome": db_usina.nome}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar usina: {str(e)}")


@router.get("/")
def listar_usinas(db: Session = Depends(get_db)):
    try:
        usinas = db.query(models.Usina).all()
        return JSONResponse(
            status_code=200,
            content={
                "dados": [{"id": u.id, "nome": u.nome} for u in usinas]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar usinas: {str(e)}")


@router.get("/{usina_id}", response_model=schemas.UsinaRead)
def obter_usina(usina_id: int, db: Session = Depends(get_db)):
    usina = db.query(models.Usina).filter(models.Usina.id == usina_id).first()
    if not usina:
        raise HTTPException(status_code=404, detail="Usina não encontrada")
    return usina

@router.put("/{usina_id}")
def atualizar_usina(usina_id: int, dados: schemas.UsinaCreate, db: Session = Depends(get_db)):
    try:
        if not dados.nome or dados.nome.strip() == "":
            raise HTTPException(status_code=400, detail="O nome da usina é obrigatório.")

        usina = db.query(models.Usina).filter(models.Usina.id == usina_id).first()
        if not usina:
            raise HTTPException(status_code=404, detail="Usina não encontrada")

        for key, value in dados.dict().items():
            setattr(usina, key, value)

        db.commit()
        db.refresh(usina)

        return JSONResponse(
            status_code=200,
            content={
                "dados": {"id": usina.id, "nome": usina.nome}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar usina: {str(e)}")


@router.delete("/{usina_id}")
def deletar_usina(usina_id: int, db: Session = Depends(get_db)):
    try:
        usina = db.query(models.Usina).filter(models.Usina.id == usina_id).first()
        if not usina:
            raise HTTPException(status_code=404, detail="Usina não encontrada")

        db.delete(usina)
        db.commit()

        return JSONResponse(
            status_code=200,
            content={
                "dados": {"id": usina.id, "nome": usina.nome}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao deletar usina: {str(e)}")


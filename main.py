from fastapi import FastAPI
from database import Base, engine
from routers import usinas, inversores, leituras


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(usinas.router)
app.include_router(inversores.router)
app.include_router(leituras.router)

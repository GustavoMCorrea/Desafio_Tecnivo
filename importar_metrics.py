import json
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Usina, Inversor, Leitura

Base.metadata.create_all(bind=engine)

# Carrega os dados JSON
with open("metrics.json", "r") as f:
    dados = json.load(f)


db: Session = SessionLocal()


usina1 = Usina(id=1, nome="Usina 1")
usina2 = Usina(id=2, nome="Usina 2")

db.merge(usina1)
db.merge(usina2)


for inversor_id in range(1, 9):
    usina_id = 1 if inversor_id <= 4 else 2
    inversor = Inversor(id=inversor_id, nome=f"Inversor {inversor_id}", usina_id=usina_id)
    db.merge(inversor)


leituras = []
for registro in dados:
    leitura = Leitura(
        inversor_id=registro["inversor_id"],
        timestamp=datetime.fromisoformat(registro["datetime"]["$date"]),
        potencia_ativa=registro["potencia_ativa_watt"],
        temperatura=registro["temperatura_celsius"]
    )
    leituras.append(leitura)

db.bulk_save_objects(leituras)
db.commit()
db.close()

print(f"Importação concluída com sucesso: {len(leituras)} leituras inseridas.")

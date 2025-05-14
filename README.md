# ☀️ Solar API — Monitoramento de Usinas Fotovoltaicas

---

## 🚀 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) — Framework Web
- [SQLite](https://www.sqlite.org/) — Banco de dados
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [Pydantic](https://docs.pydantic.dev/) — Validação de dados (DTOs)
- [Uvicorn](https://www.uvicorn.org/) — ASGI server


---

## 🧩 Funcionalidades Implementadas

### 🔧 CRUD

- ✅ **Usinas**
- ✅ **Inversores**

### 📊 Agregações

- 🔹 Potência máxima por dia
- 🔹 Média da temperatura por dia
- 🔹 Geração do inversor por período
- 🔹 Geração da usina por período

### ✅ Validações

- Uso de **DTOs com Pydantic**
- Tratamento de erros `400`, `404`, `500`
- Respostas HTTP padronizadas (`status`, `mensagem`, `dados`)




---

## 🗂️ Estrutura do Projeto

```text
solar_api/
├── routers/
│   ├── usinas.py
│   ├── inversores.py
│   └── leituras.py
├── models.py
├── schemas.py
├── database.py
├── main.py
└── importar_metrics.py
```



---

## ▶️ Como Rodar o Projeto

### 1. Clone o repositório
```bash
git clone https://github.com/seuusuario/solar-api.git
cd solar-api
```
### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
### 3. Instale as dependências
```bash
pip install -r requirements.txt
```
### 4. Inicie o servidor
```bash
uvicorn main:app --reload
```
### 5. Acesse a documentação interativa
(http://localhost:8000/docs)

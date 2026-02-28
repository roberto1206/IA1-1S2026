# pip install fastapi uvicorn pyswip
# uvicorn main:app --reload
from fastapi import FastAPI
from repositories.prolog_repo import PrologRepo
from services.productos_service import ProductosService
from controllers.productos_controller import productos_router

app = FastAPI(title="Clase 03 - IA1")

# Repo (datos)
repo = PrologRepo("tienda.pl")

#Service
productos_service = ProductosService(repo)

#controller
app.include_router(productos_router(productos_service))
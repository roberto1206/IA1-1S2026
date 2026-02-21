from typing import List, Dict
from repositories.prolog_repo import PrologRepo

class ProductosService:
    def __init__(self, repo: PrologRepo):
        self.repo = repo

    def obtener_productos(self) -> List[str]:
        return self.repo.obtener_productos()

    def obtener_productos_con_precios(self) -> List[Dict]:
        return self.repo.obtener_productos_con_precios()

    def agregar_producto_persistente(self, nombre: str, precio: int) -> Dict:
        return self.repo.insertar_producto_persistente(nombre, precio)

    def obtener_precio_por_nombre(self, nombre: str):
        return self.repo.obtener_precio_por_nombre(nombre)
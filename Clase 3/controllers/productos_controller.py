from fastapi import APIRouter, Body
from services.productos_service import ProductosService

def productos_router(service: ProductosService) -> APIRouter:
    router = APIRouter(prefix="/productos", tags=["productos"])

    @router.get("")
    def get_productos():
        return {"productos": service.obtener_productos()}

    @router.get("/precios")
    def get_productos_precios():
        return {"items": service.obtener_productos_con_precios()}

    @router.post("")
    def post_producto(data: dict = Body(...)):
        nombre = data.get("producto")
        precio = data.get("precio")

        if not isinstance(nombre, str) or not nombre.strip():
            return {"error": "Campo 'producto' inválido"}
        if not isinstance(precio, int):
            return {"error": "Campo 'precio' debe ser entero"}

        return service.agregar_producto_persistente(nombre, precio)

    @router.get("/{nombre}")
    def get_precio_producto(nombre: str):
        return service.obtener_precio_por_nombre(nombre)
    
    return router
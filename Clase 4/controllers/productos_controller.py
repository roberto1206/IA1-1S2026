from fastapi import APIRouter, Body
from services.productos_service import ProductosService

def productos_router(service: ProductosService) -> APIRouter:
    router = APIRouter(prefix="/productos", tags=["productos"])

    #CRUD DE PRODUCTOS
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
    
    @router.put("/{nombre}")
    def put_precio_producto(nombre: str, data: dict= Body(...)):
        nuevo_precio = data.get("precio")
        if not isinstance(nuevo_precio, int):
            return{"error": "precio debe de ser entero, 'precio' no cumple"}
        return service.actualizar_precio(nombre, nuevo_precio)
    
    @router.delete("/{nombre}")
    def delete_producto(nombre:str):
        return service.eliminar_producto(nombre)
    
    return router
from pyswip import Prolog
from typing import Any, Dict, Optional, List
from pathlib import Path
import re

class PrologRepo:
    def __init__(self, prolog_file: str):
        self.prolog_file = Path(prolog_file).resolve()
        self.prolog = Prolog()
        self._consult_file()

    def _consult_file(self) -> None:
        self.prolog = Prolog()  # reinicia el motor
        path_str = self.prolog_file.as_posix()
        list(self.prolog.query(f"consult('{path_str}')."))

    def query_one(self, q: str) -> Optional[Dict[str, Any]]:
        return next(self.prolog.query(q), None)

    _safe_atom_re = re.compile(r"^[a-z][a-z0-9_]*$")

    def _to_prolog_atom(self, s:str) -> str:
        s = s.strip()
        if self._safe_atom_re.match(s): #juan Juan
            return s
        
        s_escaped = s.replace("'", "''") # Juan -> 'Juan'
        return f"'{s_escaped}'"

    def obtener_productos(self) -> List[str]:
        sol = self.query_one("productos(L).")
        if not sol:
            return []
        return [str(x) for x in sol["L"]]

    def obtener_productos_con_precios(self) -> List[Dict[str, Any]]:
        sol = self.query_one("productos_con_precio(L).")
        if not sol:
            return []
        items = []
        for par in sol["L"]:
            items.append({"producto": str(par[0]), "precio": int(par[1])})
        return items

    def obtener_precio_por_nombre(self, nombre: str) -> Dict[str, Any]:
        atom = self._to_prolog_atom(nombre)
        sol = self.query_one(f"precio({atom}, P).")
        if not sol:
            return {"error": "Producto no encontrado"}
        return {"producto": nombre, "precio": int(sol["P"])}

    # POST
    def insertar_producto_persistente(self, nombre: str, precio: int) -> Dict[str, Any]:
        if precio < 0:
            return {"error": "El precio no puede ser negativo"}

        atom = self._to_prolog_atom(nombre)

        # 1) Validar existencia
        exists = self.query_one(f"once(producto({atom})).")
        if exists is not None:
            return {"error": "El producto ya existe"}

        with self.prolog_file.open("a", encoding="utf-8") as f:
            f.write("\n")
            f.write(f"producto({atom}).\n")
            f.write(f"precio({atom}, {precio}).\n")

        self._consult_file()

        return {"mensaje": "Producto agregado y guardado", "producto": nombre, "precio": precio}

    # PUT
    def actulizar_precio(self, nombre:str, nuevo_precio: int) -> Dict[str,Any]:
        if nuevo_precio < 0:
            return {"error": "El precio no puede ser negativo"}
        
        atom = self._to_prolog_atom(nombre)

        # Verificar que exista
        if self.query_one(f"once(producto({atom})).") is None:
            return {"error": "Producto no existe"}
        
        contenido = self.prolog_file.read_text(encoding="utf-8").splitlines()
        nueva_linea_precio =  f"precio({atom}, {nuevo_precio})."

        actualizado = False
        nueva_lineas=[]

        for linea in contenido:
            s = linea.strip()

            # detecta correctamente el precio y ayuda a evitar el bug
            if s.startswith(f"precio({atom},"):
                # escribe solo una vez el nuevo precio y elimina duplicados
                if not actualizado:
                    nueva_lineas.append(nueva_linea_precio)
                    actualizado = True
                # si ya actualizo no se debe de agregar la linea vieja asi que se debe de saltar
                continue
            nueva_lineas.append(linea)

        # Si no tenía precio antes
        if not actualizado:
            nueva_lineas.append(nueva_linea_precio)

        #Sobreescribir el archivo
        self.prolog_file.write_text("\n".join(nueva_lineas), encoding="utf-8")

        #recargar prolog
        self._consult_file()

        return{"mensaje": "Precio actualizado", "producto": nombre, "precio nuevo": nuevo_precio}
    
    # Eliminar
    def eliminar_producto(self, nombre:str) -> Dict[str, Any]:
        atom = self._to_prolog_atom(nombre)

        #verifica si existe antes de borrar
        if self.query_one(f"once(producto({atom})).") is None:
            return {"error": "producto no encontrado"}
        
        lineas = self.prolog_file.read_text(encoding="utf-8").splitlines()

        #eliminar
        producto_line = f"producto({atom})."

        nuevas = []
        borrado_producto = 0
        borrados_precio = 0

        for linea in lineas:
            s = linea.strip()

            # borrar exactamente el hecho producto(atom).
            if s == producto_line:
                borrado_producto += 1
                continue

            # borrar cualquier precio(atom,precio)
            if s.startswith(f"precio({atom},"):
                borrados_precio += 1
                continue

            nuevas.append(linea)

        self.prolog_file.write_text("\n".join(nuevas), encoding="utf-8")
        self._consult_file()

        return {
            "mensaje":"Producto eliminado",
            "producto": nombre,
            "producto_borrados": borrado_producto,
            "precio_borrados": borrados_precio
        }
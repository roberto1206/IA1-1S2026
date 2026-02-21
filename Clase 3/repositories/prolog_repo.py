from pyswip import Prolog
from typing import Any, Dict, Optional
from pathlib import Path
import re

class PrologRepo:
    def __init__(self, prolog_file: str):
        self.prolog_file = Path(prolog_file).resolve()
        self.prolog = Prolog()
        self._consult_file()

    def _consult_file(self) -> None:
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
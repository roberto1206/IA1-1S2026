from datetime import datetime


class Bitacora:
    def __init__(self, archivo: str) -> None:
        self.archivo = archivo

    def escribir(self, mensaje: str) -> None:
        with open(self.archivo, "a", encoding="utf-8") as archivo:
            archivo.write(f"[{datetime.now()}] {mensaje}\n")
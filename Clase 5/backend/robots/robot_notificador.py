import os

from services.bitacora import Bitacora
from services.correo import Correo

class RobotNotificador:

    # crear robot
    def __init__(self, archivo_clientes: str, correo: Correo, bitacora: Bitacora) :
        self.archivo_clientes = archivo_clientes
        self.correo = correo
        self.bitacora = bitacora

    def procesar(self) -> None:
        # Validar credenciales
        if not self.correo.smtp_user or not self.correo.smtp_password:
            print("Error, faltan variables de entorno")
            self.bitacora.escribir("Error de configuracion SMTP")
            return
        
        # verificar archivo
        if not os.path.exists(self.archivo_clientes):
            print("Error no existe el archivo")
            self.bitacora.escribir("Archivo no encontrado")
            return
        
        # inicialzar contadores
        enviados = 0
        ignorados = 0
        errores_formato = 0
        self.bitacora.escribir("---Iniicio de ejecucion del robot---")

        # inciar el proceso
        with open(self.archivo_clientes, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

        # Leer cada cliente
        for numero_linea, linea in enumerate(lineas,start=1):
            linea = linea.strip()

            if not linea:
                continue

            partes = [p.strip() for p in linea.split(",")]

            #Ver si esta pendiente y validar datos de clientes.txt

            if len(partes) != 3:
                errores_formato +=1
                self.bitacora.escribir(f"Linea {numero_linea} invalida, formato incorrecto")
                continue

            nombre, correo_destino, estado = partes

            # decision del robot
            if estado.lower() == "pendiente":
                # ejecuta la accion
                if self.correo.enviar(correo_destino, nombre):
                    enviados += 1
            elif estado.lower() == "quebrado":
                if self.correo.enviar_quebrado(correo_destino, nombre):
                    enviados +=1
            else:
                ignorados += 1
                self.bitacora.escribir(f"No se envio correo {nombre} porque el estado es {estado}")

        # Registar bitacora
        self.bitacora.escribir("---Fin del Robot---")
        self.bitacora.escribir(f"Resumen, | enviados: {enviados} | ignorados: {ignorados} | errores con el formato: {errores_formato}")

        print("proceso finalizado")


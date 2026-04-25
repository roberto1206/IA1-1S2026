import cv2


from signal_detector import SignalDetector
from telegram_service import TelegramService


class AppSignal:
    def __init__(self):
        self.detector = SignalDetector()
        self.telegram = TelegramService()

        self.lista_mensajes = []
        self.texto_sena_actual = "No hay mano"

        self.boton_capturar = (30, 400, 280, 460)
        self.boton_enviar = (320, 400, 570, 460)

        self.nombre_ventana = "Reconocimiento de Senas"

    def run(self):
        cap = cv2.VideoCapture(0)

        cv2.namedWindow(self.nombre_ventana)
        cv2.setMouseCallback(self.nombre_ventana, self.click_mouse)

        while True:
            ret, frame = cap.read()

            if not ret:
                print("No se pudo leer la cámara")
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            dedos, self.texto_sena_actual = self.detector.detect_signals(rgb, frame)
            total = sum(dedos)

            self.dibujar_interfaz(frame, total)

            cv2.imshow(self.nombre_ventana, frame)

            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def click_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.esta_dentro_boton(x, y, self.boton_capturar):
                self.capturar_mensaje()

            if self.esta_dentro_boton(x, y, self.boton_enviar):
                self.enviar_lista_mensajes()

    def capturar_mensaje(self):
        mensaje = self.detector.mensajes_signal(self.texto_sena_actual)

        if mensaje:
            self.lista_mensajes.append(mensaje)
            print("Mensaje agregado a la lista:", mensaje)
            print("Lista actual:", self.lista_mensajes)
        else:
            print("No hay una seña válida para capturar")

    def enviar_lista_mensajes(self):
        if len(self.lista_mensajes) == 0:
            print("Lista vacía")
            self.telegram.enviar_mensaje("Lista vacía")
            return

        mensaje_final = "\n".join(self.lista_mensajes)
        self.telegram.send_message(mensaje_final)

        print("Mensajes enviados:")
        print(mensaje_final)

        self.lista_mensajes.clear()
        print("Lista limpiada")

    def esta_dentro_boton(self, x, y, boton):
        x1, y1, x2, y2 = boton
        return x1 <= x <= x2 and y1 <= y <= y2

    def dibujar_interfaz(self, frame, total):
        cv2.putText(
            frame,
            f"Dedos: {total}",
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3
        )

        cv2.putText(
            frame,
            f"Sena: {self.texto_sena_actual}",
            (30, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1,
            (255, 0, 0),
            3
        )

        cv2.putText(
            frame,
            f"Mensajes en lista: {len(self.lista_mensajes)}",
            (30, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        y = 200
        for i, mensaje in enumerate(self.lista_mensajes[-4:], start=1):
            cv2.putText(
                frame,
                f"{i}. {mensaje}",
                (30, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
            y += 30

        self.dibujar_boton(
            frame,
            "Capturar mensaje",
            self.boton_capturar,
            (0, 120, 255)
        )

        self.dibujar_boton(
            frame,
            "Enviar lista",
            self.boton_enviar,
            (0, 180, 0)
        )

    def dibujar_boton(self, frame, texto, boton, color):
        x1, y1, x2, y2 = boton

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

        cv2.putText(
            frame,
            texto,
            (x1 + 20, y1 + 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )
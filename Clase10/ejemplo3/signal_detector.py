import cv2
import mediapipe as mp

class SignalDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def detect_signals(self,frame_rgb, frame_original):
        results = self.hands.process(frame_rgb)

        dedos_levantados = [0,0,0,0,0]
        text_singal = "No hay mano"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame_original, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                h, w, _ = frame_original.shape
                puntos = []

                for lm in hand_landmarks.landmark:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    puntos.append((cx, cy))

                if puntos[4][0] < puntos[3][0]:  # Pulgar
                    dedos_levantados[0] = 1

                if puntos[8][1] < puntos[6][1]:  # Índice
                    dedos_levantados[1] = 1

                if puntos[12][1] < puntos[10][1]:  # Medio
                    dedos_levantados[2] = 1

                if puntos[16][1] < puntos[14][1]:  # Anular
                    dedos_levantados[3] = 1

                if puntos[20][1] < puntos[18][1]:  # Meñique
                    dedos_levantados[4] = 1
                
                text_singal = self.interpretar_senal(dedos_levantados)

        return dedos_levantados, text_singal
    
    def interpretar_senal(self, dedos):
        if dedos == [0, 0, 0, 0, 0]:
            return "Puño"
        elif dedos == [1, 1, 1, 1, 1]:
            return "Mano abierta"
        elif dedos == [0, 1, 0, 0, 0]:
            return "Índice levantado"
        elif dedos == [1, 1, 1, 0, 0]:
            return "Estas haciendo la señal de 'tres'"
        elif dedos == [1, 1, 0, 0, 0]:
            return "Pulgar e índice levantados. pistolita de la mano"
        elif dedos == [0, 1, 1, 0, 0]:
            return "paz"
        elif dedos == [1, 1, 0, 0, 1]:
            return "spiderman"
        elif dedos == [1, 0, 0, 0, 1]:
            return "rock?"
        else:
            return "signal no reconocida"

    
    def mensajes_signal(self, signal):
        mensssages = {
            "Puño": "¡Puño detectado! ¡Fuerza y determinación!",
            "Mano abierta": "¡Mano abierta detectada! ¡Paz y tranquilidad!",
            "Índice levantado": "¡Índice levantado detectado! ¡Atención y enfoque!",
            "Estas haciendo la señal de 'tres'": "¡Señal de 'tres' detectada! ¡Diversión y energía!",
            "Pulgar e índice levantados. pistolita de la mano": "¡Pistolita detectada! ¡Diversión y energía!",
            "paz": "¡Señal de paz detectada! ¡Armonía y serenidad!",
            "spiderman": "¡Señal de Spiderman detectada! ¡Aventuras y valentía!",
            "rock?": "¡Señal de rock detectada! ¡Actitud y rebeldía!",
        }

        return mensssages.get(signal, "")
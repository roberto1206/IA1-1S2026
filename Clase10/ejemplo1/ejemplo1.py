# py -3.12 -m venv venv
# venv\Scripts\activate
# python -m pip install opencv-python mediapipe==0.10.21

import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

DEDOS = [ "Pulgar", "Indice", "Medio", "Anular", "Menique" ]

def reconocer_gesto(dedos):
    pulgar, indice, medio, anular, menique = dedos

    if dedos == [0, 0, 0, 0, 0]:
        return "silencio"

    if dedos == [1, 0, 0, 0, 0]:
        return "Pulgar levantado o me gusta"      
    
    if dedos == [0, 1, 0, 0, 0]:
        return "Índice levantado"
    
    if dedos == [1,1, 0, 0, 0]:
        return "Pulgar e índice levantados"
    
    if dedos == [1,1,1,1,1]:
        return "Todos los dedos levantados"
    
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7) as hands:

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo acceder a la cámara")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        dedos_levantados = [0, 0, 0, 0, 0]
        texto_dedos = "Gesto no reconocido"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                h, w , _ = frame.shape
                puntos=[]
                
                for id, lm in enumerate(hand_landmarks.landmark):
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
                if puntos[20][1] < puntos[18][1]:  # Menique
                    dedos_levantados[4] = 1

                texto_dedos = reconocer_gesto(dedos_levantados)

        total = sum(dedos_levantados)

        cv2.putText(frame, f'Dedos levantados: {total}', (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        cv2.putText(frame, texto_dedos, (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 3)

        cv2.imshow('Reconocimiento de Gestos', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
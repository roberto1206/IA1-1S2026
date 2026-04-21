# pip install opencv-python numpy

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convertir la imagen de BGR a HSV
    # H = color
    # S = intensidad del color
    # V = brillo
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir el rango de color a detectar
    lower_color = np.array([18, 80, 80])
    upper_color = np.array([40, 255, 255])

    # Crear una máscara para el color definido
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Encontrar contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Recorrer los contornos encontrados y dibujar un rectángulo alrededor de los objetos detectados
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # Filtrar por área
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
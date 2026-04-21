import cv2
from matplotlib.pyplot import contour

#Activa camara
cap = cv2.VideoCapture(0)

# Imagen anterior y actual
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while True:
    # Calcula la diferencia entre las dos imágenes
    ## Como lo hace? -> Compara cada pixel de las dos imágenes y devuelve un nuevo array con la diferencia absoluta entre los valores de cada pixel.
    diff = cv2.absdiff(frame1, frame2)

    # Convierte la diferencia a blanco y negro
    ## Blanco y negro ayuda a simplificar el procesamiento
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Aplicar un desenfoque
    ## El desenfoque ayuda a eliminar el ruido y mejorar la detección de contornos
    ## (5,5) Tamaño del filtro
    ## 0 OpenCV calcula automaticamente
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Imagen binaria
    ## La imagen binaria convierte los valores de los píxeles en 0 o 255
    ## Blanco movimiento; Negro no se mueve
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Contorno para detectar algo
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Contruir el bounding box o el rectangulo de movimiento
        (x, y, w, h) = cv2.boundingRect(contour)
        # Filtrar el ruido solo considerara movimientos grandes
        if cv2.contourArea(contour) > 1000:
            #Dibuja el rectangulo
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Movimiento', frame1)

    # Actualizar los frames
    ## La imagen anterior pase a ser la nueva imagen
    ## Frame 1 = anterior
    ## Frame 2 = nuevo
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
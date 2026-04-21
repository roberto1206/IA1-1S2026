import cv2

# Haar Cascades
## Ya aprendio que es un rostro, ahora vamos a enseñarle a la computadora a reconocerlo

#Clasifica el rostro, lo detecta y lo dibuja
## Que es haarcascade_frontalface_default.xml -> Es un archivo que contiene los datos necesarios para detectar rostros en una imagen
face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

# Instancia de la camara
cap = cv2.VideoCapture(0)

# bucle
while True:
    
    # ret =  Si se iniciar la camara
    # frame = La imagen que se captura de la camara
    ret, frame = cap.read()

    if not ret:
        print("No se pudo iniciar la camara")
        break

    # gris -> Imagen en escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # faces -> Lista de coordenadas de los rostros detectados en la imagen
    # MultiScale -> Es un algoritmo que se utiliza para detectar objetos en una imagen, en este caso rostros, a diferentes escalas
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Delimitar el rostro con un rectangulo
    # Para obtener todas las coordenadas de los rostros
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
    
    # Mostrar la imagen con los rostros detectados
    cv2.imshow("Rostros", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
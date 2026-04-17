# pip install scikit-learn

from sklearn.feature_extraction.text import TfidfVectorizer # Sirve para convertir texto en numeros
from sklearn.naive_bayes import MultinomialNB 

# Datos de entrenamiento

correos = [
    "Gana dinero ahora",
    "Tu pariente lejano ha fallecido y te quiere dejar tu herencia",
    "Haz clic aqui para ganar premio",
    "Reunion a las 10 p.m.",
    "Adjunto informe solicitado",
    "Se revisa el lunes en la oficina"
]

# Etiquetas
# 1 -> spam
# 0 -> no spam
etiquetas = [1,1,1,0,0,0]

# Convertir el texto a numeros TF-IDF
vectorizador = TfidfVectorizer()
x = vectorizador.fit_transform(correos)

# Crear el modelo
modelo = MultinomialNB()
modelo.fit(x,etiquetas)

# Correos para evaluar
nuevos_correos = [
    "Haz ganado el sorteo, tienes que depositar para recibir el premio",
    "Haz ganado un carro",
    "Reunion importante a las 8 a.m. No faltar",
    "Trabajo atrasado, favor de uniter a esta sesion",
]

x_new = vectorizador.transform(nuevos_correos)

# Prediccion
predicciones = modelo.predict(x_new)

# Mostrar resultados

for correo, pred in zip(nuevos_correos, predicciones):
    if pred == 1:
        print(f"'{correo}' esto es igual a SPAM")
    else:
        print(f"''{correo} es no es spam")

# pyswip
# pip install pyswip
from pyswip import Prolog

# Crear el motor Prolog
prolog = Prolog()

# Agregar hechos
prolog.assertz("padre(juan, maria)")
prolog.assertz("padre(juan, pedro)")
prolog.assertz("padre(carlos, juan)")

# Agregar regla
prolog.assertz("progenitor(X, Y) :- padre(X, Y)")

# Consulta simple
print("Progenitores de maria:")
for resultado in prolog.query("progenitor(X, pedro)"):
    print(resultado["X"])

from pyswip import Prolog

# Crear motor Prolog
prolog = Prolog()

# Cargar archivo Prolog
prolog.consult("./ayuda/auxiliar.pl")

# Consulta 1: Abuelos de maria
print("Abuelos de maria:")
for r in prolog.query("abuelo(X, maria)"):
    print(r["X"])

# Consulta 2: Ancestros directos de pedro
print("\nAncestros directos de maria:")
for r in prolog.query("ancestro_directo(X, maria)"):
    print(r["X"])

# Consulta 3: ¿Carlos es ancestro directo de maria?
print("\n¿Carlos es ancestro directo de maria?")
resultado = list(prolog.query("ancestro_directo(carlos, maria)"))
print("Sí" if resultado else "No")
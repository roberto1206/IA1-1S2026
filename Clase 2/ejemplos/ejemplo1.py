from pyswip import Prolog

prolog = Prolog()
prolog.consult("./rule/rule1.pl")

print("1) adulto: ")
for personas in prolog.query("adulto(X)"):
    print(personas["X"])

print("2) Tiene 17 y es adulto ")
for personas in prolog.query("es_adulto_o_17(X)"):
    print(personas["X"])
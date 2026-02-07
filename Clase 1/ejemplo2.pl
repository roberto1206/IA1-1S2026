#hechos
#padre con hijos
padre(juan,maria).
padre(juan,pedro).

#padre con hijos
padre(manuel,omar).
padre(manuel,sofia).

#abuelo y padre
padre(carlos,juan).

abuelo(X,Y) :- padre(X,Z), padre(Z,Y).
hermano(X,Y) :- padre(Z, X), padre(Z, Y).
# X es padre de Y; si X es padre de Z y Z es padre de Y

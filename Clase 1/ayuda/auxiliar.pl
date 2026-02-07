% Hechos
padre(juan, maria).
padre(juan, pedro).
padre(carlos, juan).

% Reglas simples
progenitor(X, Y) :- padre(X, Y).

abuelo(X, Y) :-
    padre(X, Z),
    padre(Z, Y).

ancestro_directo(X, Y) :-
    padre(X, Y).

ancestro_directo(X, Y) :-
    abuelo(X, Y).
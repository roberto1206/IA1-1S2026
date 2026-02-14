% Unificar estandar: Comparar el tipo dato
% X = 10
unificar_ejem(A,B) :- A = B.

% No unificar: True si A y B no pueden unificarse
no_unificar(A,B) :- A \= B.
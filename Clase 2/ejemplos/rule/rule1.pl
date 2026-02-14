persona(ana,20).
persona(javier,35).
persona(edgar,17).
persona(jimena,22).

adulto(N) :- persona(N, E), E >= 18.

es_adulto_o_17(N) :- adulto(N) ; (persona(N,E), E =:= 17).

% N -> javier
% adulto -> persona(javier, 35), E>= 18 -> true
% es_adulto_o_17(javier) -> false ; persona(javier, 35), 35 == 20? false
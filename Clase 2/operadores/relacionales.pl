% A mayor que B
es_mayor(A,B) :- A>B.

% A Mayor que o igual B
es_mayor_igual(A,B) :- A >= B.

% A menor que B
es_menor(A,B) :- A<B.

% A menor o igual que B
es_menor_o_igual(A,B) :- A =< B.

% =:= Si es igual
es_igual(A,B) :- A =:= B.

% =\= no es igual
no_es_igual(A,B) :- A =\= B.

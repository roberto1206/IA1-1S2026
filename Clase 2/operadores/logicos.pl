% AND -> ,
ambos_positivos(A,B) :- A=0 , B>0.

%OR -> ;
alguno_zero(A,B) :- A =:= 0 ; B =:=0.

%NOT -> \+
no_es_igual(A,B) :- \+ (A =:= B).
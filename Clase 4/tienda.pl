:- dynamic producto/1.
:- dynamic precio/2.
:- discontiguous producto/1.
:- discontiguous precio/2.

% datos aqui se declararon hechos:
producto(frijol).
producto(krispies).
producto(papas).
producto(maiz).
producto(galletas).

precio(frijol, 5).
precio(krispies, 20).
precio(papas, 7).
precio(maiz, 8).
precio(galletas, 7).

% Consultas
% Ayuda del backend --No olvidar--

% get simple
productos(L) :- findall(P, producto(P), L).

% get con precio
productos_con_precio(L) :- findall([P, Precio], precio(P, Precio), L).

%post de productos
precio_producto(Nombre, Precio) :-
    precio(Nombre, Precio).

producto(sopa).
precio(sopa, 90).
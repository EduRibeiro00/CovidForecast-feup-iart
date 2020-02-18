:- use_module(library(lists)).

%estado inicial
estado_inicial(b(0,0)).

%estado final
estado_final(b(2,0)).

%transições entre estados
sucessor(b(X,Y), b(4,Y)) :- X<4.
sucessor(b(X,Y), b(X,3)) :- Y<3.
sucessor(b(X,Y), b(0,Y)) :- X>0.
sucessor(b(X,Y), b(X,0)) :- Y>0.
sucessor(b(X,Y), b(4,Y1)) :-
    X+Y>=4,
    X<4,
    Y1 is Y-(4-X).

sucessor(b(X,Y), b(X1,3)) :-
    X+Y>=3,
    Y<3,
    X1 is X-(3-Y).

sucessor(b(X,Y), b(X1,0)) :-
    X+Y<4,
    Y>0,
    X1 is X+Y.

sucessor(b(X,Y), b(0,Y1)) :-
    X+Y<3,
    X>0,
    Y1 is X+Y.

% depth first search
dfs(E, _, [E]):-estado_final(E).
dfs(E, V, [E|R]):-
    sucessor(E, E2),
    \+ member(E2, V),
    dfs(E2, [E2|V], R).

bfs(E, _, _, [E]):- estado_final(E).
bfs(E, V, L, [E|R]):-
    findall(E2, (sucessor(E, E2), \+ member(E2, V)), L2),
    append(L, L2, L3),
    append(V, L2, New_V),
    L3 = [New_E | New_L],
    bfs(New_E, New_V, New_L, R).

start(dfs, S):-estado_inicial(Node), dfs(Node, [Node], S).
start(bfs, S):-estado_inicial(Node), bfs(Node, [Node], [], S), write(S).

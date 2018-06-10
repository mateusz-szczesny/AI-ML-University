male(franciszek).
male(jan).
male(krzysztof).
male(wojciech).
male(robert).
male(bogdan).

female(wanda).
female(maria).
female(anna).
female(ewa).
female(zofia).
female(katarzyna).

marriage(jan, maria).
marriage(maria, jan).
marriage(bogdan, anna).
marriage(anna, bogdan).
marriage(wojciech, zofia).
marriage(zofia, wojciech).

parent(franciszek, maria).
parent(jan, krzysztof).
parent(maria, krzysztof).
parent(jan, wojciech).
parent(maria, wojciech).
parent(wanda, bogdan).
parent(bogdan, zofia).
parent(bogdan, ewa).
parent(anna, zofia).
parent(anna, ewa).
parent(zofia, robert).
parent(zofia, katarzyna).
parent(wojciech, robert).
parent(wojciech, katarzyna).

mother(X, Y) :- female(X), parent(X, Y).
father(X, Y) :- male(X), parent(X, Y).
son(X, Y) :- male(X), parent(Y, X).
daughter(X, Y) :- female(X), parent(Y, X).
grandfather(X, Y) :- male(X), parent(X, Somebody), parent(Somebody, Y).
grandmother(X, Y) :- female(X), parent(X, Somebody), parent(Somebody, Y).
sister(X, Y) :- female(X), parent(Somebody, X), parent(Somebody, Y), X \= Y.
sister(X, Y) :- male(X), parent(Somebody, X), parent(Somebody, Y), X \= Y.
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Somebody), ancestor(Somebody, Y).
descendant(X, Y) :- parent(Y, X).
descendant(X, Y) :- parent(Y, Somebody), ancestor(Somebody, X).

aunt(X, Y) :- female(X), sister(X, Par), parent(Par, Y).
uncle(X, Y) :- male(X), brother(X, Par), parent(Par, Y).
			 
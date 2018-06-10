plywa(adam).
plywa(jan).

biega(jan).
biega(marek).

dobra_kondycja(jan).
dobra_kondycja(marek).

sportowiec(X) :- plywa(X), biega(X).
zawody(X) :- sportowiec(X), dobra_kondycja(X).
pilkarz(X) :- biega(X), dobra_kondycja(X).

/**
 * Kto bierze udział w zawodach? | zawody(X).
 * ans: jan
 *
 * Czy jest ktoś kto jest piłkarzem i pływakiem? | pilkarz(X), plywa(X).
 * ans: jan
 *
 * Kto ma kondycję? | dobra_kondycja(X).
 * ans: jan, marek
 *
 * Kim jest Marek? 
 * ans: 
 *
 * Kto jest sportowcem? | sportowcem(X).
 * ans: jan
 *
 * Kto biega i ma dobrą kondycją? | biega(X), dobra_kondycja(X).
 * ans: jan, marek
 *
 */
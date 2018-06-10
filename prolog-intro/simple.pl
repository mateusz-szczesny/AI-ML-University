man(marek).
man(jan).
man(karol).

woman(dominika).
woman(oliwia).
woman(basia).
woman(ala).

like(oliwia, karol).
like(karol, koty).
like(jan, psy).

like(marek, X) :- woman(X).
like(ala, X) :- like(marek, X).

/**
 * Questions:
 * 
 * man(jan). -> true
 * man(oliwia). -> false
 * 
 * man(X) -> X={marek, jan, karol}
 * 
 * woman(marek) -> false
 * woman(ala). -> true
 * 
 * like(oliwia, karol). -> true
 * like(oliwia, jan). -> false
 * 
 * like(marek, X). -> X = {dominika, oliwia, basia, ala}
 * like(ala, X). -> 
 */

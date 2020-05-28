animal(dog)  :- is_true('has fur'), is_true('says woof').
animal(cat)  :- is_true('has fur'), is_true('says meow').
animal(duck) :- is_true('has feathers'), is_true('says quack').
is_true(Q) :-
        format("~w?\n", [Q]),
        read(yes).
%---------------------------------------------------------------------

:-dynamic received/1.
:-dynamic json/1.

:-dynamic textt/1.
:-dynamic intent/1.
:-dynamic entities/1.
:-dynamic entity/2.

:-use_module(library(http/json)).
get_d(FPath, Dicty) :-
	open(FPath, read, Stream),
	json_read(Stream, Dicty),
	close(Stream)
	.

handling_received:-
	get_d('H:/HomeAssistant/1.json', json(Object)),
	not(received(Object)),
	asserta(received(Object)),
	listing(received)
	.
handling_received:-listing(received).

populate:-
	retract(received(A)),
	processing(A).

processing([(text=H)|T]):-
	asserta(textt(H)),
	processing(T).

processing([(intent=B)|T]):-
	asserta(intent(B)),
	processing(T).

processing([(entities=E)|T]):-
	asserta(entities(E)),
	processing(E),
	processing(T).

processing([json(E)|T]):-
	processing(E),
	processing(T).

processing([(entity=E) | T]) :-
	asserta(entity(E,X)),
	processing(T).

processing([(value=V) | T]) :-
	retract(entity(E,_)),
	asserta(entity(E,V)).

processing([]).
processing([_|T]):-processing(T).

clean:-
	retractall(entity(_,_)),
	retractall(entities(_)),
	retractall(textt(_)),
	retractall(intent(_)),
	retractall(received(_)).

listAll:-
	listing(received(_)),
	listing(textt(_)),
	listing(intent(_)),
	listing(entities(_)),
	listing(entity(_,_)).
















GM-IC.

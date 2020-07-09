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
	get_d('H:/HomeAssistant/sedinta.json', json(Object)),
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
	asserta(entity(E,_)),
	processing(T).

processing([(value=V) | _]) :-
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

% trb apelat cu parametru
manageRequest:-  intent(X),
                manageRequest(X).
manageRequest(adaugaCalendarEvent):-write(adaugaCalendarEvent),nl,
        verifyData(Data),!,
        verifyOraInceput(Ora),!,
        verifyOraFinal(Data,Ora, OraFinal),!.


verifyData(X):-entity(data,X),write(X),nl,!.
verifyData(X):-entity(data_timp,X),write(X),nl,!.
verifyData(X):-write(noDataFound),nl,!.

verifyOraInceput(X):-entity(ora_inceput, X),write(X),nl,!.
verifyOraInceput(X):-entity(ora_inceput_relativ, X),write(X),nl,!.
verifyOraInceput(X):-write('no hour found'),nl,!.

manageRequest(intreabaCalendarEvent):-write(intreabaCalendarEvent).

intreabaEvent(Data, Ora, OraFinal).
verifyOraFinal(Data, Ora, OraFinal):-entity(ora_final, OraFinal),write(OraFinal),nl,!.
verifyOraFinal(Data, Ora, OraFinal):-intreabaEvent(Data, Ora).

intreabaEvent(Data,Ora,OraFinal):-write('Exista ora final'),nl,
                                  write(Data),nl,
                                  write(Ora),nl,
                                  write(OraFinal),nl.

intreabaEvent(Data,Ora):-write('Nu exista ora final'),nl,
                        write(Data),nl,
                        write(Ora),nl.


entity(gabi1,gabi2).











GM-IC.

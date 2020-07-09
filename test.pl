:-dynamic received/1.
:-dynamic json/1.

:-dynamic textt/1.
:-dynamic intent/1.
:-dynamic entities/1.
:-dynamic entity/2.

% response
:-dynamic resp_data/1.
:-dynamic resp_data_timp/1.
:-dynamic resp_ora_inceput/1.
:-dynamic resp_ora_final/1.

:-use_module(library(http/json)).

get_d(FPath, Dicty) :-
	open(FPath, read, Stream),
	json_read(Stream, Dicty),
	close(Stream)
	.

handling_received:-
	get_d('C:/Users/Ionut/Desktop/proiecte/HomeAssistant/requestFaraDiac.json', json(Object)),
	not(received(Object)),
	asserta(received(Object)),
	listing(received)
	.

handling_received:-listing(received).

populate:- !,
	retract(received(A)),
	processing(A), !.

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

<<<<<<< HEAD
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


=======
listResponses:-
	listing(resp_data(_)),
	listing(resp_data_timp(_)),
	listing(resp_ora_inceput(_)),
	listing(resp_ora_final(_)).
>>>>>>> eab215f7b3f7dcc02d38b5151363943400b30969


manageRequest(Response):-  intent(X),
                manageRequest(X, Response).
manageRequest(adaugaCalendarEvent, Response):-
		entity(event, E),
        verifyData(Data, L1),!,
        verifyOraInceput(Ora, L2),!,
		verifyOraFinal(OraFinal, L3),!,
		append(L1, L2, R1),
		append([event], R1, R2),
		append(R2, L3, Response).

manageRequest(intreabaCalendarEvent, Response):-
		verifyData(Data, L1),!,
		verifyOraInceput(Ora, L2),!,
		verifyOraFinal(OraFinal, L3),!,
		append(L1, L2, R1),
		append(R1, L3, Response).

verifyEvent(X, [event]) :- entity(event, X).
verifyEvent(_, [error]).

verifyData(X, [data]):-entity(data,X), !.
verifyData(X, [data_timp]):-entity(data_timp,X),!.
verifyData(_, [warning]):-write(noDataFound),nl,!.

verifyOraInceput(X, [ora_inceput]):-entity(ora_inceput, X), !.
verifyOraInceput(X, [ora_inceput_relativ]):-entity(ora_inceput_relativ, X), !.
verifyOraInceput(_, [error]):-write('no hour found'),nl,!.

manageRequest(intreabaCalendarEvent, Response):-write(intreabaCalendarEvent).

verifyOraFinal(OraFinal, [ora_final]):-entity(ora_final, OraFinal),write(OraFinal).
verifyOraFinal(_, [warning]).


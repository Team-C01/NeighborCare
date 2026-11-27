# NeighborCare - Guida operativa

## Flusso normale

1. Un PM o TM con Write crea una Issue usando il template Task per agente, assegna i responsabili e applica `fase:piano`.
2. Il Pianificatore pubblica il piano. Un collaboratore Write lo verifica; se va bene applica `fase:implementazione` (questa label è l'autorizzazione). Non serve un commento aggiuntivo.
3. L'Implementatore pubblica il codice su un branch del task e apre una Draft PR con gli stessi assegnatari della Issue. Il runner verifica l'ambito prima della pubblicazione; la CI verifica il codice.
4. Applicare `fase:test` alla PR. Il Tester indipendente aggiunge o aggiorna i test, li fa eseguire dalla CI e attende il risultato. Pubblica in PR copertura, esito, conteggi ed eventuali errori; se la CI fallisce la fase non è superata. Se non servono modifiche, riusa una CI valida del commit corrente oppure la avvia se assente, senza produrre commit fittizi.
5. Verificare il commento CI aggiornato nella PR, i dettagli in Actions e i Test Frame. La CI parte sui push manuali e dopo ogni commit dell'agente, senza avvio duplicato su apertura o sincronizzazione PR. Se non parte, usare Actions > CI > Run workflow selezionando il branch della PR.
6. Selezionare Ready for review una sola volta. Il Revisore parte automaticamente anche dopo un nuovo commit su una PR non Draft. Il Revisore AI pubblica rilievi e suggerimenti consultivi, con commit, contesto e stato CI.
7. Una persona con Write non coinvolta nel task verifica i risultati, risolve eventuali rilievi reali e approva la PR. La review umana invia la CI finale sul merge proposto: attendere repository-checks verde, quindi effettuare il merge manuale. Il check di una CI avviata via workflow_dispatch da solo non soddisfa il Ruleset.

## Se qualcosa non va

Per ripianificare, l'agente riceve il testo della Issue, l'ultimo piano, la richiesta attuale e la discussione cronologica, entro il limite del contesto disponibile. Non usa soltanto l'ultimo commento.

Usare un commento nella conversazione della Issue o della PR:

| Dove | Commento | Effetto |
| --- | --- | --- |
| Issue | `AGENTE PIANO:` + spiegazione | Nuovo piano |
| PR | `AGENTE CORREGGI:` + problema da risolvere | Correzione sul branch della stessa PR |
| PR | `AGENTE TEST:` | Nuova sessione Tester |
| PR

Anche rimuovere e riapplicare la label della fase avvia un nuovo run. Non serve una label aggiuntiva, un particolare assegnatario o un commento di autorizzazione. Tester, Revisore e Correttore possono essere usati anche su PR manuali interne. Non occorre convertire la PR in Draft e poi Ready per ogni correzione: una nuova modifica rende comunque obsolete le approvazioni precedenti. Se l'aggiornamento del piano non produce un commit, chiedere comunque una nuova review umana sul nuovo ambito. Non avviare più agenti sulla stessa PR contemporaneamente; i run sono serializzati.

Per modifiche al requisito, aggiornare la Issue e richiedere un nuovo piano. Prima della PR si approva con fase:implementazione; se esiste già una PR, un collaboratore Write approva il piano nuovo con il commento AGENTE CORREGGI: seguito da una riga `PIANO APPROVATO: 123456` (sostituire il numero con l'ID del commento del piano, visibile nel link `#issuecomment-...`) e la descrizione della modifica. Il runner verifica che il piano sia quello più recente e aggiorna il riferimento nella PR dopo la pubblicazione. Se il cambiamento è fuori dall'obiettivo originario, creare un nuovo task. Se esiste un branch senza PR perché la creazione automatica è stata negata, aprire manualmente una Draft PR verso main con Closes #N.

Un errore di autenticazione Copilot, di GitHub o di disponibilità delle dipendenze non dimostra un difetto nel codice. Consultare il run in Actions e rilanciare la fase solo dopo aver risolto l'errore. Non usare bypass amministrativi per eludere test o review.

## Sviluppo manuale

È sempre possibile lavorare senza agenti: branch per task, PR collegata alla Issue, CI verde, verifica dei Test Frame e review umana indipendente. Gli agenti restano strumenti di supporto. Per i commit generati, la Git History mostra il bot come autore, Copilot come coautore e il richiedente nel titolo, con responsabili e URL del run nel messaggio. I contributi manuali risultano invece attribuiti ai membri che li hanno realmente effettuati. Per la coautorialità, prima della fase, ciascun assegnatario che ha realmente contribuito pubblica `COAUTORE: implementazione - descrizione del contributo` nella Issue, oppure `COAUTORE: test - descrizione del contributo` o `COAUTORE: correzione - descrizione del contributo` nella PR. Il commento non avvia l'agente; la normale label o il comando avvia la fase. Ogni dichiarazione viene utilizzata una volta nel commit successivo pertinente, con email noreply GitHub. Nessuna attribuzione fittizia. I cambi a dipendenze, configurazione, modelli e workflow sono umani e tracciati.

## Requisiti tecnici

Usare il secret COPILOT_GITHUB_TOKEN già configurato; non aggiungere token Claude o servizi a pagamento. La CI esegue Maven, PostgreSQL e npm; nessun token Copilot è passato al codice applicativo. I workflow agentici utilizzano una versione approvata della configurazione da main, per non richiedere un aggiornamento dei branch solo per eseguire un agente. La CI verifica il commit del branch e, alla review, il merge proposto. Non occorre un nuovo token GitHub.

## Controllo coerenza prima del codice

Il Pianificatore verifica UC, Sequence Diagram, Class Diagram ristrutturato, Category Partition e Test Frame nella pianificazione normale. Il team corregge le incoerenze dei modelli e richiede il piano aggiornato con AGENTE PIANO: prima di applicare fase:implementazione.

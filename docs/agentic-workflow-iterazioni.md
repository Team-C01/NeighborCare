# NeighborCare - Guida operativa

## Flusso normale

1. Un PM o TM con Write crea una Issue usando il template Task per agente, assegna i responsabili e applica `fase:piano`.
2. Il Pianificatore pubblica il piano. Un collaboratore Write lo verifica; se va bene applica `fase:implementazione` (questa label è l'autorizzazione). Non serve un commento aggiuntivo.
3. L'Implementatore pubblica il codice su un branch del task e apre una Draft PR. Il runner verifica l'ambito prima della pubblicazione; la CI verifica il codice.
4. Applicare `fase:test` alla PR. Il Tester indipendente aggiunge o aggiorna i test. Se non servono modifiche ai test, lo dichiara senza produrre commit fittizi.
5. Verificare CI e Test Frame. La CI parte anche dopo un commit dell'agente. Se non parte, usare Actions > CI > Run workflow selezionando il branch della PR.
6. Selezionare Ready for review. Il Revisore AI pubblica rilievi e suggerimenti consultivi, con commit, contesto e stato CI.
7. Una persona con Write non coinvolta nel task verifica i risultati, risolve eventuali rilievi reali e approva la PR. Sono richiesti CI verde, review indipendente, CODEOWNERS. Il merge è manuale.

## Se qualcosa non va

Per ripianificare, l'agente riceve il testo della Issue, l'ultimo piano, la richiesta attuale e la discussione cronologica, entro il limite del contesto disponibile. Non usa soltanto l'ultimo commento.

Usare un commento nella conversazione della Issue o della PR:

| Dove | Commento | Effetto |
| --- | --- | --- |
| Issue | `AGENTE PIANO:` + spiegazione | Nuovo piano |
| PR | `AGENTE CORREGGI:` + problema da risolvere | Correzione sul branch della stessa PR |
| PR | `AGENTE TEST:` | Nuova sessione Tester |
| PR | `AGENTE REVISIONE:` | Nuova revisione consultiva |

Anche rimuovere e riapplicare la label della fase avvia un nuovo run. Non serve una label aggiuntiva, un particolare assegnatario o un commento di autorizzazione. Tester, Revisore e Correttore possono essere usati anche su PR manuali interne. Non occorre convertire la PR in Draft e poi Ready per ogni correzione: una nuova modifica rende comunque obsolete le approvazioni precedenti. Non avviare più agenti sulla stessa PR contemporaneamente; i run sono serializzati.

Per modifiche al requisito, aggiornare la Issue, richiedere un nuovo piano e approvarlo con la label. Se esiste già una PR, continuare sullo stesso branch con AGENTE CORREGGI:, dopo aver condiviso il nuovo piano. Se esiste un branch senza PR perché la creazione automatica è stata negata, aprire manualmente una Draft PR verso main con Closes #N.

Un errore di autenticazione Copilot, di GitHub o di disponibilità delle dipendenze non dimostra un difetto nel codice. Consultare il run in Actions e rilanciare la fase solo dopo aver risolto l'errore. Non usare bypass amministrativi per eludere test o review.

## Sviluppo manuale

È sempre possibile lavorare senza agenti: branch per task, PR collegata alla Issue, CI verde, verifica dei Test Frame e review umana indipendente. Gli agenti restano strumenti di supporto. I cambi a dipendenze, configurazione, modelli e workflow sono umani e tracciati.

## Requisiti tecnici

Usare il secret COPILOT_GITHUB_TOKEN già configurato; non aggiungere token Claude o servizi a pagamento. La CI esegue Maven, PostgreSQL e npm; nessun token Copilot è passato al codice applicativo. I workflow agentici utilizzano una versione approvata della configurazione da main, per non richiedere un aggiornamento dei branch solo per eseguire un agente. La CI usa il codice della PR.

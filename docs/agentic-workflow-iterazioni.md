# NeighborCare - Guida operativa e iterazioni agentiche

## 1. Apertura e pianificazione

**PM e TM con permesso Write possono svolgere gli stessi passaggi operativi.** Uno di loro crea una Issue con il template `Task per agente`, assegna uno o piu collaboratori con Write (anche se stesso) e applica manualmente `fase:piano`. L'assegnazione da sola non avvia il Pianificatore.

Il Pianificatore pubblica il piano senza cambiare il codice. Uno degli assegnatari puo chiedere una modifica sulla Issue con:

```text
RICHIESTA REVISIONE PIANO:
Manca il caso in cui gli intervalli temporali sono consecutivi.
Prevedere la verifica del Test Frame TF_SIM_08.
```

`ripianifica.yml` produce una nuova versione. Quando e corretta, uno qualsiasi degli assegnatari scrive sulla Issue:

```text
AUTORIZZA PIANO: autorizzo l'ultima versione del piano.
```

Non e richiesta la lista dei file autorizzati; l'Implementatore resta vincolato al piano, ai requisiti e alle aree consentite della repository.

## 2. Implementazione e test

Un assegnatario rimuove `fase:piano` e aggiunge `fase:implementazione` alla Issue. L'Implementatore crea un branch e una Draft PR con `Closes #N`, `Autorizzante: @login` e `Responsabili assegnati: @a, @b`, registrando l'elenco iniziale come storico. Gli assegnatari correnti sono quelli della Issue.

Un assegnatario applica `fase:test` alla Draft PR. Il Tester indipendente crea o aggiorna i test dai Test Frame pertinenti e pubblica gli esiti reali. Puo correggere test errati, fragili, incompleti o superati da specifiche approvate, motivandoli; non modifica codice applicativo e non indebolisce le asserzioni. Se la PR riguarda solo documentazione, segnala N/A per test applicativi con motivazione.

## 3. Iterazione della correzione

In caso di test falliti, CI non superata, implementazione incompleta o review negativa, mantenere o riportare la PR allo stato Draft. Un assegnatario o revisore autorizzato con Write puo scrivere:

```text
RICHIESTA CORREZIONE:
TF_SIM_08 fallisce: intervalli consecutivi non devono sovrapporsi.
Atteso: false. Ottenuto: true.
Correggere o reimplementare il metodo senza modificare i test.
```

`correzione.yml` interviene sullo **stesso branch** e sulla **stessa PR**. Puo reimplementare una classe se necessario, ma non cambiare test, RAD/SDD, workflow, segreti o requisiti non pianificati. Dopo il nuovo commit un assegnatario rimuove e riaggiunge `fase:test` sulla PR, eseguendo il retest.

Dopo tre ripianificazioni o correzioni AI consecutive senza test riusciti compare un avviso. Il team puo richiedere ulteriori tentativi manualmente, senza indebolire le verifiche.

### Recupero e cambiamenti durante il task

- Build fallita: se i file rispettano i vincoli, l'Implementatore apre comunque la Draft PR e segnala l'errore; correggere sulla stessa PR.
- Branch automatico pubblicato senza PR: riapplicare `fase:implementazione` per recuperarlo. Se la PR esiste gia, continuare su quella. Se chiusa senza merge, ripristinare il branch se eliminato e riapplicare la label per riaprire la PR; nessuna cancellazione automatica.
- Riassegnazione: portare la PR a Draft, attendere le run attive, aggiornare gli assegnatari della Issue e far scrivere `AUTORIZZA PIANO:` a un assegnatario attuale. Conservare i metadati iniziali della PR. Ripetere Tester, Revisore e review umana; un assegnatario attuale o precedente non puo fare la review indipendente.
- Nuovo piano sulla stessa PR: portarla a Draft, attendere le run attive, rimuovere `fase:implementazione` e applicare `fase:piano` alla Issue. Scrivere `RICHIESTA REVISIONE PIANO:` sulla Issue, attendere il nuovo piano e autorizzarlo. Ripristinare `fase:implementazione` e richiedere `RICHIESTA CORREZIONE:` nella Draft PR per allineare il codice. Ripetere tutte le verifiche e ottenere una nuova review; non usare risultati precedenti alla nuova autorizzazione. Se l'obiettivo cambia completamente, aprire un nuovo task.
- Il Tester e la CI verificano i report reali: almeno un test eseguito per ogni stack inizializzato. Per il frontend `test:ci` deve produrre `frontend/test-results/junit.xml`. Il backend usa i report Surefire/Failsafe. Non vale un test saltato o un report fittizio.

## 4. Revisione iterativa e indipendente

Dopo Tester riuscito, uno degli assegnatari seleziona Ready for review. Il Revisore AI pubblica `ESITO_REVISIONE: PASS` oppure `CHANGES_REQUESTED`.

Se la review AI o umana trova un difetto, riportare la PR a Draft, commentare con `RICHIESTA CORREZIONE:`, ripetere il Tester e poi Ready for review. Ogni nuovo commit richiede una verifica nuova.

Un collaboratore con Write **non incluso tra gli assegnatari** (PM oppure TM) esegue Review changes > Approve dopo aver letto il diff. La review indipendente e richiesta anche quando il task e assegnato a un PM. Non e obbligatorio che il revisore sia un PM.

## 5. Governance e merge

`governance-gate` **non parte all'apertura della PR, all'aggiornamento dei commit o con Ready for review**: prima della review umana, il required check rimane `Expected` e quindi il merge resta bloccato. Il gate parte quando una persona invia una review GitHub `Approve` o `Request changes`, oppure quando una review viene revocata. Per evitare un FAIL prematuro, la review umana `Approve` va inviata **solo dopo** Tester riuscito e Revisore AI con `ESITO_REVISIONE: PASS` sul commit corrente. Il gate confronta Issue e PR, verifica Tester e Revisore sul commit corrente e una review APPROVED da un collaboratore Write non assegnato. Un `Request changes` o una revoca mantiene il blocco; se il codice cambia, sono necessari nuovo Tester, Revisore e una nuova review. Il Ruleset principale richiede inoltre `repository-checks`, una approvazione e Code Owner review.

Il merge e **sempre manuale**: PM e TM con le autorizzazioni necessarie possono integrarlo solo dopo i controlli verdi. Per le simulazioni si arriva al punto precedente al merge, poi si chiude la PR ed elimina il branch di test.

## 6. Recupero

- Piano non partito: verificare Write, Issue `task-agente`, assegnatari e label `fase:piano`.
- Piano errato: `RICHIESTA REVISIONE PIANO:` nella Issue; poi nuova `AUTORIZZA PIANO:`.
- Implementazione errata: `RICHIESTA CORREZIONE:` nella Draft PR e retest.
- Test errato: verificare i Test Frame; il Tester puo correggere il test e motivare la modifica. Per rimuovere o rinominare test obsoleti, il TM interviene manualmente sul branch e motiva il diff. Se cambia la specifica, serve una decisione approvata. Riapplicare `fase:test` anche sullo stesso commit, poi ripetere review; non forzare verde.
- Revisore AI o persona rifiuta: Convert to draft, correzione, retest e nuova review.
- Nuovo commit: ripetere le verifiche e non riutilizzare la review sul vecchio SHA.

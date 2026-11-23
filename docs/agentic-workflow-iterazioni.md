# NeighborCare - Workflow agentico e cicli iterativi

Questa procedura integra `AGENTS.md` e descrive il flusso da Issue a merge. **I PM creano e assegnano i task; il TM assegnato gestisce autonomamente il resto.** Un altro TM revisiona la PR; le modifiche alla governance richiedono anche un PM. Nessun agente fa merge.

## 1. Creazione e assegnazione

1. Un PM (Antonio o Emanuele) apre la Issue con il modulo `Task per agente` e tutti i sette campi, includendo specifiche, ambito e Test Frame.
2. Il PM assegna **esattamente un TM con Write**. L'evento `issues: assigned` attiva `piano.yml`. Non occorre applicare manualmente `fase:piano`.
3. Il Pianificatore analizza il task, pubblica una proposta e il workflow applica `fase:piano`. Se il creatore o chi assegna non è PM, se manca `task-agente` oppure se il TM non è idoneo, il workflow si blocca.
4. Non modificare l'assegnatario dopo aver approvato il piano: la PR congela il login del TM e il gate controlla che coincida con la Issue.

## 2. Iterazione del piano

Il TM confronta la proposta con RAD/SDD, file, metodi e test. Se ha rilievi, lascia **sulla Issue** un commento:

```text
RICHIESTA REVISIONE PIANO:
Verificare il caso alternativo indicato nel Sequence Diagram.
Indicare i Test Frame pertinenti e limitare i file da modificare.
```

`ripianifica.yml` crea una nuova versione. Si può ripetere fino a tre richieste, poi serve intervento umano. Ogni nuova versione invalida le precedenti approvazioni.

Solo il **TM assegnato** può approvare la versione corrente:

```text
APPROVAZIONE TM: approvo il piano corrente per Issue #N.
File autorizzati: backend/src/main/java/.../File.java, frontend/src/.../Page.tsx
```

Indicare solo percorsi esatti, separati da virgole; massimo 12. Non inserire directory generiche, wildcard, test già esistenti, governance o PDF.

## 3. Implementatore e prima prova

1. Il TM rimuove `fase:piano` e aggiunge `fase:implementazione` alla **Issue**.
2. `implementa.yml` verifica l'approvazione TM successiva all'ultimo piano, il suo accesso Write, l'ambito e la presenza di un unico assegnatario.
3. L'Implementatore crea `agent/issue-N-implementazione`, commit e **Draft PR** con `Closes #N` e `TM responsabile: @login`. Non modifica i test e non fa merge.
4. Il TM aggiunge `fase:test` alla **Draft PR**. `test.yml` genera test dalle specifiche e dai Test Frame (non dal comportamento del codice) e pubblica un report con risultato e ID della run.
5. Nei task solo documentali il Tester riporta N/A per i test applicativi, con controlli su diff e CI ugualmente obbligatori.

## 4. Loop del Tester e delle correzioni

Se il Tester fallisce, **non fare Ready for review e non modificare i test per ottenere verde**. Il TM responsabile legge frame, atteso e osservato e commenta sulla Draft PR:

```text
RICHIESTA CORREZIONE:
Il test TF_07 fallisce.
Atteso: una richiesta completata non e annullabile.
Osservato: viene annullata.
Correggere l'implementazione senza cambiare test o requisiti.
```

**Il prefisso esatto e `RICHIESTA CORREZIONE:`.** Possono utilizzarlo il TM assegnato e un altro TM revisore autorizzato (richiesto come reviewer o che abbia espresso CHANGES_REQUESTED). Il workflow verifica l'autore e non accetta richieste anonime o di estranei.

`correzione.yml` aggiorna lo **stesso branch e la stessa PR**, limitandosi ai file approvati; non modifica test, governance o PDF. Il TM rimuove e riaggiunge la label `fase:test` sulla PR e controlla il risultato sul nuovo SHA. Se ancora fallisce, può ripetere. **Dopo tre tentativi falliti, stop e intervento umano.**

Se la specifica o un Test Frame sono errati, il team deve correggere il modello tramite un task separato. Non si possono cambiare requisiti o ampliare l'ambito usando la correzione.

## 5. Loop della revisione

1. Quando il Tester è riuscito, il TM assegnato usa **Ready for review**.
2. `revisione.yml` confronta i cambiamenti con modelli e test e pubblica `ESITO_REVISIONE: PASS` oppure `ESITO_REVISIONE: CHANGES_REQUESTED`. Il Revisore AI non esegue una GitHub review APPROVED.
3. Con errori AI oppure review umana `Request changes`, **Convert to draft**, lascia `RICHIESTA CORREZIONE:` e ripeti correzione, Tester, Ready for review e Revisore AI.
4. Se tutti i controlli sono positivi, un **altro TM** approva tramite **Review changes > Approve**, sul commit corrente. Il TM responsabile non può approvare la propria implementazione, anche se la PR risulta creata dal bot.
5. I file di governance (`.github/`, `AGENTS.md`, `README.md` e questa procedura) richiedono review PM secondo `CODEOWNERS`.

## 6. Governance e merge

Il job `governance-gate` verifica Issue e assegnazione invariata, PR Ready, report Tester riuscito con run conclusa positivamente, Revisore AI riuscito con verdetto PASS, e review umana indipendente sullo SHA corrente. Per il codice serve un altro TM; per i file governance serve anche PM. Il Ruleset `Protect main - NeighborCare` richiede `repository-checks`, `governance-gate`, una review APPROVED e Code Owner review.

È normale che `governance-gate` sia rosso **prima** di Tester, Revisore e review umana. La review umana, svolta dopo i report, scatena una nuova verifica. Se arriva un nuovo commit, ricominciare dal Tester e dalla review sul nuovo SHA.

Il **merge è sempre manuale**, effettuato da un TM o PM autorizzato. La chiusura della Issue collegata e l'aggiornamento della board sono automatici dopo il merge.

**Attività Admin obbligatoria dopo la PR:** disabilitare o adeguare il Ruleset `PM-only merge - NeighborCare`, altrimenti i TM non potranno effettuare il merge nonostante i nuovi workflow. Non rimuovere le protezioni del Ruleset principale.

## 7. Recupero da errori

- Pianificatore assente: verificare PM che apre e assegna, un solo TM con Write, label `task-agente`.
- Implementatore fallito prima del push: verificare i log; solo senza branch/PR esistenti si può riaggiungere `fase:implementazione`.
- Branch creato senza PR: recuperare manualmente la Draft PR sul branch esistente, non ricreare il branch.
- Tester fallito: Draft, commento di correzione, retest, nessun merge.
- Revisore o Code Owner non approva: Convert to draft e nuova iterazione completa.
- Dopo tre tentativi: conservare log e SHA e passare a revisione manuale del team.
- Gli eventi GitHub generati mediante `GITHUB_TOKEN` non riattivano sempre altri workflow; per retest usare una label applicata da una persona, per revisione l'evento Ready for review.

## 8. Tracciabilita e responsabilita

Conservare commenti di approvazione, versione del piano, report, test frame, SHA e review umane. I PDF originali RAD/SDD non vanno alterati e gli esempi XX/YY non sono requisiti da implementare. CI e agenti supportano il team ma non sostituiscono responsabilità e verifica umana.

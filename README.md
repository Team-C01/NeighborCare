# NeighborCare — Team C01

Progetto universitario di Ingegneria del Software e Gestione dei Progetti Software, Università di Salerno. Piattaforma di vicinato per commissioni non sanitarie.

## Struttura

- [frontend/](frontend/) e [backend/](backend/): cartelle per il futuro codice, contenenti solo `.gitkeep`.
- [docs/README.md](docs/README.md): PDF, UC, diagrammi, Category Partition e Test Frame. Conservare tutti gli esempi XX/YY per i ragazzi; non sono requisiti da implementare.
- [AGENTS.md](AGENTS.md): contesto, stack, comandi disponibili e regole comuni.
- [.github/agents/](.github/agents/): quattro profili Copilot dedicati a Pianificatore, Implementatore, Tester e Revisore.
- [.github/ISSUE_TEMPLATE/task-agente.yml](.github/ISSUE_TEMPLATE/task-agente.yml), [template PR](.github/pull_request_template.md) e [CODEOWNERS](.github/CODEOWNERS): task, tracciabilità e responsabilità.

I workflow seguono i passi 7, 9, 10, 11 e 14 del tutorial, usando Copilot CLI al posto dell'action Claude. Non sono presenti script Python versionati: i controlli deterministici di approvazioni, ambito, output e test restano nei workflow. Le istruzioni specifiche dei quattro ruoli sono nei rispettivi file `.agent.md`, letti esplicitamente dai workflow insieme ad `AGENTS.md`; i workflow mantengono trigger, autorizzazioni e limiti tecnici.

## Flusso di lavoro

1. **PM** apre una Issue usando il template `Task per agente` e assegna un solo **TM responsabile**. L'assegnazione del PM attiva `piano.yml`, che genera il piano e applica `fase:piano`.
2. **TM assegnato** controlla il piano. Può richiedere revisioni scrivendo sulla Issue `RICHIESTA REVISIONE PIANO:`; `ripianifica.yml` pubblica una nuova versione. Quando il piano è corretto, il TM commenta con due righe distinte `APPROVAZIONE TM:` e `File autorizzati:` (massimo 12 percorsi esatti).
3. Il **TM assegnato** rimuove `fase:piano` e aggiunge `fase:implementazione` sulla Issue. `implementa.yml` verifica il TM e l'approvazione successiva all'ultimo piano, modifica soltanto i file autorizzati e crea una Draft PR collegata tramite `Closes #N`, registrando il TM responsabile.
4. Il TM applica `fase:test` sulla **Draft PR**. Il Tester crea test indipendenti dai Test Frame reali (per i task documentali riporta N/A motivato). La CI verifica i controlli effettivamente disponibili.
5. Se emergono errori, il TM assegnato o un TM revisore autorizzato scrive sulla Draft PR **`RICHIESTA CORREZIONE:`**, seguito da atteso, osservato e riferimento al difetto. `correzione.yml` corregge lo stesso branch, entro i file approvati e senza toccare i test. Il TM rimuove e riaggiunge `fase:test` per il retest. Dopo tre tentativi falliti, interviene una persona.
6. Dopo un Tester riuscito il TM sceglie **Ready for review**. Il Revisore AI confronta diff e modelli, pubblica `ESITO_REVISIONE: PASS` oppure `CHANGES_REQUESTED`. Se trova difetti, si torna a Draft e al ciclo di correzione e retest.
7. **Un altro TM** (Code Owner) effettua la review umana e approva il commit corrente. Le modifiche alla governance richiedono anche una review PM. Il TM responsabile non può autoapprovare il proprio lavoro, neanche se la PR è stata creata da un bot.
8. **TM o PM autorizzato** può effettuare manualmente il merge solo dopo `repository-checks`, `governance-gate`, Tester, Revisore AI e review Code Owner positivi. GitHub chiude la Issue collegata e aggiorna la board.

## Approvazioni e configurazione GitHub

Esempio del commento del **TM assegnato** nella Issue dopo l'ultimo piano:

```text
APPROVAZIONE TM: approvo il piano corrente per Issue #N.
File autorizzati: backend/src/main/java/.../File.java
```

Il prefisso della correzione è soltanto **`RICHIESTA CORREZIONE:`**; il workflow verifica l'autore del commento, che deve essere un TM responsabile o revisore autorizzato. Non sono consentiti cambiamenti di requisiti o file fuori dall'ambito senza nuova pianificazione.

`governance-gate` può essere rosso finché mancano report, review o controlli; viene rieseguito dopo la review umana. La CI verde prima del bootstrap dei moduli non prova il funzionamento applicativo.

**Intervento amministrativo ancora necessario:** il Ruleset attivo `PM-only merge - NeighborCare` impedisce il merge ai TM. È necessario disabilitarlo o adattarlo, mantenendo invece obbligatori tutti i controlli del Ruleset `Protect main - NeighborCare`. I workflow YAML non possono modificare questa impostazione.

## CI e prerequisiti

[ci.yml](.github/workflows/ci.yml) parte sulle PR verso main e controlla il diff, la sintassi YAML e i collegamenti Markdown locali. Quando compaiono manifest approvati, esegue `mvn -B verify` e i comandi npm di build/test. Il job obbligatorio mantiene il nome `repository-checks` e non chiama modelli.

Frontend e backend non sono inizializzati: nessuna build o esecuzione di test applicativi viene simulata. Il bootstrap approvato dovrà inserire `backend/pom.xml`, `backend/.java-version`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/.nvmrc` e script npm `build` e `test:ci` approvati dal team (il comando `test:ci` deve terminare senza watch mode). Fino ad allora una CI verde certifica la governance, non il funzionamento dell'applicazione.

Il PM verifica in GitHub: accessi Write, label `task-agente`, `fase:piano`, `fase:implementazione`, `fase:test`, secret `COPILOT_GITHUB_TOKEN`, permessi per creare PR e Ruleset che richieda 1 approvazione umana, Code Owner review e lo status check `repository-checks`. Per riconoscere il secondo PM che apre e assegna le Issue impostare la variabile repository `NEIGHBORCARE_SECOND_PM_LOGIN` con il suo login GitHub verificato. Non abilitare API AI esterne o spesa extra; verificare idoneità e quote Copilot/Actions. Le PR del bot possono richiedere un'azione umana per avviare altri workflow.

Per approvare un piano, il TM assegnato usa `APPROVAZIONE TM:` e `File autorizzati:` dopo l'ultima versione pubblicata.

Le modifiche alla pipeline vanno provate con un task documentale approvato prima di dichiarare funzionante il flusso completo. I PDF RAD/SDD restano fonti originali: non copiarne pagine in file Markdown. Questa semplificazione non esegue chiamate AI e non modifica PDF o template didattici.

Per piani respinti, test falliti e revisioni con rilievi, seguire la [procedura di iterazione e recupero](docs/agentic-workflow-iterazioni.md). Il PM autorizza esplicitamente ogni correzione sulla Draft PR; non indebolire i test per ottenere una CI verde.

## Glossario

- **PM** — Project Manager
- **TM** — Team Member
- **RAD** — Requirements Analysis Document
- **SDD** — System Design Document
- **PR** — Pull Request
- **CI** — Continuous Integration

## Verifica workflow agentico

Questa sezione è stata aggiunta per verificare il workflow agentico del Team C01.

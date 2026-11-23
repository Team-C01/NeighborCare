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

1. **PM:** apre una Issue con il modulo Task per agente, aggiunge `task-agente`, assegna **uno o piu TM** e applica manualmente `fase:piano`. L'assegnazione da sola non avvia nulla.
2. **Pianificatore:** pubblica il piano sulla Issue. I TM assegnati possono richiedere ripianificazione con `RICHIESTA REVISIONE PIANO:`. Un assegnatario autorizza l'ultima versione con `AUTORIZZA PIANO:` e `File autorizzati:`.
3. **Implementatore:** un TM assegnato rimuove `fase:piano` e applica `fase:implementazione` sulla Issue. Il workflow verifica l'autorizzazione e genera branch e Draft PR con `Closes #N` e elenco dei TM assegnati.
4. **Tester:** un TM assegnato aggiunge `fase:test` sulla Draft PR; il Tester genera ed esegue test dai Test Frame indipendenti dal codice. Task documentale: test applicativi N/A motivati.
5. **Correzioni/reimplementazione:** con bug o implementazione inadeguata, un TM assegnato o revisore autorizzato scrive `RICHIESTA CORREZIONE:` sulla PR Draft. La Correzione AI puo reimplementare i metodi/classi nei soli file autorizzati e pubblica un nuovo commit sulla stessa PR. Il TM rimuove e riaggiunge `fase:test`.
6. **Revisore:** dopo test positivi il TM seleziona Ready for review. Il Revisore AI pubblica `ESITO_REVISIONE: PASS` oppure `CHANGES_REQUESTED`. Se il lavoro non va bene: Convert to draft, correzione o reimplementazione, nuovo Tester e nuova review.
7. **Review umana:** un collaboratore Write non assegnato alla Issue (TM o PM) approva il commit corrente. **Nessuna review PM obbligatoria**, anche per file di governance.
8. **Merge:** TM o PM autorizzato, manualmente, dopo `repository-checks`, `governance-gate` e Code Owner review positivi. Poi GitHub chiude la Issue collegata e aggiorna la board.

## Commenti esatti

Sulla Issue, dopo l'ultimo piano:

```text
AUTORIZZA PIANO: autorizzo l'ultima versione del piano.
File autorizzati: percorso/esatto/Service.java
```

Sulla Draft PR per un bug oppure una reimplementazione:

```text
RICHIESTA CORREZIONE:
Atteso: ...
Osservato: ...
Reimplementare il metodo nei file autorizzati senza modificare i test.
```

Se servono nuovi file o requisiti, non usare il ciclo di correzione: creare un nuovo task. Per far effettuare merge ai TM occorre adattare il Ruleset `PM-only merge - NeighborCare`, mantenendo attivo `Protect main - NeighborCare`.

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

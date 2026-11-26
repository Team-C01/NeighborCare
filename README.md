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

1. **PM o TM con Write** apre una Issue con il template Task per agente, assegna uno o piu collaboratori con Write (anche se stesso) e applica **manualmente** la label `fase:piano`. La sola assegnazione non avvia alcun piano.
2. **Pianificatore AI** pubblica il piano. Uno degli assegnatari (PM o TM) puo chiedere una nuova versione tramite `RICHIESTA REVISIONE PIANO:` o autorizzare l'ultima versione tramite `AUTORIZZA PIANO:`. Non serve una lista di file.
3. **Implementatore AI:** un assegnatario sostituisce `fase:piano` con `fase:implementazione` sulla Issue. Il workflow crea branch e Draft PR collegata con `Closes #N`, `Autorizzante:` e `Responsabili assegnati:`. Il corpo della PR segue sezioni fisse per modifiche reali, modelli/riferimenti, verifiche eseguite, rischi e limiti, senza inventare risultati non disponibili.
4. **Tester AI:** un assegnatario aggiunge `fase:test` alla Draft PR. Il Tester crea o aggiorna test indipendenti dai Test Frame, senza modificare il codice applicativo. I test esistenti possono essere corretti con motivazione e senza indebolire gli esiti attesi. Per task solo documentali indica N/A motivato.
5. **Correzioni e reimplementazioni:** un assegnatario o revisore autorizzato scrive `RICHIESTA CORREZIONE:` sulla Draft PR. L'agente corregge sullo stesso branch e nell'ambito approvato, senza modificare test e documentazione protetta. Un assegnatario toglie e riapplica `fase:test` per ripetere i controlli.
6. **Revisore AI:** dopo test riusciti l'assegnatario seleziona Ready for review. Il Revisore pubblica `ESITO_REVISIONE: PASS` o `CHANGES_REQUESTED`. Con errori: Convert to draft, correzione, nuovo Tester e nuova review.
7. **Review umana:** **solo dopo** il report Tester riuscito e il report Revisore AI con `ESITO_REVISIONE: PASS`, una persona con Write (PM o TM) **non assegnata al task** esegue Review changes > Approve sul commit corrente. Questo evento fa partire `governance-gate`. Prima della review il required check resta `Expected`, non `FAIL` e non `SUCCESS`; il merge e bloccato. Non si puo approvare il proprio task anche se il bot ha creato la PR.
8. **Merge:** un PM o TM autorizzato esegue manualmente il merge solo con `repository-checks`, `governance-gate`, Tester, Revisore e Code Owner review positivi. Non usare auto-merge.

## Commenti esatti

Sulla Issue, dopo l'ultimo piano:

```text
AUTORIZZA PIANO: autorizzo l'ultima versione del piano.
```

Sulla Draft PR se il codice e errato o va reimplementato:

```text
RICHIESTA CORREZIONE:
Atteso: ...
Osservato: ...
Correggere o reimplementare nel piano approvato senza alterare i test.
```

Un PM puo essere sia chi apre la Issue sia uno degli assegnatari; per una review indipendente deve intervenire un'altra persona **non assegnata**. Conservare i controlli del Ruleset `Protect main - NeighborCare`.

## CI e prerequisiti

[ci.yml](.github/workflows/ci.yml) parte sulle PR verso main e controlla il diff, la sintassi YAML e i collegamenti Markdown locali. Quando compaiono manifest approvati, esegue `mvn -B verify` e i comandi npm di build/test. Il job obbligatorio mantiene il nome `repository-checks` e non chiama modelli.

Implementatore e Correttore possono usare solo i comandi tecnici npm/Maven autorizzati nei workflow per compilare, eseguire i test e correggere il codice; il Tester puo installare da lockfile ed eseguire verifiche, senza modificare il codice applicativo. Pianificatore e Revisore non hanno accesso alla shell. GitHub Actions ripete sempre i controlli indipendenti e gestisce commit, push e PR. Implementatore e Correttore possono eliminare o rinominare soltanto file applicativi obsoleti in backend/ e frontend/, entro il piano autorizzato e con motivazione nel report. Test, manifest, lockfile, file versione, Dockerfile, Compose, .gitkeep, documenti e governance restano protetti dalla rimozione; il Tester non puo eliminare file versionati. I TM possono aggiornare o rimuovere manualmente test obsoleti con motivazione in PR; ripetere `fase:test`, CI e review. Rimuovere e riapplicare `fase:test` consente di ripetere anche una verifica fallita sullo stesso commit.

Frontend e backend non sono inizializzati: nessuna build o esecuzione di test applicativi viene simulata. Il bootstrap approvato dovrà inserire `backend/pom.xml`, `backend/.java-version`, `frontend/package.json`, `frontend/package-lock.json`, `frontend/.nvmrc` e script npm `build` e `test:ci` approvati dal team (il comando `test:ci` deve terminare senza watch mode). Fino ad allora una CI verde certifica la governance, non il funzionamento dell'applicazione.

PM o TM verifica in GitHub: accessi Write, label `task-agente`, `fase:piano`, `fase:implementazione`, `fase:test`, secret `COPILOT_GITHUB_TOKEN`, permessi per creare PR e Ruleset che richieda 1 approvazione umana, Code Owner review e lo status check `repository-checks`. Non serve alcuna variabile `NEIGHBORCARE_SECOND_PM_LOGIN`: le autorizzazioni di PM e TM sono determinate dinamicamente dai permessi GitHub (Write/Maintain/Admin) e dagli assegnatari effettivi della Issue. Le review devono essere effettuate da collaboratori indipendenti, non assegnati al task. Non abilitare API AI esterne o spesa extra; verificare idoneità e quote Copilot/Actions. Le PR del bot possono richiedere un'azione umana per avviare altri workflow.

Per autorizzare un piano, uno degli assegnatari usa `AUTORIZZA PIANO:` dopo l'ultima versione pubblicata, senza lista di percorsi.

Le modifiche alla pipeline vanno provate con un task documentale approvato prima di dichiarare funzionante il flusso completo. I PDF RAD/SDD restano fonti originali: non copiarne pagine in file Markdown. La CI deterministica (`ci.yml`) non effettua chiamate AI: controlla YAML, link, diff e, quando esistono i manifest, build e test applicativi. I workflow agentici (Pianificatore, Ripianificazione, Implementatore, Tester, Correzione e Revisore) invocano invece Copilot CLI usando il secret `COPILOT_GITHUB_TOKEN`. Nessun workflow deve modificare i PDF RAD/SDD o gli esempi didattici.

Per piani respinti, test falliti e revisioni con rilievi, seguire la [procedura di iterazione e recupero](docs/agentic-workflow-iterazioni.md). Uno dei TM assegnati o un revisore autorizzato puo richiedere la correzione o reimplementazione con `RICHIESTA CORREZIONE:` sulla Draft PR; non indebolire i test per ottenere una CI verde.

## Glossario

- **PM** — Project Manager
- **TM** — Team Member
- **RAD** — Requirements Analysis Document
- **SDD** — System Design Document
- **PR** — Pull Request
- **CI** — Continuous Integration

## Verifica workflow agentico

Questa sezione è stata aggiunta per verificare il workflow agentico del Team C01.

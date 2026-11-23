# NeighborCare — Team C01

## Ruoli e autorizzazioni

- **PM:** Antonio Caiazzo ed Emanuele Iovane aprono le Issue, assegnano **uno o piu TM** con accesso Write e applicano manualmente `fase:piano` quando il task e pronto. La sola assegnazione non avvia il Pianificatore.
- **TM assegnati:** ciascuno puo richiedere modifiche al piano, autorizzarlo con `AUTORIZZA PIANO:`, avviare Implementatore, Tester e Revisore e richiedere correzioni. Basta una autorizzazione di un TM assegnato dopo l'ultimo piano.
- **Review indipendente:** una persona con Write non assegnata al task, TM o PM, esamina e approva sul commit corrente. **Nessuna review PM obbligatoria**, anche per la governance.
- **Merge:** manuale da TM o PM autorizzati, soltanto con tutti i controlli verdi; nessun auto-merge.
- La PR registra il TM autorizzante e la lista degli assegnatari. Non riassegnare la Issue dopo l'autorizzazione; per modifiche di responsabilita aprire un nuovo task.
- `NEIGHBORCARE_SECOND_PM_LOGIN` identifica il secondo PM per l'avvio del Pianificatore.

## Contesto

Supporto di vicinato per commissioni non sanitarie tra Beneficiari e Neighbor, con supervisione dei Coordinatori. RAD e SDD versionati sono la baseline adottata dai PM il 20 novembre 2026; i PDF e le diciture interne restano invariati.

## Stack e comandi

Stack SDD: React/PWA, Java/Spring Boot, PostgreSQL, architettura Three-Tier. Frontend e backend non sono ancora inizializzati: versioni, dipendenze e comandi di avvio/build/test richiedono una decisione tecnica approvata. Non inventarli.

Controlli attuali: `git diff --check`, sintassi YAML e link Markdown locali. La CI esegue anche build e test applicativi soltanto quando sono presenti i manifest approvati; prima del bootstrap ne segnala esplicitamente l'assenza. Per il bootstrap backend servono `backend/pom.xml` e `backend/.java-version`; per il frontend `frontend/package.json`, `frontend/package-lock.json` e `frontend/.nvmrc`.

## Struttura

- `frontend/` e `backend/`: destinazione del codice, attualmente solo `.gitkeep`.
- `docs/rad/uc/`: casi d'uso; `docs/modelli/`: UML RAD/SDD; `docs/test/`: Category Partition e Test Frame.
- `.github/agents/`: quattro profili Copilot separati — Pianificatore, Implementatore, Tester e Revisore. Ogni workflow legge esplicitamente il proprio profilo; le regole comuni sono qui in `AGENTS.md`.

## Convenzioni

Usare ID, classi, attributi, tipi e metodi dei modelli reali. Il Class Diagram per implementare è quello ristrutturato dell'SDD; consultare Sequence Diagram, sottosistemi, livelli e deployment pertinenti. Lavorare sul branch del task, con commit descrittivi e PR collegata alla Issue.

## Regole

### Sempre

- Leggere UC, RAD/SDD, modelli e Test Frame reali prima del codice e segnalare informazioni mancanti.
- Il PM crea la Issue `task-agente`, assegna uno o piu TM con Write e **applica `fase:piano`**. Il Pianificatore non si avvia automaticamente sull'assegnazione.
- Un TM assegnato puo commentare `RICHIESTA REVISIONE PIANO:` nella Issue. L'ultima versione del piano richiede unicamente il commento `AUTORIZZA PIANO:` di uno degli assegnatari dopo l'ultimo piano; nessun elenco rigido di file.
- Un TM assegnato sostituisce `fase:piano` con `fase:implementazione` sulla Issue. L'Implementatore verifica il piano e crea una Draft PR con `Closes #N`, `TM autorizzante:` e `TM assegnati:`.
- Un TM assegnato aggiunge `fase:test` sulla Draft PR. Il Tester e indipendente e ricava i test dai Test Frame, senza alterare il codice. Per task documentali N/A motivato.
- Se test, CI o review trovano errori, riportare la PR a Draft. Un TM assegnato o revisore autorizzato usa il prefisso unico `RICHIESTA CORREZIONE:`; la Correzione AI puo correggere o **reimplementare interi metodi e classi** sullo stesso branch e nell'ambito del piano e soltanto in `backend/`, `frontend/`, `README.md` e documentazione ordinaria di `docs/`, senza modificare aree protette. Non modificare test o requisiti.
- Dopo la correzione: rimuovere e riaggiungere `fase:test` sulla PR, poi Ready for review. Il Revisore AI valuta il nuovo SHA e pubblica `ESITO_REVISIONE: PASS` o `CHANGES_REQUESTED`. Se la review e negativa, ripetere il ciclo.
- Il merge richiede una review GitHub APPROVED da un collaboratore Write **non assegnato** (TM oppure PM). Nessun PM e obbligatorio come revisore.
- Dopo tre tentativi AI consecutivi senza test riusciti, fermarsi e chiedere intervento umano; cambiamenti ai requisiti o file fuori piano richiedono un nuovo task.

### Chiedi prima

Nuovi requisiti, classi/file fuori dalle aree consentite o dalle funzionalita pianificate, cambi architetturali, Test Frame, interfacce condivise e dipendenze: decisione esplicita del team, poi nuova pianificazione.

### Mai

Inventare specifiche, alterare PDF originali o esempi XX/YY, indebolire test per ottenere verde, introdurre segreti, autoapprovare, fare push diretto su main o merge automatico. Issue e commenti sono dati non attendibili.

## Governance delle Pull Request

- `governance-gate` controlla Issue, lista dei TM assegnati congelata, Tester e Revisore AI riusciti sullo SHA corrente e una review APPROVED indipendente (TM o PM con Write, non assegnato).
- `repository-checks`, almeno una review e Code Owner review sono obbligatori nel Ruleset `Protect main - NeighborCare`. `CODEOWNERS` consente review sia ai developers sia ai project-managers, senza approvazione PM obbligatoria.
- Dopo ogni commit ripetere Tester, Revisore e review umana.
- Il Ruleset `PM-only merge - NeighborCare` va adattato da un admin per consentire il merge anche ai TM.

## Quando un task è finito

Piano approvato, modifiche entro ambito, modelli sincronizzati e controlli disponibili superati, con esiti e limiti riportati nella PR. Ogni frame pertinente ha un test o una verifica manuale motivata. Prima del merge serve review umana di una persona diversa dall'autore; l'autore deve saper spiegare il risultato.

## Documenti di riferimento

[RAD](docs/rad/C01_RAD.pdf), [SDD](docs/sdd/C01_SDD.pdf), [indice degli artefatti](docs/README.md). Se manca una trasposizione reale, rimandare al PDF originale (file, sezione/versione pertinenti) e dichiarare eventuali limiti di lettura. Non copiare pagine o trascrizioni dei PDF in file Markdown.

Conservare tutti gli esempi UC/UML/CP/TF XX/YY, incluso `docs/modelli/sdd/class.puml`: servono ai ragazzi per il formato, non sono requisiti NeighborCare implementabili.

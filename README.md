# NeighborCare — Team C01

Progetto universitario di Ingegneria del Software e Gestione dei Progetti Software, Università di Salerno. Piattaforma di vicinato per commissioni non sanitarie.

## Struttura

- [frontend/](frontend/) e [backend/](backend/): bootstrap tecnico minimo per React/PWA e Spring Boot, oltre ai file `.gitkeep`.
- [docs/README.md](docs/README.md): PDF, UC, diagrammi, Category Partition e Test Frame. Conservare tutti gli esempi XX/YY per i ragazzi; non sono requisiti da implementare.
- [AGENTS.md](AGENTS.md): contesto, stack, comandi disponibili e regole comuni.
- [.github/agents/](.github/agents/): quattro profili Copilot dedicati a Pianificatore, Implementatore, Tester e Revisore.
- [.github/ISSUE_TEMPLATE/task-agente.yml](.github/ISSUE_TEMPLATE/task-agente.yml), [template PR](.github/pull_request_template.md) e [CODEOWNERS](.github/CODEOWNERS): task, tracciabilità e responsabilità.

I workflow agentici usano Copilot CLI con un runner condiviso: preparazione del contesto, generazione della patch e pubblicazione separata. La CI è indipendente dall'AI: parte sui push manuali (anche main), dopo ogni commit agente e alla review umana finale. I commit AI riportano il richiedente effettivo, i responsabili e il run; le PR ereditano gli assegnatari della Issue. Il bot resta autore dei commit AI e Copilot compare come coautore; l'assegnatario che avvia una fase di modifica dopo aver contribuito al task compare automaticamente come coautore GitHub, senza commenti aggiuntivi; gli altri assegnatari restano responsabili del task. La CI aggiorna un unico commento riepilogativo sulla PR.

## Avvio locale (bootstrap)

Il frontend usa Node.js `26.13.1` (vedi [frontend/.nvmrc](frontend/.nvmrc)); il backend usa Java `25` e Maven. Per installare le dipendenze frontend dal lockfile versionato:

```sh
npm --prefix frontend ci
```

Il frontend usa React `19.3.1`, Vite `7.3.8` e Vitest `5.1.2` con jsdom per i test UI. Il backend usa Spring Boot `4.2.0` con WebMVC, Actuator, JDBC e driver PostgreSQL; le credenziali DB sono configurabili tramite `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` e `DB_PASSWORD`.

In due terminali, eseguire `npm --prefix frontend run dev` e `mvn -f backend/pom.xml spring-boot:run`. Il frontend è disponibile su <http://localhost:5173>, il backend su <http://localhost:8080> e la verifica tecnica di salute su <http://localhost:8080/actuator/health>. Avviando il backend al di fuori di Compose, PostgreSQL deve essere raggiungibile su `localhost:5432`.

Per avviare i tre servizi con Docker Compose, dalla radice del repository eseguire:

```sh
mvn -B -f backend/pom.xml verify
docker compose -f backend/compose.yaml up --build
```

Compose espone frontend e backend rispettivamente sulle porte `5173` e `8080`; PostgreSQL è pubblicato solo su localhost alla porta `5432`. Il database usa il volume persistente `neighborcare-postgres`. Le credenziali dimostrative `neighborcare` / `neighborcare_local` sono esclusivamente per lo sviluppo locale: non riutilizzarle né considerarle segreti adatti a un ambiente condiviso o di produzione. Fermare i servizi con `docker compose -f backend/compose.yaml down`; per mantenere i dati non rimuovere il volume.

Il manifest web rende l'app installabile nei browser compatibili, ma non è configurato un service worker, caching o supporto offline. Il bootstrap comprende smoke test frontend e backend e un test di integrazione PostgreSQL, creati nella fase di testing indipendente. Eseguire `npm --prefix frontend run build`, `npm --prefix frontend run test:ci` e `mvn -B -f backend/pom.xml verify`; `test:ci` produce `frontend/test-results/junit.xml` e fallisce se non sono presenti test. Per verificare anche PostgreSQL avviare il servizio con `docker compose -f backend/compose.yaml up -d --wait database`, quindi eseguire `mvn -B -f backend/pom.xml clean verify -Dneighborcare.integration.database=true`. Il test di integrazione viene saltato quando la proprietà non è attiva.

## Flusso di lavoro

1. Creare una Issue e assegnare i responsabili; applicare `fase:piano`.
2. Leggere il piano; applicare `fase:implementazione` per approvarlo.
3. L'Implementatore crea la Draft PR; applicare `fase:test` per il Tester indipendente, che genera i test, avvia la CI e attende il risultato effettivo prima di pubblicare l'esito finale.
4. Controllare il riepilogo CI e il collaudo; selezionare Ready for review per la prima revisione AI. Il Revisore si avvia anche all'apertura di una PR direttamente Ready e dopo nuovi commit su una PR Ready.
5. Review umana indipendente; l'approvazione avvia la CI finale sulla PR. Merge manuale soltanto dopo il check obbligatorio verde.

In caso di problemi usare `AGENTE PIANO:` sulla Issue, `AGENTE CORREGGI:` o `AGENTE TEST:` nella PR. Vedi la [guida operativa](docs/agentic-workflow-iterazioni.md).

## Configurazione

- [.github/workflows/esegui-fase.yml](.github/workflows/esegui-fase.yml): workflow riutilizzabile per i quattro ruoli.
- [.github/scripts/agent_workflow.py](.github/scripts/agent_workflow.py): preparazione, validazione e pubblicazione delle modifiche.
- [.github/scripts/verify-project.sh](.github/scripts/verify-project.sh): comandi di verifica della CI.
- [.github/workflows/ci.yml](.github/workflows/ci.yml): controlli automatici, Maven, PostgreSQL, npm, test e audit; nessuna chiamata AI.
- Secret richiesto: `COPILOT_GITHUB_TOKEN`. Nessun token Claude, nessun servizio aggiuntivo.
- Protezioni main: review indipendente e repository-checks; CODEOWNERS indica i reviewer. Mai push diretto o merge automatico.

Lo sviluppo manuale è supportato con branch, PR, test e review. Il report AI aiuta il team, ma non sostituisce le verifiche o la responsabilità dei revisori.

## SonarQube Cloud (opzionale fino al setup)

Importare la repository pubblica in SonarQube Cloud e scegliere un piano gratuito compatibile. Impostare in Settings > Secrets and variables > Actions le variabili `SONAR_PROJECT_KEY`, `SONAR_ORGANIZATION` e il secret `SONAR_TOKEN`. Disattivare Automatic Analysis nel progetto Sonar per evitare doppie analisi. La CI analizza Java e React su main e sulle PR interne verso main; senza le variabili il controllo viene saltato. La prima analisi deve stabilire la baseline di main. Sonar riporta il Quality Gate nel proprio dashboard: rimane consultivo (non è un check obbligatorio). La CI produce JaCoCo XML per Java e LCOV tramite Vitest V8 per React, e Sonar li importa; la soglia del Quality Gate non viene abbassata. Il report JUnit contiene gli esiti, non la copertura del codice.

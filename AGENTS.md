# NeighborCare — Team C01

## Ruoli e autorizzazioni

- PM e TM con Write possono aprire Issue, assegnare responsabili e avviare gli agenti. La label `fase:implementazione` applicata dopo il piano costituisce autorizzazione esplicita.
- Il Tester ha un contesto indipendente e genera test dalla specifica; l'Implementatore non modifica test. Il Revisore AI è consultivo, non può approvare una PR.
- Una persona Write diversa dall'autore e dai responsabili del task esamina e approva il commit corrente. Il merge è manuale, con CI positiva e review indipendente. Mai push diretto su main o auto-merge.

## Contesto

Supporto di vicinato per commissioni non sanitarie tra Beneficiari e Neighbor, con supervisione dei Coordinatori. RAD e SDD versionati sono la baseline adottata dai PM il 20 novembre 2026; i PDF e le diciture interne restano invariati.

## Stack e comandi

Stack SDD: React/PWA, Java/Spring Boot, PostgreSQL, architettura Three-Tier. Usare le versioni fissate dai manifest e le dipendenze già approvate. Nuove dipendenze, manifest e configurazioni richiedono una modifica umana tracciata.

Controlli: `git diff --check`, sintassi YAML e link Markdown locali, test degli script del workflow, Maven, test di integrazione con PostgreSQL, installazione riproducibile npm, build frontend, test frontend e audit npm high/critical. Usare i manifest e le versioni presenti; non dichiarare verifiche non svolte.

## Struttura

- `frontend/` e `backend/`: destinazione del codice, con il bootstrap tecnico e il codice del progetto.
- `docs/rad/uc/`: casi d'uso; `docs/modelli/`: UML RAD/SDD; `docs/test/`: Category Partition e Test Frame.
- `.github/agents/`: quattro profili Copilot separati — Pianificatore, Implementatore, Tester e Revisore. Il runner include nel prompt il profilo e il testo approvato di `AGENTS.md`; non serve rileggere questo file con Copilot.

## Convenzioni

Usare ID, classi, attributi, tipi e metodi dei modelli reali. Il Class Diagram per implementare è quello ristrutturato dell'SDD; consultare Sequence Diagram, sottosistemi, livelli e deployment pertinenti. Lavorare sul branch del task, con commit descrittivi e PR collegata alla Issue.

### Convenzioni di naming comuni

- Usare i termini di dominio italiani del RAD/SDD (es. `Richiesta`, `Beneficiario`, `Neighbor`, `Comunita`). Conservare esattamente nomi, ID, firme e contratti gia definiti nei modelli approvati. Gli esempi qui sotto illustrano il naming, non autorizzano nuove classi o operazioni.
- Package Java e cartelle dei sottosistemi React: minuscolo, senza spazi, accenti o caratteri speciali; per piu parole usare snake_case (es. `gestione_richieste`).
- Classi, interfacce ed enum Java: PascalCase (es. `Richiesta`, `RichiestaService`). Metodi, attributi, parametri e variabili: camelCase (es. `creaRichiesta()`, `ottieniChat()`, `dataConsegna`). Preferire nomi descrittivi; abbreviazioni come `i` solo in contesti locali semplici. Costanti: UPPER_SNAKE_CASE.
- Evitare sinonimi, traduzioni arbitrarie e suffissi ridondanti. Usare suffissi tecnici in inglese in modo uniforme; se un nome e gia definito nel modello approvato, non rinominarlo senza decisione del team.

### Backend Java / Spring Boot

- Package radice: `it.unisa.neighborcare`. Organizzare i sottosistemi sotto `sottosistemi`, ciascuno con `controller` per gli endpoint HTTP Spring e `service` per la logica applicativa. Non usare Servlet personalizzate o JSP per la presentazione React.
- Controller HTTP: PascalCase con suffisso `Controller` (es. `RichiestaController`); delegano la logica ai servizi, senza interrogare direttamente il database. Non confondere i controller HTTP con gli oggetti Control del modello: mantenere responsabilita e contratti modellati.
- Servizi: PascalCase con suffisso `Service`. Rispettare le interfacce e operazioni della sezione 3.2.2 dell'SDD, ad esempio `RegistrazioneService`, `LoginService`, `NeighborService`, `ComunitaService`, `BeneficiarioService`, `RichiestaService`, `MessaggioService`, `ChatService`, `IAService`, `NotificaService`. Se serve una classe concreta distinta dall'interfaccia, usare un nome coerente (es. `RichiestaServiceImpl`); non duplicare interfacce o servizi inutilmente.
- Entita: PascalCase, in `model/entity`; usare l'Entity Class Diagram SDD per le entita persistenti, senza reintrodurre automaticamente le classi escluse dal prototipo. Le classi Control e le altre classi non persistenti seguono il RAD/SDD e appartengono alla logica applicativa.
- Accesso ai dati: in `model/dao`, classi/interfacce PascalCase con suffisso `DAO` (es. `RichiestaDAO`). Se il team approva Spring Data, usare invece `model/repository` e suffisso `Repository` (es. `RichiestaRepository`); non introdurre DAO e Repository duplicati. L'SDD prevede PostgreSQL e connettivita JDBC, non impone una specifica libreria ORM. Non introdurre JPA o altre dipendenze senza approvazione.
- DTO, se necessari e approvati: PascalCase con suffisso `DTO`, nel sottosistema pertinente; configurazioni Spring in `config`, utility condivise in `utilities`. Lasciare la configurazione della connessione a Spring Boot quando sufficiente, senza creare un gestore della connessione duplicato.
- Strategy: interfacce e classi in PascalCase con nomi che descrivano il comportamento. Per strategie di validazione, suffisso `Validator` nelle implementazioni (es. `PasswordValidator`); per altre strategie scegliere un nome coerente con il pattern approvato. Non imporre pattern non previsti.
- Test Java: in `backend/src/test/java`, distinguere `unit` e `integration` sotto il package radice, rispecchiando il sottosistema quando utile. Classi di test PascalCase con suffisso `Test`; metodi camelCase descrittivi, riconducibili ai Test Frame. Il Tester indipendente mantiene la responsabilita dei test applicativi.

### Frontend JavaScript / React (PWA)

- Organizzare il codice per sottosistemi in `frontend/src/sottosistemi/`; utilizzare gli stessi identificatori snake_case del backend. In ciascun sottosistema, `pages` per schermate, `components` per componenti Boundary, `services` per chiamate API e `hooks` solo se necessari.
- Componenti React e pagine: PascalCase e file `.jsx` omonimi (es. `DettaglioRichiesta.jsx`). Funzioni, props, variabili e gestori eventi: camelCase (es. `gestisciInvio`). Hook personalizzati: prefisso `use` e camelCase (es. `useRichieste`). Moduli JavaScript non componenti: camelCase (es. `richiestaService.js`); seguire le estensioni previste dalla configurazione approvata. Non introdurre TypeScript senza approvazione.
- Risorse condivise: `src/assets/images`, `src/assets/styles`, `src/components`, `src/services` o `src/utilities` solo quando realmente condivise. CSS con nomi coerenti e leggibili (es. `dettaglio-richiesta` per classi CSS). Risorse PWA pubbliche in `public/` secondo la configurazione approvata.
- I componenti React gestiscono presentazione, input e feedback; le chiamate al backend passano dai servizi frontend. La logica di business e l'accesso a PostgreSQL restano nel backend; non replicarli nel browser.
- Test frontend: `frontend/tests/unit/` e `frontend/tests/integration/`; nomi `NomeComponente.test.jsx` o `nomeModulo.test.js` (anche `.spec.*` se coerente con il runner approvato). Mantenere `test:ci` non interattivo, con report JUnit XML reale in `frontend/test-results/junit.xml`. Il backend usa i report Surefire/Failsafe in target. Tester e CI verificano almeno un test realmente eseguito (non saltato) per ogni stack inizializzato; non imporre coverage arbitrarie e non generare report fittizi.

### Struttura di riferimento dei sottosistemi

SDD v1.0, 23/11/2026, sezioni 3.1–3.3, pp. 10–15: i livelli di presentazione (Boundary React), applicazione (Control/Entity Spring Boot) e dati (PostgreSQL) sono separati. I sottosistemi sono esattamente questi otto:

| Sottosistema SDD | Package/cartella |
| --- | --- |
| Gestione Utenti | `gestione_utenti` |
| Gestione Neighbor | `gestione_neighbor` |
| Gestione Comunità | `gestione_comunita` |
| Gestione Beneficiario | `gestione_beneficiario` |
| Gestione Richieste | `gestione_richieste` |
| Gestione Comunicazione | `gestione_comunicazione` |
| Gestione Servizi Esterni | `gestione_servizi_esterni` |
| Gestione Notifiche | `gestione_notifiche` |

```text
backend/
  src/
    main/
      java/it/unisa/neighborcare/
        sottosistemi/
          gestione_utenti/
          gestione_neighbor/
          gestione_comunita/
          gestione_beneficiario/
          gestione_richieste/
            controller/
            service/
          gestione_comunicazione/
          gestione_servizi_esterni/
          gestione_notifiche/
        model/
          entity/
          dao/         (oppure repository, se approvato)
        config/
        utilities/
      resources/
    test/java/it/unisa/neighborcare/
      unit/
      integration/
frontend/
  src/
    sottosistemi/
      gestione_utenti/
      gestione_neighbor/
      gestione_comunita/
      gestione_beneficiario/
      gestione_richieste/
        pages/
        components/
        services/
        hooks/
      gestione_comunicazione/
      gestione_servizi_esterni/
      gestione_notifiche/
    assets/
      images/
      styles/
    components/
    services/
    utilities/
  public/
  tests/
    unit/
    integration/
```

La struttura e una convenzione di implementazione, non un elenco di file da generare subito. Creare solo package/cartelle/classi necessari al task autorizzato; non creare moduli vuoti o funzionalita fuori piano. Un sottosistema senza interfaccia utente dedicata non richiede pagine React. Rispettare la direzione delle dipendenze del diagramma SDD (sez. 3.2.1, p. 11), i servizi della sez. 3.2.2 (pp. 12–13), il diagramma Three-Tier (sez. 3.2.3, p. 14), il deployment (sez. 3.3.1 del PDF SDD originale) e l'Entity Class Diagram (sez. 4.2, p. 17). Non dedurre nuovi contratti dalla struttura delle cartelle.

### Applicazione delle convenzioni da parte degli agenti e del team

- Pianificatore (anche ripianificazione): indicare sottosistemi, package, livelli, servizi e file pertinenti, usando i nomi approvati; segnalare conflitti con RAD/SDD o codice esistente prima dell'autorizzazione.
- Implementatore e Correttore: applicare queste convenzioni al codice nel piano autorizzato; non modificare test o documenti protetti, non effettuare refactoring di moduli estranei al task.
- Tester: applicare le convenzioni ai nuovi test indipendenti, mantenendo i riferimenti ai Test Frame e senza alterare contratti o codice applicativo.
- Revisore e review umana: controllare naming, collocazione nei sottosistemi, separazione dei livelli e coerenza con RAD/SDD. Segnalare le violazioni concrete con file/riga e motivazione; richiedere correzioni quando incompatibili con le regole approvate.
- Queste convenzioni sono comuni anche ai contributi manuali dei TM. Non duplicarle nei profili agenti: tutti leggono questo file. Se un piano precedente o una PR in corso e incompatibile con le convenzioni, concordare l'allineamento con gli assegnatari; non cambiare silenziosamente un contratto gia approvato.

## Regole operative

- Seguire RAD, SDD, UC, Class Diagram ristrutturato, Sequence Diagram, Category Partition e Test Frame approvati. Gli esempi XX/YY non sono specifiche reali. Se una fonte è assente o illeggibile, dichiarare il limite; non inventare requisiti.
- Creare una Issue, assegnare responsabili, applicare `fase:piano`, verificare il piano e applicare `fase:implementazione`. L'Implementatore pubblica una Draft PR con Closes #N e responsabilità tracciate. Per ripianificare scrivere `AGENTE PIANO:`. Il controllo di coerenza dei modelli fa parte del piano.
- Applicare `fase:test` alla PR. Il Tester crea o aggiorna i test dai frame approvati. Se non servono modifiche, non produce commit fittizi. La fase Tester avvia la CI indipendente e attende l'esito reale prima di concludere, pubblicando anche eventuali errori. Se una CI valida esiste gia per lo stesso commit, la riusa senza duplicare i test; se manca, la avvia. Un test saltato non è superato. Una CI fallita o non disponibile rende la fase Tester non superata, senza modificare automaticamente il codice.
- Usare `AGENTE CORREGGI:` per correggere il task sulla PR esistente, `AGENTE TEST:` per rieseguire il Tester. Nessuna obbligatorietà di alternare Draft/Ready per ogni correzione.
- I ruoli sono separati: Pianificatore e Revisore in sola lettura; Implementatore/Correttore limitati a codice applicativo e documentazione ordinaria; Tester limitato ai file di test. Nessuna shell libera, Git, GitHub o credenziali al modello. Pubblicazione tramite runner separato con controllo di percorsi e SHA. Le modifiche a manifest, dipendenze, workflow, documenti approvati, PDF e test frame sono umane e tracciate.
- Le modifiche applicative devono rispettare lo stesso obiettivo autorizzato. Per un requisito diverso modificare la Issue e far approvare un nuovo piano o creare un nuovo task. Non indebolire o eliminare test per ottenere verde; i test esistenti si aggiornano con motivazione e copertura equivalente o migliore.
- La CI parte sui push manuali e dopo ogni commit agente. Il riepilogo dei test viene aggiornato nella PR, anche se fallisce un controllo; consultare Actions per il dettaglio. La review umana finale avvia il check obbligatorio sulla PR; non occorre autorizzare CI duplicate. GitHub Actions esegue build/test con PostgreSQL di sviluppo usa e getta, senza passare token Copilot al codice applicativo. In caso di errore, leggere i log, correggere il problema reale e ripetere il controllo. Non usare bypass amministrativi per eludere verifiche.
- I commit AI mantengono l'autore bot e riportano il vero richiedente, gli assegnatari e il run. Per riconoscere contributi umani effettivi, un assegnatario può dichiarare nella Issue (implementazione) o nella PR (test/correzione), prima di avviare la fase: `COAUTORE: implementazione - descrizione del contributo` (oppure `test` o `correzione`). Il runner aggiunge il trailer Co-authored-by al prossimo commit pertinente una sola volta per dichiarazione, senza cambiare l'autore bot. Non dichiarare contributi non svolti. Le PR agentiche ereditano gli assegnatari della Issue. Lo sviluppo manuale è consentito: branch per task, PR tracciata, Test Frame verificati, CI verde, review umana. Non è necessario invocare AI per ogni modifica.

## Pull Request e merge

GitHub richiede CI repository-checks verde e almeno un'approvazione umana; CODEOWNERS indirizza le richieste di review. Il revisore deve essere diverso dall'autore e dai responsabili del task; il team verifica questa indipendenza. La review umana è responsabile di esaminare e risolvere i rilievi reali e di verificare la copertura dei Test Frame prima di approvare. Dopo un nuovo commit le approvazioni precedenti non valgono. Per modificare un piano dopo l'apertura della PR, aggiornare la Issue, usare AGENTE PIANO: e poi AGENTE CORREGGI: nella PR con una riga PIANO APPROVATO: ID numerico del nuovo commento del bot. Non cambiare il riferimento senza approvazione. Il Revisore AI resta uno strumento di supporto e parte quando si seleziona Ready for review e dopo ogni nuovo commit su una PR non Draft.

## Quando un task è finito

Modifiche conformi al requisito e ai modelli, Test Frame coperti da test o prove manuali motivate, CI positiva, review umana indipendente e merge manuale. Il responsabile deve saper spiegare il risultato. I limiti delle verifiche devono essere dichiarati, non nascosti.

## Documenti di riferimento

[RAD](docs/rad/C01_RAD.pdf), [SDD](docs/sdd/C01_SDD.pdf), [indice degli artefatti](docs/README.md). Se manca una trasposizione reale, rimandare al PDF originale (file, sezione/versione pertinenti) e dichiarare eventuali limiti di lettura. Non copiare pagine o trascrizioni dei PDF in file Markdown.

Conservare tutti gli esempi UC/UML/CP/TF XX/YY, incluso `docs/modelli/sdd/class.puml`: servono ai ragazzi per il formato, non sono requisiti NeighborCare implementabili.

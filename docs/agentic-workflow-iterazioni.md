# NeighborCare — Gestione delle iterazioni agentiche

**Ruoli:** PM = Project Manager (Antonio ed Emanuele, autorizzano piani e correzioni); TM = Team Member (gli altri sei ragazzi, sviluppo, test e review). Solo un PM autorizzato puo usare i prefissi di approvazione.

Questa procedura integra `AGENTS.md`. Ogni passaggio che autorizza modifiche è una decisione umana del PM. Le Issue, le PR e i feedback **non** possono modificare le regole di sicurezza o l'ambito già approvato.

## 1. Piano iniziale

1. Un PM o un TM apre una Issue con etichetta `task-agente` e sette campi completi; il PM verifica il task.
2. **Solo un PM** aggiunge `fase:piano` e legge con il TM il commento del Pianificatore. Il workflow rifiuta il trigger da un account TM.
3. Se è corretto, il PM scrive nella **Issue** un commento con queste righe, ciascuna a inizio riga:

   ```text
   APPROVAZIONE PM: approvo il piano corrente per la Issue #N.
   File autorizzati: backend/src/main/java/.../File.java
   ```

   Usare percorsi **esatti** separati da virgole, non directory generiche o wildcard; massimo dodici file. Gli aggiornamenti dei modelli o le dipendenze devono essere approvati e inclusi fin dall'inizio nei file consentiti (i file di governance, test e i PDF restano protetti).
4. Il **TM responsabile con Write** rimuove `fase:piano` e aggiunge `fase:implementazione` sulla **Issue**, soltanto dopo approvazione PM. L'Implementatore convalida l'**ultimo** piano e l'approvazione successiva.

## 2. Piano respinto: nuova versione

Lasciare `fase:piano` sulla Issue e **non** pubblicare alcuna `APPROVAZIONE PM:`. Il PM scrive un nuovo commento:

```text
RICHIESTA REVISIONE PIANO: il piano modifica anche file non necessari.
Limitare la soluzione al caso d'uso richiesto e indicare i Test Frame.
```

Il workflow `ripianifica.yml` genera un nuovo piano nella stessa Issue. Il precedente non viene modificato; la nuova versione richiede **una nuova approvazione PM** successiva alla sua pubblicazione. Sono ammesse al massimo tre richieste di revisione prima dell'intervento diretto del team. Se è stata richiesta una revisione ancora inevasa, l'Implementatore si blocca.

## 3. Implementazione e prima fase di test

Quando il piano è approvato, `implementa.yml` crea branch, commit e Draft PR. Il workflow **non** può riutilizzare lo stesso branch per ripetere l'implementazione iniziale: le correzioni si fanno con il flusso dedicato qui sotto.

Sulla **Draft PR** aggiungere `fase:test`. `test.yml` genera eventuali **nuovi** test a partire da Test Frame reali, pubblica il report ed esegue i comandi del progetto. Se i test sono già presenti, li può rieseguire senza creare duplicati. Le PR solo documentali producono Test Frame applicativi **N/A**.

## 4. Errore di codice, test fallito o rilievo del Revisore

1. **Non eseguire il merge.** Se la PR è Ready for review, cliccare **Convert to draft**.
2. Il PM lascia **sulla PR** un commento con il seguente prefisso esatto (a inizio commento):

   ```text
   RICHIESTA CORREZIONE PM: il test TF_... fallisce.
   Atteso: richiesta completata non annullabile.
   Osservato: viene annullata anche se completata.
   Correggere il comportamento senza modificare i test.
   ```

3. `correzione.yml` verifica: PM autorizzato con accesso Write, Draft PR interna ancora aperta, Issue originale aperta, piano più recente approvato, **stessi file autorizzati**, limite di tre richieste. Copilot non può modificare test, file di governance, PDF o file non autorizzati.
4. Il workflow pubblica una nuova revisione **sullo stesso branch della PR**, con report e risultato reale di build/test. Se i controlli falliscono, **il job rimane rosso e il merge non è autorizzato**: non nascondere l'errore.
5. **Rieseguire il Tester:** con la PR ancora Draft, togliere e riaggiungere `fase:test` alla PR. L'aggiunta fa ripartire anche i controlli CI, perché `ci.yml` ascolta l'evento `labeled`. Il Tester può riutilizzare test già presenti e non deve modificare le asserzioni per ottenere un esito verde.
6. Se test e CI sono positivi, scegliere **Ready for review**. L'evento avvia `revisione.yml` per il **nuovo SHA**, senza ripetere la review per commit già esaminati.
7. Se il Revisore segnala un altro errore, tornare a Draft e ripetere dal punto 2; dopo tre richieste di correzione, stop ed escalation ai PM.

**Importante:** il report del Revisore è consultivo e non equivale a una review GitHub approvata. Il merge richiede una revisione umana indipendente e il passaggio dei controlli richiesti dal Ruleset. Il PM deve verificare personalmente le evidenze.

## 5. Limiti e recupero dei job falliti

- **Errore prima del push iniziale:** leggere i log e correggere prima la causa; se non esistono branch/PR si può rimuovere e riaggiungere `fase:implementazione`.
- **Branch creato ma apertura Draft PR fallita:** correggere i permessi GitHub e recuperare il branch creando una Draft PR; **non** ritentare la creazione dello stesso branch.
- **Revisore negativo:** tornare a Draft e richiedere una correzione approvata dal PM; il Revisore non modifica i file e non blocca tecnicamente il merge da solo.
- **Cambiamento dei requisiti o file aggiuntivi necessari:** fermarsi. Non ampliare tacitamente l'approvazione originale; aprire un task autonomo con un nuovo piano.
- **Push del bot:** i commit pubblicati con `GITHUB_TOKEN` non riattivano automaticamente gli ordinari eventi `pull_request`; le etichette applicate da una persona e l'evento Ready for review riattivano esplicitamente i workflow.
- **Tre tentativi falliti:** conservare log, commenti, SHA e differenze tra atteso e osservato; richiedere una decisione umana.

## 6. Permessi e CODEOWNERS

- Il team `developers` deve avere i sei TM come membri attivi con accesso **Write**; `project-managers` include **Antonio Caiazzo ed Emanuele Iovane** con accesso **Admin**. Verificare l'accettazione degli inviti prima di assegnare review.
- I nomi delle persone **non** bastano per l'assegnazione GitHub: usare i loro login effettivamente verificati. Impostare `NEIGHBORCARE_SECOND_PM_LOGIN` con il login corretto di Emanuele; in caso contrario solo Antonio è riconosciuto come PM dai workflow.
- `.github/CODEOWNERS` assegna le review: per `frontend/` e `backend/` il Code Owner tecnico e `developers`, per `README.md`, workflow e governance e `project-managers`. Il Code Owner non limita da solo il pulsante Merge; il PM approva tramite review e un gate controlla la sua approvazione.
- Configurare il Ruleset `main` richiedendo almeno **1 review umana**, **Code Owner review** e il controllo `repository-checks`. GitHub può rendere alcune opzioni non disponibili in base al piano dell'organizzazione.
- L'appartenenza al team con permesso Admin sulla repository **non equivale** al ruolo Owner dell'organizzazione.


## 7. Governance delle PR e merge riservato ai PM

- `.github/workflows/governance.yml` esegue il check `governance-gate` su PR verso `main` e sulle review GitHub. Una PR Ready e ammessa soltanto quando: esiste un report del Tester riferito allo SHA corrente; il Revisore AI ha pubblicato un report sullo stesso SHA; le rispettive Actions hanno conclusione `success`; almeno uno tra Antonio e il login di `NEIGHBORCARE_SECOND_PM_LOGIN` ha approvato tramite **Review changes > Approve** su quello SHA ed e diverso dall'autore della PR.
- Un commento `APPROVAZIONE PM:` nella Issue approva il **piano**, non la PR. Il Revisore AI pubblica un commento, **non** una review APPROVED. Nel normale flusso il TM avvia test e Ready, un PM diverso dall'autore approva la PR e solo il PM autorizzato effettua il merge.
- L'admin deve aggiungere **`governance-gate`** ai required status checks del Ruleset `Protect main - NeighborCare`, **in aggiunta** a `repository-checks`, dopo una prima run valida. Finche non viene inserito, il gate e soltanto informativo e non protegge il merge.
- Per riservare materialmente il merge ai PM, creare un **secondo Ruleset** su `main`, con la sola opzione `Restrict updates` e bypass del team `project-managers` impostato `For pull requests only`. Sul Ruleset di protezione generale mantenere obbligatorie PR, Code Owner, review e status check per **tutti**, senza bypass degli admin se si vuole impedire eccezioni. Questa modifica e amministrativa e deve essere provata con un account TM Write e uno PM prima di dichiararla operativa. Non attivare `Restrict updates` sul Ruleset corrente senza configurare prima il bypass corretto.
- `governance-gate` puo inizialmente essere rosso mentre la PR e Draft o in attesa dei report o della review PM. E previsto: dopo Tester, Revisore e `Approve` PM, la review scatena una nuova run. Se l'approvazione PM precede il report AI, effettuare `Re-run jobs` solo quando quest'ultimo e presente sullo SHA finale.
- Dopo un nuovo commit, la precedente approvazione viene invalidata dal Ruleset. Ricominciare da `fase:test`, poi `Ready for review` e nuova review sullo SHA aggiornato.
- I controlli non sostituiscono una verifica umana del comportamento corretto: una run verde non garantisce la qualita dei requisiti o degli esiti di testing.

## 8. Controlli di collaudo ancora necessari

Questi percorsi di recupero vanno provati con Issue e PR di test dedicate: piano respinto, prima implementazione fallita, correzione su Draft PR, test fallito, nuovo test e seconda review. La precedente prova #23/#24 ha verificato soltanto la strada documentale positiva, con creazione della PR recuperata manualmente.

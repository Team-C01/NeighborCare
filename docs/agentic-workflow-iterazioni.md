# NeighborCare - Workflow e cicli iterativi

## Ruoli

I PM creano le Issue, assegnano **uno o piu TM** con Write, poi applicano manualmente `fase:piano`. L'assegnazione non avvia il Pianificatore. Ogni TM assegnato puo gestire i passaggi successivi; una review umana deve provenire da una persona Write non assegnata, TM o PM. Non e obbligatoria una review PM, nemmeno sulla governance.

## Piano e autorizzazione

Il Pianificatore pubblica un piano quando un PM applica `fase:piano`. Un TM assegnato puo chiedere modifiche sulla Issue:

```text
RICHIESTA REVISIONE PIANO:
Aggiungere il recupero dei messaggi preesistenti.
Controllare il Sequence Diagram e i Test Frame pertinenti.
```

`ripianifica.yml` pubblica la nuova versione. Per autorizzare l'ultima proposta uno dei TM assegnati scrive sulla Issue:

```text
AUTORIZZA PIANO: autorizzo l'ultima versione del piano.
File autorizzati: backend/src/main/java/.../ChatService.java
```

Massimo 12 percorsi **esatti** di file; una autorizzazione precedente all'ultimo piano non vale. Il limite di tre ripianificazioni richiede una verifica umana in caso di stallo.

## Prima implementazione

Un TM assegnato sostituisce `fase:piano` con `fase:implementazione` **sulla Issue**. `implementa.yml` controlla autore e data dell'autorizzazione, verifica i percorsi, crea un branch e una Draft PR con `Closes #N`, `TM autorizzante: @login` e `TM assegnati: @a, @b`. L'elenco degli assegnatari viene congelato: se cambia, il workflow deve fermarsi finche non si decide come procedere.

## Tester e correzioni

Un TM assegnato applica `fase:test` **alla Draft PR**. Il Tester produce test indipendenti dalle specifiche e un report. Se un test fallisce, il Tester non corregge codice o test: un TM assegnato o revisore autorizzato pubblica sulla **PR**:

```text
RICHIESTA CORREZIONE:
TF_07 fallisce.
Atteso: richiesta completata non annullabile.
Osservato: annullamento consentito.
Correggere il comportamento senza modificare i test.
```

La stessa richiesta puo dire **Reimplementare completamente il metodo/la classe**, purche entro i file e i requisiti autorizzati. `correzione.yml` aggiorna lo stesso branch e la stessa PR, pubblicando un nuovo commit. Per i nuovi test il TM rimuove e riaggiunge `fase:test`; controllare nuovamente tutti i test pertinenti.

Tre tentativi AI consecutivi senza test superati richiedono intervento umano. Un nuovo ciclo puo iniziare quando, dopo test superati, emerge un rilievo ulteriore in review. Se e sbagliato il Test Frame oppure servono file/requisiti fuori ambito, fermarsi e aprire un altro task, senza indebolire i test.

## Revisore AI e review umana

Dopo Tester positivo, un TM assegnato clicca **Ready for review**. `revisione.yml` valuta diff e modelli e pubblica `ESITO_REVISIONE: PASS` o `CHANGES_REQUESTED`.

Se AI o persona trovano un problema: **Convert to draft**, commento `RICHIESTA CORREZIONE:`, correzione o reimplementazione nei file approvati, retest con `fase:test`, nuovo Ready for review e nuovo report AI. La PR non viene ricreata e il Revisore AI non modifica codice.

Un revisore umano con Write, **non tra gli assegnatari**, approva sullo SHA corrente con Review changes > Approve. Puo essere un TM o Emanuele come PM, ma nessun PM e richiesto obbligatoriamente. Dopo un nuovo commit, invalidare le vecchie approvazioni.

## Governance e merge

`governance-gate` controlla la corrispondenza tra assegnatari Issue/PR, Tester riuscito sul commit attuale, Revisore AI con verdetto PASS e review indipendente. Il Ruleset `Protect main - NeighborCare` richiede anche `repository-checks` e Code Owner review; `CODEOWNERS` consente reviewers developers **o** project-managers. Il merge e sempre manuale da TM o PM autorizzato. L'Issue collegata e la board si aggiornano dopo il merge.

Il Ruleset separato `PM-only merge - NeighborCare` va aggiornato tramite GitHub Settings, altrimenti i TM non possono fare merge nonostante i nuovi workflow. Non disattivare i required checks. I push di GitHub Actions con `GITHUB_TOKEN` possono non riattivare automaticamente altri workflow: gli eventi manuali su label e Ready for review fanno ripartire i controlli.

## Recupero

- Piano assente: PM verifica assegnatari e applica `fase:piano`.
- Implementazione fallita prima del push: leggere i log; non ripetere la fase se branch o PR esistono gia.
- Branch creato ma PR assente: recuperare la Draft PR esistente.
- Tester fallito: richiesta di correzione e retest.
- Review negativa: convertire a Draft, reimplementare o correggere, poi test e nuova review.
- Tre tentativi inefficaci: coinvolgere un membro del team e conservare log, commit e evidenze.

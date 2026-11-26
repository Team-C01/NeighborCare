# UC_B_01 – Crea Richiesta Form

## Crea Richiesta Form

| Campo | Valore |
| --- | --- |
| Identificativo | UC_B_01 |
| Nome | Crea Richiesta Form |
| Descrizione | Il Beneficiario deve poter creare una richiesta. |
| Attore principale | Beneficiario (Interesse: inserire una nuova richiesta nel sistema specificando tutte le informazioni necessarie affinché possa essere svolta) |
| Attori secondari | Nessuno |
| Entry condition | Il Beneficiario ha effettuato il login all'applicazione AND si trova nella schermata principale. |
| Exit condition on success | La richiesta è stata creata con successo AND è disponibile per essere accettata dai Neighbor della comunità corrispondente. |
| Exit condition on failure | Il sistema blocca la creazione AND non salva alcuna richiesta AND mostra un messaggio di errore al Beneficiario. |
| Extension point | Nessuno |
| Requisiti speciali | Nessuno |

### Flusso principale

1. **Beneficiario:** seleziona il pulsante per la creazione di una nuova richiesta dalla schermata principale.
2. **Sistema:** mostra il modulo di inserimento dati per la commissione (tipologia commissione, descrizione, luogo di ritiro, luogo di consegna, data e fascia oraria di ritiro, data e fascia oraria di consegna).
3. **Beneficiario:** compila i campi del modulo.
4. **Sistema:** mostra i campi compilati.
5. **Beneficiario:** aziona il comando di conferma richiesta.
6. **Sistema:** convalida i dati e registra la nuova richiesta associandole lo stato “In attesa”, aggiorna la dashboard del Beneficiario e rende la commissione visibile ai Neighbor della comunità.

### Flusso alternativo 3.a1 – Annullamento volontario

Durante la compilazione del form (passo 3), se il **Beneficiario** decide di non inoltrare la richiesta e seleziona il pulsante per annullarla (`3.a1`), il **Sistema** scarta i dati inseriti e riporta il Beneficiario alla schermata principale (`3.a2`).

### Flusso alternativo 6.a1 – Campi obbligatori mancanti

Durante la fase di convalida (passo 6), se il **Sistema** rileva che uno o più campi obbligatori sono vuoti, blocca il salvataggio, mostra un messaggio di errore e ritorna allo step 2.

### Eccezione 6.e1 – Errore di connessione

Durante la fase di invio (passo 6), se il **Sistema** rileva l'assenza di connessione internet sul dispositivo, mostra un avviso d'errore di rete e ritorna allo step 3.

## Artefatti collegati

- [Use Case Diagram (Gestione Beneficiario)](../../modelli/rad/UCD_03.puml): attori e casi d'uso del Beneficiario.
- [Statechart Stato Richiesta](../../modelli/rad/ST_01.puml): ciclo di vita e stati dell'entità `Richiesta`.
- [Activity Diagram del sistema proposto](../../modelli/rad/AD_SistemaProposto.puml): flusso operativo end-to-end e ramo di compilazione manuale della richiesta.
- [Navigational Path Beneficiario](../../modelli/rad/NP_B.puml): navigazione tra le schermate.
- [Class Diagram SDD](../../modelli/sdd/entityClassDiagram.puml): unico riferimento per entità, attributi e metodi.
- [Dipendenze dei sottosistemi SDD](../../modelli/sdd/diagrammaSottosistemi.puml): organizzazione logica e dipendenze tra `Gestione Richieste`, `Gestione Comunità` e `Gestione Beneficiario`.
- [Deployment Diagram SDD](../../modelli/sdd/deploymentDiagram.puml): architettura di deployment dei componenti.
- [Architettura a tre livelli SDD](../../modelli/sdd/diagrammaArchitetturale.puml): suddivisione logica tra `RichiesteGUI`, `GestioneRichiesta` e `RichiestaRepository`.
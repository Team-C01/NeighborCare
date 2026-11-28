# UC_C_01 – Verifica Nuovo Neighbor

## Verifica Nuovo Neighbor

| Campo | Valore |
| --- | --- |
| Identificativo | UC_C_01 |
| Nome | Verifica Nuovo Neighbor |
| Descrizione | Il Coordinatore verifica un nuovo Utente registrato come Neighbor, confermando la sua partecipazione alla comunità. |
| Attore principale | Coordinatore (Interesse: assicurarsi che solo persone fidate e idonee entrino a far parte della rete di assistenza locale) |
| Attori secondari | Neighbor (Interesse: ricevere l’approvazione da parte del Coordinatore per iniziare ad operare) |
| Entry condition | Il Coordinatore è loggato AND ha aperto la pagina di visualizzazione Neighbor “In attesa di verifica”. |
| Exit condition on success | L’account del Neighbor passa allo stato “Verificato” e può operare sulla piattaforma. |
| Exit condition on failure | Il sistema non registra la verifica. |
| Extension point | Nessuno |
| Requisiti speciali | Nessuno |

### Flusso principale

1. **Coordinatore:** seleziona un Neighbor dall’elenco per analizzarne i dati.
2. **Sistema:** mostra il profilo e i dettagli forniti dal Neighbor in fase di registrazione.
3. **Coordinatore:** utilizza il comando per verificare il Neighbor, confermandone la partecipazione alla rete.
4. **Sistema:** mostra una schermata per confermare o annullare la verifica.
5. **Coordinatore:** utilizza il comando per confermare la partecipazione del Neighbor alla Comunità.
6. **Sistema:** aggiorna lo stato del Neighbor a “Verificato” e lo rimuove dalla lista dei nuovi iscritti.
7. **Sistema:** mostra un messaggio di conferma al Coordinatore e genera una notifica per il Neighbor.

### Flusso alternativo 3.a1 – Rifiuto della verifica

Al passo 3, il **Coordinatore** riscontra incongruenze nei dati e seleziona il comando per rifiutare la registrazione del Neighbor (`3.a1`). Il **Sistema** registra il rifiuto, cambia lo stato dell’account in “Rifiutato” e notifica il Neighbor del mancato superamento della verifica (`3.a2`).

### Eccezione 2.e1 – Errore nel caricamento dei dettagli

Al passo 2, il **Sistema** mostra un messaggio di errore segnalando al Coordinatore che si è verificato un problema nel caricamento dei dati (`2.e1`), quindi termina con insuccesso e reindirizza all’elenco dei Neighbor (`2.e2`).

### Eccezione 6.e1 – Errore nella modifica dello stato

Al passo 6, il **Sistema** mostra un messaggio di errore segnalando al Coordinatore che si è verificato un problema nella modifica dello stato del Neighbor (`6.e1`), quindi termina con insuccesso e reindirizza al profilo con i dettagli forniti dal Neighbor (`6.e2`).

## Artefatti collegati

- [Use Case Diagram (Gestione Coordinatore)](../../modelli/rad/UCD_04.puml): attori e casi d'uso del Coordinatore.
- [Statechart Stato Neighbor](../../modelli/rad/ST_03.puml): transizioni di stato dell'account Neighbor.
- [Navigational Path Coordinatore](../../modelli/rad/NP_C.puml): navigazione tra le schermate.
- [Class Diagram SDD](../../modelli/sdd/entityClassDiagram.puml): unico riferimento per entità, attributi e metodi.
- [Dipendenze dei sottosistemi SDD](../../modelli/sdd/diagrammaSottosistemi.puml): organizzazione logica e dipendenze tra `Gestione Neighbor`, `Gestione Comunità`, `Gestione Utenti` e `Gestione Notifiche`.
- [Deployment Diagram SDD](../../modelli/sdd/deploymentDiagram.puml): architettura di deployment dei componenti.
- [Architettura a tre livelli SDD](../../modelli/sdd/diagrammaArchitetturale.puml): suddivisione logica tra livello di presentazione, logica applicativa e persistenza.
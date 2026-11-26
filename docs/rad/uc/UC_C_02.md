# UC_C_02 – Disattiva Neighbor

## Disattiva Neighbor

| Campo | Valore |
| --- | --- |
| Identificativo | UC_C_02 |
| Nome | Disattiva Neighbor |
| Descrizione | Il Coordinatore disattiva l’account di un Neighbor con una specifica motivazione. |
| Attore principale | Coordinatore (Interesse: mantenere elevata la qualità e la sicurezza della rete, allontanando gli utenti non più disponibili) |
| Attori secondari | Neighbor (Interesse: ricevere una motivazione chiara riguardo alla sospensione del proprio account) |
| Entry condition | Il Coordinatore è loggato AND si trova nella pagina dedicata alla visualizzazione dei Neighbor “Verificati” AND lo stato del Neighbor da disabilitare deve essere “Verificato” AND il Neighbor non deve essere impegnato nel completamento di una richiesta presa in carico. |
| Exit condition on success | L’account del Neighbor è disattivato e il volontario riceve una comunicazione con la motivazione. |
| Exit condition on failure | Il sistema non riesce a disattivare l’account e/o a inviare la notifica. |
| Extension point | Nessuno |
| Requisiti speciali | Nessuno |

### Flusso principale

1. **Coordinatore:** cerca il profilo specifico desiderato e seleziona il comando per disattivarne l'account.
2. **Sistema:** apre il modulo per l'inserimento della motivazione della disattivazione.
3. **Coordinatore:** seleziona una causale dal menu a tendina “Motivo disattivazione”, compila il campo “Note/ Dettagli motivazione” con la spiegazione estesa e clicca sul pulsante per confermare l'operazione.
4. **Sistema:** cambia lo stato del Neighbor in “Disattivato”, revoca i relativi permessi di accesso alla piattaforma, mostra un messaggio di conferma a schermo per il Coordinatore e invia automaticamente un'e-mail di notifica al Neighbor contenente la motivazione della disattivazione (estrapolata dai campi appena compilati).

### Flusso alternativo 2.a1 – Neighbor già “Disattivato”

Dopo aver selezionato il Neighbor, il **Sistema** rileva che il suo stato risulta già “Disattivato” (`2.a1`). Il **Coordinatore** torna indietro alla pagina di visualizzazione Neighbor “Verificati” (`2.a2`).

### Eccezione 4.e1 – Errore nella modifica dello stato

Al passo 4, il **Sistema** visualizza un messaggio di errore segnalando al Coordinatore che si è verificato un problema nella modifica dello stato del Neighbor (`4.e1`), quindi termina con insuccesso e reindirizza alla pagina di visualizzazione Neighbor “Verificati” (`4.e2`).

## Artefatti collegati

- [Use Case Diagram (Gestione Coordinatore)](../../modelli/rad/UCD_04.puml): attori e casi d'uso del Coordinatore.
- [Statechart Stato Neighbor](../../modelli/rad/ST_03.puml): transizioni di stato dell'account Neighbor.
- [Navigational Path Coordinatore](../../modelli/rad/NP_C.puml): navigazione tra le schermate.
- [Class Diagram SDD](../../modelli/sdd/entityClassDiagram.puml): unico riferimento per entità, attributi e metodi.
- [Dipendenze dei sottosistemi SDD](../../modelli/sdd/diagrammaSottosistemi.puml): organizzazione logica e dipendenze tra `Gestione Neighbor`, `Gestione Utenti`, `Gestione Richieste` e `Gestione Notifiche`.
- [Deployment Diagram SDD](../../modelli/sdd/deploymentDiagram.puml): architettura di deployment dei componenti.
- [Architettura a tre livelli SDD](../../modelli/sdd/diagrammaArchitetturale.puml): suddivisione logica tra livello di presentazione, logica applicativa e persistenza.
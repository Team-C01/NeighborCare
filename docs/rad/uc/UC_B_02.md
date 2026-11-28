# UC_B_02 – Utilizzo Chat

## Utilizzo Chat

| Campo | Valore |
| --- | --- |
| Identificativo | UC_B_02 |
| Nome | Utilizzo Chat |
| Descrizione | Il Beneficiario deve poter utilizzare la chat con il Neighbor. |
| Attore principale | Beneficiario (Interesse: utilizzare la chat per comunicare eventuali informazioni aggiuntive al Neighbor) |
| Attori secondari | Neighbor (Interesse: scambiare messaggi con il Beneficiario per chiedere informazioni o segnalare eventuali anomalie) |
| Entry condition | Esiste una richiesta attiva creata dal Beneficiario che viene presa in carico dal Neighbor. |
| Exit condition on success | Il messaggio inviato dal Beneficiario viene salvato a sistema e recapitato al Neighbor. |
| Exit condition on failure | Il sistema mantiene il testo digitato nel campo di composizione e mostra un messaggio di errore al Beneficiario, lasciando lo stato della richiesta e la cronologia della chat inalterati. |
| Extension point | Nessuno |
| Requisiti speciali | Nessuno |

### Flusso principale

1. **Beneficiario:** seleziona la propria richiesta attiva dalla schermata principale per visualizzarne le informazioni e ne apre la chat integrata.
2. **Sistema:** abilita il campo di inserimento testo per la commissione selezionata.
3. **Beneficiario:** scrive il messaggio e aziona il comando di invio.
4. **Sistema:** convalida il messaggio, lo registra, aggiorna la vista della chat del Beneficiario e invia una notifica al Neighbor; aggiorna inoltre la schermata di chat del Neighbor mostrando il nuovo messaggio ricevuto.

### Flusso alternativo 1.a1 – Consultazione cronologia

Il **Beneficiario** apre la chat solo per rileggere le informazioni o le istruzioni precedentemente scambiate con il Neighbor (`1.a1`). Il **Sistema** mostra l'elenco completo dei messaggi inviati e ricevuti fino a quel momento (`1.a2`).

### Flusso alternativo 2.a1 – Chiusura manuale chat

Dopo aver digitato un testo (o prima di completare l'invio), il **Beneficiario** decide di non inviare più il messaggio e seleziona il pulsante per uscire dalla chat/tornare indietro (`2.a1`). Il **Sistema** mostra l'elenco completo dei messaggi inviati e ricevuti fino a quel momento e una bozza del messaggio non inviato (`2.a2`), quindi visualizza la pagina di dettagli della richiesta associata alla chat (`2.a3`).

### Eccezione 4.e1 – Errore di connessione

Durante la fase di invio del messaggio (passo 4), il **Sistema** rileva l’assenza di connessione internet sul dispositivo del Beneficiario (`4.e1`). Il sistema mostra un avviso d'errore e contrassegna il messaggio con un'icona di errore, consentendo al Beneficiario di riprovare l'invio.

### Eccezione 3.e1 – Invio messaggio vuoto

Al passo 3, il **Beneficiario** tenta di azionare il pulsante di invio senza aver digitato alcun testo nella casella di composizione (`3.e1`). Il **Sistema** blocca l'operazione mantenendo il pulsante di invio disabilitato o mostrando un avviso visivo (`3.e2`).

## Artefatti collegati

- [Use Case Diagram (Gestione Beneficiario)](../../modelli/rad/UCD_03.puml): attori e casi d'uso del Beneficiario.
- [Activity Diagram del sistema proposto](../../modelli/rad/AD_SistemaProposto.puml): flusso operativo end-to-end dell'assistenza.
- [Navigational Path Beneficiario](../../modelli/rad/NP_B.puml): navigazione tra le schermate.
- [Class Diagram SDD](../../modelli/sdd/entityClassDiagram.puml): unico riferimento per entità, attributi e metodi.
- [Dipendenze dei sottosistemi SDD](../../modelli/sdd/diagrammaSottosistemi.puml): organizzazione logica e dipendenze tra `Gestione Comunicazione`, `Gestione Richieste` e `Gestione Notifiche`.
- [Deployment Diagram SDD](../../modelli/sdd/deploymentDiagram.puml): architettura di deployment dei componenti.
- [Architettura a tre livelli SDD](../../modelli/sdd/diagrammaArchitetturale.puml): suddivisione logica tra livello di presentazione, logica applicativa e persistenza.
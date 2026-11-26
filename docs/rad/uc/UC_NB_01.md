# UC_NB_01 – Presa in Carico Commissioni

## Presa in Carico Commissioni

| Campo | Valore |
| --- | --- |
| Identificativo | UC_NB_01 |
| Nome | Presa in Carico Commissioni |
| Descrizione | Funzione che permette al Neighbor di visualizzare le richieste di assistenza compatibili con i propri tragitti o orari e di accettarne una per prenderla in carico. |
| Attore principale | Neighbor (Interesse: ricevere richieste compatibili, valutarne i dettagli e confermare l'accettazione della commissione) |
| Attori secondari | Beneficiario (Interesse: che la richiesta di assistenza venga presa in considerazione e portata a termine) |
| Entry condition | Il Neighbor ha effettuato il login AND il Neighbor è verificato AND il Neighbor ha attivato la geolocalizzazione AND il Neighbor si trova sulla schermata delle nuove richieste AND è presente almeno una richiesta compatibile in base a posizione, fascia temporale e deviazione dal tragitto. |
| Exit condition on success | La commissione è assegnata al Neighbor, lo stato della richiesta viene aggiornato in “Accettata” e il sistema registra la presa in carico. |
| Exit condition on failure | La commissione è stata rifiutata dal Neighbor. La richiesta verrà mandata ad altri Neighbor e da parte del Beneficiario rimarrà in stato di attesa fino a quando non verrà accettata. |
| Extension point | Nessuno |
| Requisiti speciali | Nessuno |

### Flusso principale

1. **Neighbor:** dalla dashboard delle richieste, seleziona una specifica richiesta per visualizzarne i dettagli.
2. **Sistema:** mostra informazioni parziali della commissione (luogo di ritiro/consegna, orario, beni da ritirare), mantenendo nascosti gli indirizzi completi e i dati personali del Beneficiario fino all'accettazione.
3. **Neighbor:** utilizza il pulsante “Accetta” per accettare la commissione.
4. **Sistema:** registra l'avvenuta presa in carico, ne aggiorna lo stato in “Accettata” e genera istantaneamente una notifica per il Beneficiario.
5. **Sistema:** mostra al Neighbor i dettagli completi della richiesta e tutte le informazioni necessarie per completare la commissione: indirizzi completi di numero civico, dettagli del Beneficiario (nome, cognome, età) e specifiche dettagliate sul ritiro.

### Flusso alternativo 3.a1 – Annulla presa in carico

Dopo aver visualizzato i dettagli (passo 2), il **Neighbor** utilizza il comando per annullare la presa in carico (`3.a1`). Il **Sistema** non modifica alcuno stato e mostra la dashboard delle richieste (`3.a2`).

### Eccezione 3.e1 – Commissione non più disponibile

Al momento del click su “Accetta” (passo 3), il **Sistema** rileva che la commissione è appena stata presa in carico da un altro Neighbor (`3.e1`), quindi rimanda il Neighbor alla homepage e lo notifica del fatto che la richiesta non è più disponibile (`3.e2`).

### Eccezione 4.e1 – Errore di connessione

Durante il salvataggio dell'accettazione (passo 4), il **Sistema** riscontra un errore di rete (`4.e1`), mostra un messaggio di errore invitando il Neighbor a riprovare e lo mantiene sulla schermata di dettaglio della richiesta (`4.e2`).

## Artefatti collegati

- [Use Case Diagram (Gestione Neighbor)](../../modelli/rad/UCD_05.puml): attori e casi d'uso del Neighbor.
- [Statechart Stato Richiesta](../../modelli/rad/ST_01.puml): ciclo di vita e stati dell'entità `Richiesta`.
- [Activity Diagram del sistema proposto](../../modelli/rad/AD_SistemaProposto.puml): flusso operativo end-to-end dal matching delle richieste alla presa in carico.
- [Navigational Path Neighbor](../../modelli/rad/NP_NB.puml): navigazione tra le schermate.
- [Class Diagram SDD](../../modelli/sdd/entityClassDiagram.puml): unico riferimento per entità, attributi e metodi.
- [Dipendenze dei sottosistemi SDD](../../modelli/sdd/diagrammaSottosistemi.puml): organizzazione logica e dipendenze tra `Gestione Neighbor`, `Gestione Richieste` e `Gestione Notifiche`.
- [Deployment Diagram SDD](../../modelli/sdd/deploymentDiagram.puml): architettura di deployment dei componenti.
- [Architettura a tre livelli SDD](../../modelli/sdd/diagrammaArchitetturale.puml): suddivisione logica tra livello di presentazione, logica applicativa e persistenza.
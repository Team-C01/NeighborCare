# UC_B_03 – Crea Richiesta IA

## Crea Richiesta IA

| Campo | Valore |
| --- | --- |
| Identificativo | UC_B_03 |
| Nome | Crea Richiesta IA |
| Descrizione | Funzione del sistema che permette al Beneficiario di creare una richiesta utilizzando linguaggio naturale tramite tecnologia speech-to-text. |
| Attore principale | Beneficiario (Interesse: inserire rapidamente e facilmente una richiesta di assistenza senza dover digitare manualmente i campi) |
| Attori secondari | Nessuno |
| Entry condition | Il Beneficiario ha effettuato il login AND si trova nella sezione di inserimento di una nuova richiesta AND ha concesso all'applicazione i permessi di accesso al microfono. |
| Exit condition on success | Il sistema compila correttamente il form della richiesta partendo dall'audio, il Beneficiario conferma e la richiesta viene pubblicata. |
| Exit condition on failure | La richiesta non viene creata (es. audio incomprensibile, elaborazione fallita) e il Beneficiario viene invitato a riprovare o a procedere con l'inserimento manuale. |
| Extension point | Nessuno |
| Requisiti speciali | Nessuno |

### Flusso principale

1. **Beneficiario:** attiva il comando per l'inserimento vocale (microfono).
2. **Sistema:** si pone in ascolto e registra l'audio in ingresso.
3. **Beneficiario:** descrive a voce i campi del form e ferma la registrazione.
4. **Sistema:** converte l'audio in testo (*speech-to-text*), estrapola le informazioni chiave tramite IA (tipologia, luogo, data/ora) e mostra al Beneficiario il riepilogo della richiesta precompilata.
5. **Beneficiario:** verifica i dati proposti e utilizza il comando per confermare e pubblicare la richiesta.
6. **Sistema:** salva la richiesta, la rende disponibile in bacheca per i Neighbor e mostra un messaggio di successo al Beneficiario.

### Flusso alternativo 5.a1 – Modifica Manuale

Leggendo il riepilogo generato dall'IA al passo 4, il **Beneficiario** nota un'inesattezza e decide di modificare manualmente il campo errato (`5.a1`). Il **Sistema** accetta la modifica manuale, aggiorna il form mostrandolo a schermo e richiede al Beneficiario una nuova conferma per procedere (`5.a2`). Il **Beneficiario** verifica i dati corretti e utilizza il comando per confermare l'invio (`5.a3`), riprendendo il flusso dal passo 6.

### Eccezione 4.e1 – Audio Incomprensibile

Al passo 4, il **Sistema** non riesce a trascrivere l'audio o l'IA non riesce ad estrapolare informazioni sufficienti per compilare i campi obbligatori (`4.e1`), quindi mostra un messaggio di errore e invita l'utente a registrare nuovamente il messaggio vocale o a passare alla compilazione manuale (`4.e2`). Il **Beneficiario** sceglie come procedere (`4.e3`):
- **Nuova registrazione (`4.e4`):** il **Sistema** consente di ripetere la registrazione e il flusso riprende dal passo 1.
- **Compilazione manuale (`4.e5`):** il **Sistema** apre il modulo previsto da [UC_B_01 – Crea Richiesta Form](UC_B_01.md) e il presente caso d'uso termina senza creare la richiesta.

### Eccezione 4.e1 – API IA non disponibile

Al passo 4, il **Sistema** rileva che l’API IA non risulta disponibile (`4.e1`), mostra un messaggio di errore e invita l'utente a passare alla compilazione manuale (`4.e2`). Il **Beneficiario** procede con la compilazione manuale (`4.e3`) e il **Sistema** apre il modulo previsto da [UC_B_01 – Crea Richiesta Form](UC_B_01.md) (`4.e4`), terminando il presente caso d'uso senza creare la richiesta.

## Artefatti collegati

- [Use Case Diagram (Gestione Beneficiario)](../../modelli/rad/UCD_03.puml): attori e casi d'uso del Beneficiario.
- [Statechart Stato Richiesta](../../modelli/rad/ST_01.puml): ciclo di vita e stati dell'entità `Richiesta`.
- [Activity Diagram del sistema proposto](../../modelli/rad/AD_SistemaProposto.puml): flusso operativo end-to-end e ramo di inserimento vocale con fallback manuale.
- [Navigational Path Beneficiario](../../modelli/rad/NP_B.puml): navigazione tra le schermate.
- [Class Diagram SDD](../../modelli/sdd/entityClassDiagram.puml): unico riferimento per entità, attributi e metodi.
- [Dipendenze dei sottosistemi SDD](../../modelli/sdd/diagrammaSottosistemi.puml): organizzazione logica e dipendenze tra `Gestione Richieste` e `Gestione Servizi Esterni`.
- [Deployment Diagram SDD](../../modelli/sdd/deploymentDiagram.puml): architettura di deployment dei componenti e comunicazione verso il `Server Esterno`.
- [Architettura a tre livelli SDD](../../modelli/sdd/diagrammaArchitetturale.puml): suddivisione logica tra `RichiesteGUI`, `ServiziGUI`, `GestioneRichiesta` e `GestioneServizi`.
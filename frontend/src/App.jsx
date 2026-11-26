import { useId } from 'react';
import PresentazioneRuoli from './components/PresentazioneRuoli';

function App() {
  const sezioneRuoliId = useId();

  return (
    <main className="pagina-iniziale">
      <section className="scheda-benvenuto" aria-labelledby="titolo">
        <p className="etichetta">NeighborCare</p>
        <h1 id="titolo">Il vicinato, un aiuto alla volta.</h1>
        <p className="descrizione-benvenuto">
          La piattaforma per coordinare commissioni di vicinato non sanitarie.
        </p>
        <a className="link-scopri-ruoli" href={`#${sezioneRuoliId}`}>
          Scopri i ruoli
        </a>
      </section>
      <PresentazioneRuoli idSezione={sezioneRuoliId} />
    </main>
  );
}

export default App;

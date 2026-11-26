import PresentazioneRuoli from './components/PresentazioneRuoli';

function App() {
  return (
    <main className="pagina-iniziale">
      <section className="scheda-benvenuto" aria-labelledby="titolo">
        <p className="etichetta">NeighborCare</p>
        <h1 id="titolo">Il vicinato, un aiuto alla volta.</h1>
        <p>
          La piattaforma per coordinare commissioni di vicinato non sanitarie.
        </p>
      </section>
      <PresentazioneRuoli />
    </main>
  );
}

export default App;

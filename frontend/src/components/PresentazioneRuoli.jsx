import { useId } from 'react';

function PresentazioneRuoli() {
  const titoloId = useId();

  return (
    <section className="presentazione-ruoli" aria-labelledby={titoloId}>
      <h2 id={titoloId}>Come funziona NeighborCare</h2>
      <ul className="lista-ruoli">
        <li>
          <strong>Beneficiario</strong>
          <p>Richiede aiuto per commissioni non sanitarie.</p>
        </li>
        <li>
          <strong>Neighbor</strong>
          <p>Offre supporto per le commissioni di vicinato.</p>
        </li>
        <li>
          <strong>Coordinatore</strong>
          <p>Supervisiona il coordinamento del servizio.</p>
        </li>
      </ul>
    </section>
  );
}

export default PresentazioneRuoli;

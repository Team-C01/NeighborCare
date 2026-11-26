import { act } from 'react';
import { createRoot } from 'react-dom/client';
import { afterEach, expect, it } from 'vitest';
import App from '../../src/App.jsx';
import PresentazioneRuoli from '../../src/components/PresentazioneRuoli.jsx';

let container;
let root;

afterEach(async () => {
  if (root) {
    await act(async () => root.unmount());
    root = undefined;
  }
  container?.remove();
  container = undefined;
  globalThis.IS_REACT_ACT_ENVIRONMENT = false;
});

async function renderApp() {
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  container = document.createElement('div');
  document.body.append(container);
  root = createRoot(container);

  await act(async () => root.render(<App />));

  return container;
}

function trovaSezioneRuoli(app) {
  return [...app.querySelectorAll('section')].find(
    (section) =>
      section.querySelector('h2')?.textContent === 'Come funziona NeighborCare',
  );
}

it('TF_SETUP_01 renders the initial frontend application', async () => {
  const app = await renderApp();

  expect(app.firstElementChild).not.toBeNull();
});

it('TF_UI_01 preserves the main title and renders the roles section', async () => {
  const app = await renderApp();

  expect(app.querySelector('h1')?.textContent).toBe(
    'Il vicinato, un aiuto alla volta.',
  );
  expect(trovaSezioneRuoli(app)).toBeDefined();
});

it('TF_UI_02 presents exactly the three specified roles and descriptions', async () => {
  const app = await renderApp();
  const sezione = trovaSezioneRuoli(app);
  const lista = sezione?.querySelector('ul');

  expect(lista).toBeTruthy();
  expect(
    [...lista.querySelectorAll('li')].map((elemento) => [
      elemento.querySelector('strong')?.textContent,
      elemento.querySelector('p')?.textContent,
    ]),
  ).toEqual([
    ['Beneficiario', 'Richiede aiuto per commissioni non sanitarie.'],
    ['Neighbor', 'Offre supporto per le commissioni di vicinato.'],
    ['Coordinatore', 'Supervisiona il coordinamento del servizio.'],
  ]);
});

it('TF_UI_03 associates the roles section with its accessible heading', async () => {
  const app = await renderApp();
  const sezione = trovaSezioneRuoli(app);
  const titoloId = sezione?.getAttribute('aria-labelledby');
  const titolo = titoloId ? document.getElementById(titoloId) : null;

  expect(sezione?.tagName).toBe('SECTION');
  expect(titolo).not.toBeNull();
  expect(sezione?.contains(titolo)).toBe(true);
  expect(titolo?.tagName).toBe('H2');
  expect(titolo?.textContent).toBe('Come funziona NeighborCare');
});

it('TF_LINK_01 links to the unique roles section in the application', async () => {
  const app = await renderApp();
  const link = [...app.querySelectorAll('a')].find(
    (elemento) => elemento.textContent === 'Scopri i ruoli',
  );
  const href = link?.getAttribute('href');
  const sezione = href?.startsWith('#')
    ? document.getElementById(href.slice(1))
    : null;

  expect(link).not.toBeUndefined();
  expect(sezione).toBe(trovaSezioneRuoli(app));
  expect(sezione?.tagName).toBe('SECTION');
  expect(
    [...app.querySelectorAll('[id]')].filter(
      (elemento) => elemento.id === href?.slice(1),
    ),
  ).toHaveLength(1);
});

it('keeps accessible heading IDs unique across reusable role sections', async () => {
  const app = await renderApp();

  await act(async () =>
    root.render(
      <>
        <PresentazioneRuoli idSezione="ruoli-uno" />
        <PresentazioneRuoli idSezione="ruoli-due" />
      </>,
    ),
  );

  const sezioni = [...app.querySelectorAll('section')];
  const titoliId = sezioni.map((sezione) =>
    sezione.getAttribute('aria-labelledby'),
  );

  expect(sezioni).toHaveLength(2);
  expect(new Set(titoliId).size).toBe(2);
  sezioni.forEach((sezione, indice) => {
    const titolo = titoliId[indice]
      ? document.getElementById(titoliId[indice])
      : null;

    expect(titolo?.tagName).toBe('H2');
    expect(sezione.contains(titolo)).toBe(true);
  });
});

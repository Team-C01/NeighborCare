import { act } from 'react';
import { createRoot } from 'react-dom/client';
import { afterEach, expect, it } from 'vitest';
import App from '../../src/App.jsx';

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

it('TF_SETUP_01 renders the initial frontend application', async () => {
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  container = document.createElement('div');
  document.body.append(container);
  root = createRoot(container);

  await act(async () => root.render(<App />));

  expect(container.firstElementChild).not.toBeNull();
});

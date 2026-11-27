package it.unisa.neighborcare.simulazione;

public class EtichettaSimulazione {
    public String normalizza(String testo) {
        if (testo == null) {
            throw new IllegalArgumentException("Il testo non può essere null");
        }

        String etichettaNormalizzata = testo.strip();
        if (etichettaNormalizzata.isEmpty()) {
            throw new IllegalArgumentException("Il testo non può essere vuoto");
        }

        return etichettaNormalizzata;
    }
}

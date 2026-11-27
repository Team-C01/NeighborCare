package it.unisa.neighborcare.simulazione;

public class PrioritaSimulazione {

    public String calcolaPriorita(int punti) {
        if (punti < 0 || punti > 10) {
            throw new IllegalArgumentException("I punti devono essere compresi tra 0 e 10");
        }

        return punti >= 7 ? "ALTA" : "NORMALE";
    }
}

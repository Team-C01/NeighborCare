package it.unisa.neighborcare.simulazione;

public class PrioritaSimulazione {

    public String calcolaPriorita(int punti) {
        if (punti < 0 || punti > 10) {
            throw new IllegalArgumentException("Punti fuori intervallo 0-10");
        }

        return punti >= 7 ? "ALTA" : "NORMALE";
    }
}

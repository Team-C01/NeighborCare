package it.unisa.neighborcare.simulazione;

public class ContatoreSimulazione {

    public int incrementa(int valore) {
        if (valore < 0 || valore > 99) {
            throw new IllegalArgumentException("Il valore deve essere compreso tra 0 e 99");
        }
        return valore + 1;
    }
}

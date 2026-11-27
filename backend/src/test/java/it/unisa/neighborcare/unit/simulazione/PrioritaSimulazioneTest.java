package it.unisa.neighborcare.unit.simulazione;

import it.unisa.neighborcare.simulazione.PrioritaSimulazione;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class PrioritaSimulazioneTest {
    @Test
    void simTf01ValoreInferioreAlMinimoLanciaIllegalArgumentException() {
        PrioritaSimulazione priorita = new PrioritaSimulazione();

        assertThrows(IllegalArgumentException.class, () -> priorita.calcolaPriorita(-1));
    }

    @Test
    void simTf02ZeroRestituisceNormale() {
        PrioritaSimulazione priorita = new PrioritaSimulazione();

        assertEquals("NORMALE", priorita.calcolaPriorita(0));
    }

    @Test
    void simTf03SeiRestituisceNormale() {
        PrioritaSimulazione priorita = new PrioritaSimulazione();

        assertEquals("NORMALE", priorita.calcolaPriorita(6));
    }

    @Test
    void simTf04SetteRestituisceAlta() {
        PrioritaSimulazione priorita = new PrioritaSimulazione();

        assertEquals("ALTA", priorita.calcolaPriorita(7));
    }

    @Test
    void simTf05DieciRestituisceAlta() {
        PrioritaSimulazione priorita = new PrioritaSimulazione();

        assertEquals("ALTA", priorita.calcolaPriorita(10));
    }

    @Test
    void simTf06ValoreSuperioreAlMassimoLanciaIllegalArgumentException() {
        PrioritaSimulazione priorita = new PrioritaSimulazione();

        assertThrows(IllegalArgumentException.class, () -> priorita.calcolaPriorita(11));
    }

    @Test
    void simTf07TreRestituisceNormale() {
        PrioritaSimulazione priorita = new PrioritaSimulazione();

        assertEquals("NORMALE", priorita.calcolaPriorita(3));
    }

    @Test
    void simTf08OttoRestituisceAlta() {
        PrioritaSimulazione priorita = new PrioritaSimulazione();

        assertEquals("ALTA", priorita.calcolaPriorita(8));
    }
}

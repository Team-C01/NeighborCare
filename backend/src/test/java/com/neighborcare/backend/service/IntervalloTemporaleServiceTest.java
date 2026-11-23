package com.neighborcare.backend.service;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.LocalDateTime;
import org.junit.jupiter.api.Test;

class IntervalloTemporaleServiceTest {

    private static final LocalDateTime NOVE = LocalDateTime.of(2026, 12, 1, 9, 0);
    private static final LocalDateTime DIECI = LocalDateTime.of(2026, 12, 1, 10, 0);
    private static final LocalDateTime UNDICI = LocalDateTime.of(2026, 12, 1, 11, 0);
    private static final LocalDateTime DODICI = LocalDateTime.of(2026, 12, 1, 12, 0);
    private static final LocalDateTime QUINDICI = LocalDateTime.of(2026, 12, 1, 15, 0);

    private final IntervalloTemporaleService service = new IntervalloTemporaleService();

    @Test
    void TF_SIM_01_intervalloValido() {
        assertTrue(service.validaIntervallo(NOVE, UNDICI));
    }

    @Test
    void TF_SIM_02_estremiUguali() {
        assertFalse(service.validaIntervallo(NOVE, NOVE));
    }

    @Test
    void TF_SIM_03_estremiInvertiti() {
        assertFalse(service.validaIntervallo(DODICI, UNDICI));
    }

    @Test
    void TF_SIM_04_inizioNullo() {
        assertFalse(service.validaIntervallo(null, UNDICI));
    }

    @Test
    void TF_SIM_05_fineNulla() {
        assertFalse(service.validaIntervallo(NOVE, null));
    }

    @Test
    void TF_SIM_06_entrambiNulli() {
        assertFalse(service.validaIntervallo(null, null));
    }

    @Test
    void TF_SIM_07_sovrapposizioneParziale() {
        assertTrue(service.siSovrappongono(NOVE, UNDICI, DIECI, DODICI));
    }

    @Test
    void TF_SIM_08_intervalliConsecutivi() {
        assertFalse(service.siSovrappongono(NOVE, DIECI, DIECI, UNDICI));
    }

    @Test
    void TF_SIM_09_intervalliSeparati() {
        assertFalse(service.siSovrappongono(NOVE, DIECI, UNDICI, DODICI));
    }

    @Test
    void TF_SIM_10_intervalloNonValido() {
        assertFalse(service.siSovrappongono(DODICI, DIECI, NOVE, UNDICI));
    }

    @Test
    void TF_SIM_11_intervalloCompletamenteContenuto() {
        assertTrue(service.siSovrappongono(NOVE, QUINDICI, DIECI, DODICI));
    }

    @Test
    void TF_SIM_12_valoreNullo() {
        assertFalse(service.siSovrappongono(null, UNDICI, NOVE, DODICI));
    }
}

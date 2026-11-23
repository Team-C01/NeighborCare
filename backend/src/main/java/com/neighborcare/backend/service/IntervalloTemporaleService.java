package com.neighborcare.backend.service;

import java.time.LocalDateTime;

public class IntervalloTemporaleService {

    public boolean validaIntervallo(LocalDateTime inizio, LocalDateTime fine) {
        return inizio != null && fine != null && inizio.isBefore(fine);
    }

    public boolean siSovrappongono(
            LocalDateTime inizio1,
            LocalDateTime fine1,
            LocalDateTime inizio2,
            LocalDateTime fine2) {
        if (!validaIntervallo(inizio1, fine1) || !validaIntervallo(inizio2, fine2)) {
            return false;
        }

        boolean primoIniziaPrimaDellaFineDelSecondo = inizio1.isBefore(fine2);
        boolean secondoIniziaPrimaDellaFineDelPrimo = inizio2.isBefore(fine1);

        return primoIniziaPrimaDellaFineDelSecondo
                && secondoIniziaPrimaDellaFineDelPrimo;
    }
}

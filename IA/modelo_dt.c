
/*
 * =============================================================================
 * CÓDIGO GERADO AUTOMATICAMENTE - NÃO EDITAR MANUALMENTE
 * =============================================================================
 * Gerado em: 2026-01-27 19:36:55
 * Script: treinar_scanner.py
 * 
 * Classes:
 *   0 = PLANTA
 *   1 = AR_NEUTRO
 * =============================================================================
 */

// ============================================================================
// DECISION TREE
// ============================================================================

/**
 * Classifica uma amostra usando Decision Tree.
 * 
 * @param ratios Array de 9 elementos: [G320/G100, G295/G100, ..., G120/G100]
 * @return Classe predita (0, 1, ...)
 */
int identificar_dt(float ratios[]) {
    if (ratios[1] <= 0.020050f) {
        if (ratios[0] <= 0.012890f) {
            if (ratios[8] <= 0.635305f) {
                if (ratios[1] <= 0.019701f) {
                    return 1;  // AR_NEUTRO
                } else {
                    return 0;  // PLANTA
                }
            } else {
                return 1;  // AR_NEUTRO
            }
        } else {
            if (ratios[3] <= 0.043028f) {
                if (ratios[8] <= 0.642649f) {
                    if (ratios[5] <= 0.104626f) {
                        return 0;  // PLANTA
                    } else {
                        return 1;  // AR_NEUTRO
                    }
                } else {
                    return 0;  // PLANTA
                }
            } else {
                if (ratios[4] <= 0.066057f) {
                    return 1;  // AR_NEUTRO
                } else {
                    return 0;  // PLANTA
                }
            }
        }
    } else {
        if (ratios[7] <= 0.310555f) {
            if (ratios[0] <= 0.013646f) {
                if (ratios[1] <= 0.020277f) {
                    if (ratios[6] <= 0.175683f) {
                        return 0;  // PLANTA
                    } else {
                        return 1;  // AR_NEUTRO
                    }
                } else {
                    if (ratios[6] <= 0.179391f) {
                        return 0;  // PLANTA
                    } else {
                        return 1;  // AR_NEUTRO
                    }
                }
            } else {
                if (ratios[5] <= 0.108428f) {
                    if (ratios[8] <= 0.638287f) {
                        return 0;  // PLANTA
                    } else {
                        return 1;  // AR_NEUTRO
                    }
                } else {
                    if (ratios[0] <= 0.013956f) {
                        return 0;  // PLANTA
                    } else {
                        return 0;  // PLANTA
                    }
                }
            }
        } else {
            if (ratios[8] <= 0.645698f) {
                if (ratios[4] <= 0.073494f) {
                    return 0;  // PLANTA
                } else {
                    return 1;  // AR_NEUTRO
                }
            } else {
                if (ratios[2] <= 0.015094f) {
                    return 1;  // AR_NEUTRO
                } else {
                    if (ratios[0] <= 0.013279f) {
                        return 1;  // AR_NEUTRO
                    } else {
                        return 0;  // PLANTA
                    }
                }
            }
        }
    }
}

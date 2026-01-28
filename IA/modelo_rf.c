
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
// RANDOM FOREST (5 árvores)
// ============================================================================

// --- Árvore 0 ---
static int arvore_0(float ratios[]) {
    if (ratios[2] <= 0.029225f) {
        if (ratios[8] <= 0.635623f) {
            if (ratios[6] <= 0.173142f) {
                return 1;
            } else {
                return 0;
            }
        } else {
            if (ratios[2] <= 0.028874f) {
                return 1;
            } else {
                if (ratios[5] <= 0.104354f) {
                    return 0;
                } else {
                    return 1;
                }
            }
        }
    } else {
        if (ratios[5] <= 0.117207f) {
            if (ratios[1] <= 0.020913f) {
                if (ratios[1] <= 0.020289f) {
                    return 0;
                } else {
                    return 0;
                }
            } else {
                if (ratios[8] <= 0.650790f) {
                    return 1;
                } else {
                    return 0;
                }
            }
        } else {
            if (ratios[8] <= 0.645706f) {
                return 1;
            } else {
                if (ratios[0] <= 0.024930f) {
                    return 0;
                } else {
                    return 0;
                }
            }
        }
    }
}

// --- Árvore 1 ---
static int arvore_1(float ratios[]) {
    if (ratios[1] <= 0.019910f) {
        if (ratios[0] <= 0.012826f) {
            return 1;
        } else {
            if (ratios[0] <= 0.012831f) {
                return 0;
            } else {
                if (ratios[2] <= 0.028893f) {
                    return 1;
                } else {
                    return 1;
                }
            }
        }
    } else {
        if (ratios[0] <= 0.013212f) {
            if (ratios[8] <= 0.651664f) {
                if (ratios[7] <= 0.303352f) {
                    return 1;
                } else {
                    return 0;
                }
            } else {
                return 1;
            }
        } else {
            if (ratios[0] <= 0.013511f) {
                if (ratios[2] <= 0.030503f) {
                    return 0;
                } else {
                    return 1;
                }
            } else {
                if (ratios[5] <= 0.108425f) {
                    return 1;
                } else {
                    return 0;
                }
            }
        }
    }
}

// --- Árvore 2 ---
static int arvore_2(float ratios[]) {
    if (ratios[6] <= 0.175186f) {
        if (ratios[2] <= 0.029138f) {
            if (ratios[0] <= 0.012806f) {
                return 1;
            } else {
                if (ratios[8] <= 0.636160f) {
                    return 0;
                } else {
                    return 1;
                }
            }
        } else {
            if (ratios[7] <= 0.305946f) {
                if (ratios[1] <= 0.020341f) {
                    return 1;
                } else {
                    return 0;
                }
            } else {
                return 0;
            }
        }
    } else {
        if (ratios[0] <= 0.013115f) {
            if (ratios[7] <= 0.304873f) {
                if (ratios[8] <= 0.653679f) {
                    return 0;
                } else {
                    return 1;
                }
            } else {
                if (ratios[3] <= 0.043070f) {
                    return 1;
                } else {
                    return 1;
                }
            }
        } else {
            if (ratios[7] <= 0.309919f) {
                if (ratios[2] <= 0.030533f) {
                    return 0;
                } else {
                    return 1;
                }
            } else {
                if (ratios[0] <= 0.024997f) {
                    return 0;
                } else {
                    return 1;
                }
            }
        }
    }
}

// --- Árvore 3 ---
static int arvore_3(float ratios[]) {
    if (ratios[1] <= 0.019924f) {
        if (ratios[0] <= 0.012904f) {
            if (ratios[7] <= 0.300903f) {
                if (ratios[4] <= 0.066023f) {
                    return 1;
                } else {
                    return 0;
                }
            } else {
                if (ratios[2] <= 0.028964f) {
                    return 1;
                } else {
                    return 1;
                }
            }
        } else {
            if (ratios[5] <= 0.104741f) {
                return 0;
            } else {
                return 1;
            }
        }
    } else {
        if (ratios[2] <= 0.029464f) {
            if (ratios[7] <= 0.308832f) {
                if (ratios[4] <= 0.065977f) {
                    return 1;
                } else {
                    return 0;
                }
            } else {
                return 1;
            }
        } else {
            if (ratios[2] <= 0.030370f) {
                if (ratios[8] <= 0.651717f) {
                    return 0;
                } else {
                    return 0;
                }
            } else {
                if (ratios[8] <= 0.645299f) {
                    return 1;
                } else {
                    return 0;
                }
            }
        }
    }
}

// --- Árvore 4 ---
static int arvore_4(float ratios[]) {
    if (ratios[6] <= 0.175292f) {
        if (ratios[2] <= 0.028962f) {
            if (ratios[2] <= 0.028868f) {
                return 1;
            } else {
                if (ratios[1] <= 0.019706f) {
                    return 1;
                } else {
                    return 0;
                }
            }
        } else {
            if (ratios[7] <= 0.306573f) {
                if (ratios[5] <= 0.104582f) {
                    return 0;
                } else {
                    return 1;
                }
            } else {
                return 0;
            }
        }
    } else {
        if (ratios[0] <= 0.012998f) {
            if (ratios[1] <= 0.019939f) {
                return 1;
            } else {
                if (ratios[2] <= 0.029245f) {
                    return 0;
                } else {
                    return 1;
                }
            }
        } else {
            if (ratios[7] <= 0.307389f) {
                if (ratios[3] <= 0.044259f) {
                    return 0;
                } else {
                    return 1;
                }
            } else {
                if (ratios[7] <= 0.319646f) {
                    return 0;
                } else {
                    return 0;
                }
            }
        }
    }
}


/**
 * Classifica uma amostra usando Random Forest (votação majoritária).
 * 
 * @param ratios Array de 9 elementos: [G320/G100, G295/G100, ..., G120/G100]
 * @return Classe predita (0, 1, ...)
 */
int identificar_rf(float ratios[]) {
    int votos[2] = {0};
    
    // Coletar votos de cada árvore
    votos[arvore_0(ratios)]++;
    votos[arvore_1(ratios)]++;
    votos[arvore_2(ratios)]++;
    votos[arvore_3(ratios)]++;
    votos[arvore_4(ratios)]++;

    // Encontrar classe com mais votos
    int classe_vencedora = 0;
    int max_votos = votos[0];
    for (int i = 1; i < 2; i++) {
        if (votos[i] > max_votos) {
            max_votos = votos[i];
            classe_vencedora = i;
        }
    }
    
    return classe_vencedora;
}

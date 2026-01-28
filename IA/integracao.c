
// ============================================================================
// CÓDIGO DE INTEGRAÇÃO PARA MAIN.C
// ============================================================================
// Cole este código no seu main.c para usar os classificadores

// Escolha qual modelo usar (descomente UM):
#define USAR_DECISION_TREE
// #define USAR_RANDOM_FOREST
// #define USAR_SVM_LINEAR

// Função wrapper que chama o modelo selecionado
int identificar(float gases[]) {
    // Calcular ratios normalizados
    float ratios[9];
    float g100 = gases[9];  // G100 é o último elemento
    
    if (g100 <= 0) {
        return -1;  // Erro: G100 inválido
    }
    
    // ratios[0] = G320/G100, ratios[1] = G295/G100, ..., ratios[8] = G120/G100
    for (int i = 0; i < 9; i++) {
        ratios[i] = gases[i] / g100;
    }
    
    // Chamar modelo selecionado
#ifdef USAR_DECISION_TREE
    return identificar_dt(ratios);
#elif defined(USAR_RANDOM_FOREST)
    return identificar_rf(ratios);
#elif defined(USAR_SVM_LINEAR)
    return identificar_svm(ratios);
#else
    #error "Nenhum modelo selecionado! Descomente uma das definições acima."
#endif
}

// Nomes das classes para impressão
const char* NOMES_CLASSES[] = {
    "PLANTA",  // Classe 0
    "AR_NEUTRO",  // Classe 1
};

// Exemplo de uso no loop principal:
/*
void exemplo_classificacao() {
    float gases[10];  // G320, G295, ..., G100
    
    // ... coletar dados do sensor ...
    
    int classe = identificar(gases);
    
    if (classe >= 0) {
        printf("Classe detectada: %s\n", NOMES_CLASSES[classe]);
    } else {
        printf("Erro na classificação\n");
    }
}
*/

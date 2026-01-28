
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
// SVM LINEAR
// ============================================================================

// Pesos do hiperplano (w)
static const float svm_weights[9] = {
    3.49160976f, -1.00145950f, -2.02520785f, -2.82569044f, 5.56164028f, -2.23885858f, -1.52696944f, -0.42624243f, 0.21297775f
};

// Bias (b)
static const float svm_bias = -0.50875047f;

// Parâmetros do StandardScaler (média)
static const float scaler_mean[9] = {
    0.01411359f, 0.02163207f, 0.03112135f, 0.04540703f, 0.06865733f, 0.10867066f, 0.17894018f, 0.30882462f, 0.64590110f
};

// Parâmetros do StandardScaler (desvio padrão)
static const float scaler_std[9] = {
    0.00232593f, 0.00326162f, 0.00401661f, 0.00447094f, 0.00524255f, 0.00574027f, 0.00708913f, 0.00795405f, 0.00683998f
};

/**
 * Classifica uma amostra usando SVM Linear.
 * 
 * A classificação é feita calculando: sign(w · x_normalizado + b)
 * 
 * @param ratios Array de 9 elementos: [G320/G100, G295/G100, ..., G120/G100]
 * @return Classe predita (0 ou 1)
 */
int identificar_svm(float ratios[]) {
    float soma = svm_bias;
    
    // Calcular w · x_normalizado
    for (int i = 0; i < 9; i++) {
        // Normalizar feature: (x - mean) / std
        float x_norm = (ratios[i] - scaler_mean[i]) / scaler_std[i];
        soma += svm_weights[i] * x_norm;
    }
    
    // Retornar classe baseado no sinal
    return (soma > 0.0f) ? 1 : 0;
}

/**
 * Retorna a confiança da predição SVM (distância ao hiperplano).
 * Valores maiores indicam maior confiança.
 * 
 * @param ratios Array de 9 elementos
 * @return Valor de decisão (positivo = classe 1, negativo = classe 0)
 */
float svm_confianca(float ratios[]) {
    float soma = svm_bias;
    for (int i = 0; i < 9; i++) {
        float x_norm = (ratios[i] - scaler_mean[i]) / scaler_std[i];
        soma += svm_weights[i] * x_norm;
    }
    return soma;
}

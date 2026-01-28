#!/usr/bin/env python3
"""
=============================================================================
TREINADOR MULTIMODELO PARA BME688 - NARIZ ELETRÔNICO
=============================================================================
ATUALIZADO: Suporte a múltiplos arquivos por classe

Estrutura de dados suportada:
1. Arquivos separados por classe (modo antigo):
   ARQUIVOS = {0: 'planta.csv', 1: 'ar_neutro.csv'}

2. Múltiplos arquivos por classe (NOVO):
   ARQUIVOS = {
       0: ['planta_01.csv', 'planta_02.csv', 'planta_noite.csv'],
       1: ['ar_manha.csv', 'ar_tarde.csv', 'ar_noite.csv']
   }

3. Arquivo único com coluna 'classe' (NOVO):
   ARQUIVO_UNICO = 'todos_dados.csv'  # Deve ter coluna 'classe'

=============================================================================
"""

import pandas as pd
import numpy as np
import os
import sys
import argparse
import glob
from datetime import datetime

# Scikit-learn
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# =============================================================================
# CONFIGURAÇÃO - EDITE AQUI
# =============================================================================

# OPÇÃO 1: Arquivos separados por classe (pode ser lista ou string única)
ARQUIVOS = {
    0: [
        '../data/planta.csv',
        '../data/planta2.csv',
        # Adicione mais arquivos de planta aqui
    ],
    1: [
        '../data/ar_neutro.csv',
        '../data/ar_neutro2.csv',
        # Adicione mais arquivos de ar neutro aqui
    ],
    # 2: ['../data/doenca_a.csv', '../data/doenca_b.csv'],
}

# OPÇÃO 2: Arquivo único com coluna 'classe' (descomente para usar)
# ARQUIVO_UNICO = '../data/todos_dados.csv'

# OPÇÃO 3: Usar padrão glob (ex: todos os CSVs de uma pasta)
# USA_GLOB = True
# PADROES_GLOB = {
#     0: '../data/planta_*.csv',
#     1: '../data/ar_*.csv',
# }

NOMES_CLASSES = {
    0: "PLANTA",
    1: "AR_NEUTRO",
    # 2: "DOENTE",
}

# Features do sensor
FEATURES_RAW = ['G320', 'G295', 'G270', 'G245', 'G220', 'G195', 'G170', 'G145', 'G120', 'G100']
FEATURES_RATIO = ['R_G320', 'R_G295', 'R_G270', 'R_G245', 'R_G220', 'R_G195', 'R_G170', 'R_G145', 'R_G120']

# Configurações dos modelos
CONFIG_MODELOS = {
    'dt': {
        'nome': 'Decision Tree',
        'max_depth': 5,
        'random_state': 42
    },
    'rf': {
        'nome': 'Random Forest',
        'n_estimators': 5,
        'max_depth': 4,
        'random_state': 42
    },
    'svm': {
        'nome': 'SVM Linear',
        'kernel': 'linear',
        'C': 1.0,
        'random_state': 42
    }
}

# =============================================================================
# FUNÇÕES DE CARREGAMENTO
# =============================================================================

def normalizar_lista_arquivos(entrada):
    """Converte entrada para lista de arquivos."""
    if isinstance(entrada, str):
        return [entrada]
    elif isinstance(entrada, list):
        return entrada
    else:
        return []

def carregar_arquivo_csv(caminho, id_classe=None):
    """Carrega um único arquivo CSV."""
    if not os.path.exists(caminho):
        return None
    
    try:
        df = pd.read_csv(caminho)
        
        # Verificar se tem coluna 'classe' (arquivo com múltiplas classes)
        if 'classe' in df.columns and id_classe is None:
            # Arquivo com coluna classe - usar LabelEncoder
            return df
        
        # Verificar colunas de gás
        cols_faltando = [c for c in FEATURES_RAW if c not in df.columns]
        if cols_faltando:
            print(f"   ⚠️  Colunas faltando: {cols_faltando}")
            return None
        
        # Filtrar colunas
        colunas_manter = [c for c in df.columns if c in FEATURES_RAW or c in ['temp', 'umid', 'timestamp', 'amostra_id', 'sessao_id', 'notas', 'classe']]
        df = df[colunas_manter].copy()
        
        # Definir classe se fornecida
        if id_classe is not None:
            df['target'] = id_classe
        
        return df
        
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return None

def carregar_dados():
    """Carrega todos os dados de todas as fontes configuradas."""
    df_list = []
    base_dir = os.path.dirname(__file__)
    
    print("\n📂 CARREGANDO DADOS")
    print("=" * 60)
    
    # Verificar se está usando arquivo único
    if 'ARQUIVO_UNICO' in globals() and ARQUIVO_UNICO:
        print("\n📄 Modo: Arquivo único com coluna 'classe'")
        full_path = os.path.join(base_dir, ARQUIVO_UNICO)
        df = carregar_arquivo_csv(full_path)
        
        if df is not None and 'classe' in df.columns:
            # Converter classe string para numérico
            le = LabelEncoder()
            df['target'] = le.fit_transform(df['classe'])
            
            # Atualizar NOMES_CLASSES
            global NOMES_CLASSES
            NOMES_CLASSES = {i: nome.upper() for i, nome in enumerate(le.classes_)}
            
            print(f"   Classes encontradas: {list(le.classes_)}")
            df_list.append(df)
    
    # Verificar se está usando glob
    elif 'USA_GLOB' in globals() and USA_GLOB and 'PADROES_GLOB' in globals():
        print("\n📄 Modo: Padrões glob")
        for id_classe, padrao in PADROES_GLOB.items():
            full_pattern = os.path.join(base_dir, padrao)
            arquivos = glob.glob(full_pattern)
            
            nome = NOMES_CLASSES.get(id_classe, f'Classe {id_classe}')
            print(f"\n🏷️  {nome} (padrão: {padrao})")
            
            for arq in arquivos:
                df = carregar_arquivo_csv(arq, id_classe)
                if df is not None:
                    df_list.append(df)
                    print(f"   ✅ {os.path.basename(arq)}: {len(df)} amostras")
    
    # Modo padrão: dicionário de arquivos
    else:
        print("\n📄 Modo: Arquivos por classe")
        
        for id_classe, arquivos in ARQUIVOS.items():
            arquivos_lista = normalizar_lista_arquivos(arquivos)
            nome = NOMES_CLASSES.get(id_classe, f'Classe {id_classe}')
            
            print(f"\n🏷️  {nome} ({len(arquivos_lista)} arquivo(s))")
            
            total_classe = 0
            
            for caminho in arquivos_lista:
                full_path = os.path.join(base_dir, caminho)
                df = carregar_arquivo_csv(full_path, id_classe)
                
                if df is not None:
                    # Processar dados
                    df = df[FEATURES_RAW].copy()
                    df = df.replace([np.inf, -np.inf], np.nan).dropna()
                    df = df[df['G100'] > 0]
                    
                    # Criar ratios
                    for col in FEATURES_RAW[:-1]:
                        df[f'R_{col}'] = df[col] / df['G100']
                    
                    df['target'] = id_classe
                    df_list.append(df)
                    
                    total_classe += len(df)
                    print(f"   ✅ {os.path.basename(caminho)}: {len(df):,} amostras")
                else:
                    print(f"   ❌ {os.path.basename(caminho)}: não encontrado")
            
            print(f"   📊 Total {nome}: {total_classe:,} amostras")
    
    if not df_list:
        print("\n❌ Nenhum dado válido encontrado!")
        print("\n💡 Verifique:")
        print("   - Os caminhos dos arquivos em ARQUIVOS")
        print("   - Se os arquivos CSV existem")
        print("   - Se os arquivos têm as colunas G320...G100")
        sys.exit(1)
    
    # Concatenar todos os dados
    df_final = pd.concat(df_list, ignore_index=True)
    
    # Garantir que temos os ratios
    if 'R_G320' not in df_final.columns:
        for col in FEATURES_RAW[:-1]:
            df_final[f'R_{col}'] = df_final[col] / df_final['G100']
    
    # Estatísticas finais
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS DADOS")
    print("=" * 60)
    
    print(f"\n{'Classe':<15} {'Amostras':>10} {'Porcentagem':>12}")
    print("-" * 40)
    
    for id_classe in sorted(df_final['target'].unique()):
        n = len(df_final[df_final['target'] == id_classe])
        pct = n / len(df_final) * 100
        nome = NOMES_CLASSES.get(id_classe, f'Classe {id_classe}')
        print(f"{nome:<15} {n:>10,} {pct:>11.1f}%")
    
    print("-" * 40)
    print(f"{'TOTAL':<15} {len(df_final):>10,}")
    
    # Verificar balanceamento
    counts = df_final['target'].value_counts()
    ratio = counts.max() / counts.min()
    if ratio > 2:
        print(f"\n⚠️  AVISO: Classes desbalanceadas (ratio {ratio:.1f}:1)")
        print("   Considere coletar mais dados da classe minoritária")
    
    return df_final

def preparar_dados(df, usar_ratios=True):
    """Prepara X e y para treinamento."""
    features = FEATURES_RATIO if usar_ratios else FEATURES_RAW[:-1]
    
    # Verificar se todas as features existem
    for f in features:
        if f not in df.columns:
            print(f"❌ Feature não encontrada: {f}")
            sys.exit(1)
    
    X = df[features].values
    y = df['target'].values
    return X, y, features

# =============================================================================
# FUNÇÕES DE TREINAMENTO
# =============================================================================

def treinar_decision_tree(X, y):
    cfg = CONFIG_MODELOS['dt']
    clf = DecisionTreeClassifier(
        max_depth=cfg['max_depth'],
        random_state=cfg['random_state']
    )
    clf.fit(X, y)
    return clf

def treinar_random_forest(X, y):
    cfg = CONFIG_MODELOS['rf']
    clf = RandomForestClassifier(
        n_estimators=cfg['n_estimators'],
        max_depth=cfg['max_depth'],
        random_state=cfg['random_state']
    )
    clf.fit(X, y)
    return clf

def treinar_svm(X, y):
    cfg = CONFIG_MODELOS['svm']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    clf = SVC(
        kernel=cfg['kernel'],
        C=cfg['C'],
        random_state=cfg['random_state']
    )
    clf.fit(X_scaled, y)
    return clf, scaler

def avaliar_modelos(X, y):
    """Avalia todos os modelos com cross-validation."""
    print("\n📈 AVALIAÇÃO DOS MODELOS (5-fold cross-validation)")
    print("=" * 60)
    
    resultados = {}
    
    # Decision Tree
    dt = DecisionTreeClassifier(
        max_depth=CONFIG_MODELOS['dt']['max_depth'],
        random_state=CONFIG_MODELOS['dt']['random_state']
    )
    scores_dt = cross_val_score(dt, X, y, cv=5, scoring='accuracy')
    resultados['dt'] = {'media': scores_dt.mean(), 'std': scores_dt.std()}
    print(f"\n🌳 Decision Tree:  {scores_dt.mean():.2%} ± {scores_dt.std():.2%}")
    
    # Random Forest
    rf = RandomForestClassifier(
        n_estimators=CONFIG_MODELOS['rf']['n_estimators'],
        max_depth=CONFIG_MODELOS['rf']['max_depth'],
        random_state=CONFIG_MODELOS['rf']['random_state']
    )
    scores_rf = cross_val_score(rf, X, y, cv=5, scoring='accuracy')
    resultados['rf'] = {'media': scores_rf.mean(), 'std': scores_rf.std()}
    print(f"🌲 Random Forest:  {scores_rf.mean():.2%} ± {scores_rf.std():.2%}")
    
    # SVM Linear
    from sklearn.pipeline import make_pipeline
    svm_pipe = make_pipeline(
        StandardScaler(),
        SVC(kernel='linear', C=1.0, random_state=42)
    )
    scores_svm = cross_val_score(svm_pipe, X, y, cv=5, scoring='accuracy')
    resultados['svm'] = {'media': scores_svm.mean(), 'std': scores_svm.std()}
    print(f"📐 SVM Linear:     {scores_svm.mean():.2%} ± {scores_svm.std():.2%}")
    
    # Melhor modelo
    melhor = max(resultados.items(), key=lambda x: x[1]['media'])
    print(f"\n🏆 Melhor modelo: {CONFIG_MODELOS[melhor[0]]['nome']}")
    
    return resultados

# =============================================================================
# GERADORES DE CÓDIGO C (mantidos do original)
# =============================================================================

def gerar_header_c():
    header = f"""
/*
 * =============================================================================
 * CÓDIGO GERADO AUTOMATICAMENTE - NÃO EDITAR MANUALMENTE
 * =============================================================================
 * Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 * Script: treinar_scanner.py
 * 
 * Classes:
"""
    for id_classe, nome in sorted(NOMES_CLASSES.items()):
        header += f" *   {id_classe} = {nome}\n"
    header += " * =============================================================================\n */\n"
    return header

def gerar_decision_tree_c(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != -2 else "undefined!"
        for i in tree_.feature
    ]
    
    code_lines = []
    
    def recurse(node, depth):
        indent = "    " * depth
        if tree_.feature[node] != -2:
            col = feature_name[node]
            idx = feature_names.index(col) if col in feature_names else -1
            nome_c = f"ratios[{idx}]"
            threshold = tree_.threshold[node]
            
            code_lines.append(f"{indent}if ({nome_c} <= {threshold:.6f}f) {{")
            recurse(tree_.children_left[node], depth + 1)
            code_lines.append(f"{indent}}} else {{")
            recurse(tree_.children_right[node], depth + 1)
            code_lines.append(f"{indent}}}")
        else:
            classe = int(tree_.value[node][0].argmax())
            nome = NOMES_CLASSES.get(classe, f"CLASSE_{classe}")
            code_lines.append(f"{indent}return {classe};  // {nome}")
    
    recurse(0, 1)
    
    code = gerar_header_c()
    code += """
// ============================================================================
// DECISION TREE
// ============================================================================

int identificar_dt(float ratios[]) {
"""
    code += "\n".join(code_lines)
    code += "\n}\n"
    
    return code

def gerar_random_forest_c(rf, feature_names):
    n_trees = len(rf.estimators_)
    n_classes = len(NOMES_CLASSES)
    
    code = gerar_header_c()
    code += f"""
// ============================================================================
// RANDOM FOREST ({n_trees} árvores)
// ============================================================================

"""
    
    for i, tree in enumerate(rf.estimators_):
        code += f"static int arvore_{i}(float ratios[]) {{\n"
        
        tree_ = tree.tree_
        feature_name = [
            feature_names[j] if j != -2 else "undefined!"
            for j in tree_.feature
        ]
        
        lines = []
        def recurse(node, depth):
            indent = "    " * depth
            if tree_.feature[node] != -2:
                col = feature_name[node]
                idx = feature_names.index(col) if col in feature_names else -1
                nome_c = f"ratios[{idx}]"
                threshold = tree_.threshold[node]
                
                lines.append(f"{indent}if ({nome_c} <= {threshold:.6f}f) {{")
                recurse(tree_.children_left[node], depth + 1)
                lines.append(f"{indent}}} else {{")
                recurse(tree_.children_right[node], depth + 1)
                lines.append(f"{indent}}}")
            else:
                classe = int(tree_.value[node][0].argmax())
                lines.append(f"{indent}return {classe};")
        
        recurse(0, 1)
        code += "\n".join(lines)
        code += "\n}\n\n"
    
    code += f"""
int identificar_rf(float ratios[]) {{
    int votos[{n_classes}] = {{0}};
    
"""
    for i in range(n_trees):
        code += f"    votos[arvore_{i}(ratios)]++;\n"
    
    code += f"""
    int classe_vencedora = 0;
    int max_votos = votos[0];
    for (int i = 1; i < {n_classes}; i++) {{
        if (votos[i] > max_votos) {{
            max_votos = votos[i];
            classe_vencedora = i;
        }}
    }}
    
    return classe_vencedora;
}}
"""
    return code

def gerar_svm_c(svm, scaler, feature_names):
    w = svm.coef_[0]
    b = svm.intercept_[0]
    mean = scaler.mean_
    std = scaler.scale_
    n_features = len(w)
    
    code = gerar_header_c()
    code += f"""
// ============================================================================
// SVM LINEAR
// ============================================================================

static const float svm_weights[{n_features}] = {{
    {', '.join(f'{x:.8f}f' for x in w)}
}};

static const float svm_bias = {b:.8f}f;

static const float scaler_mean[{n_features}] = {{
    {', '.join(f'{x:.8f}f' for x in mean)}
}};

static const float scaler_std[{n_features}] = {{
    {', '.join(f'{x:.8f}f' for x in std)}
}};

int identificar_svm(float ratios[]) {{
    float soma = svm_bias;
    
    for (int i = 0; i < {n_features}; i++) {{
        float x_norm = (ratios[i] - scaler_mean[i]) / scaler_std[i];
        soma += svm_weights[i] * x_norm;
    }}
    
    return (soma > 0.0f) ? 1 : 0;
}}

float svm_confianca(float ratios[]) {{
    float soma = svm_bias;
    for (int i = 0; i < {n_features}; i++) {{
        float x_norm = (ratios[i] - scaler_mean[i]) / scaler_std[i];
        soma += svm_weights[i] * x_norm;
    }}
    return soma;
}}
"""
    return code

def gerar_codigo_integracao():
    code = """
// ============================================================================
// CÓDIGO DE INTEGRAÇÃO PARA MAIN.C
// ============================================================================

// Escolha qual modelo usar (descomente UM):
#define USAR_DECISION_TREE
// #define USAR_RANDOM_FOREST
// #define USAR_SVM_LINEAR

int identificar(float gases[]) {
    float ratios[9];
    float g100 = gases[9];
    
    if (g100 <= 0) {
        return -1;
    }
    
    for (int i = 0; i < 9; i++) {
        ratios[i] = gases[i] / g100;
    }
    
#ifdef USAR_DECISION_TREE
    return identificar_dt(ratios);
#elif defined(USAR_RANDOM_FOREST)
    return identificar_rf(ratios);
#elif defined(USAR_SVM_LINEAR)
    return identificar_svm(ratios);
#else
    #error "Nenhum modelo selecionado!"
#endif
}

const char* NOMES_CLASSES[] = {
"""
    for id_classe, nome in sorted(NOMES_CLASSES.items()):
        code += f'    "{nome}",\n'
    code += "};\n"
    return code

# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Treinador Multi-Modelo para BME688',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--modelo', choices=['dt', 'rf', 'svm', 'auto'],
                        default='auto', help='Modelo para gerar código C')
    parser.add_argument('--exportar', choices=['console', 'arquivo', 'todos'],
                        default='console', help='Onde exportar o código')
    parser.add_argument('--avaliar', action='store_true',
                        help='Mostrar avaliação detalhada')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🧠 TREINADOR MULTI-MODELO PARA BME688")
    print("=" * 60)
    
    # Carregar dados
    df = carregar_dados()
    X, y, features = preparar_dados(df, usar_ratios=True)
    
    # Avaliar todos os modelos
    resultados = avaliar_modelos(X, y)
    
    # Determinar qual modelo exportar
    if args.modelo == 'auto':
        modelo_escolhido = max(resultados.items(), key=lambda x: x[1]['media'])[0]
        print(f"\n🎯 Modelo selecionado: {CONFIG_MODELOS[modelo_escolhido]['nome']}")
    else:
        modelo_escolhido = args.modelo
    
    # Treinar e exportar
    print(f"\n🔧 Treinando modelo(s) final(is)...")
    
    if args.exportar == 'todos':
        modelos_para_exportar = ['dt', 'rf', 'svm']
    else:
        modelos_para_exportar = [modelo_escolhido]
    
    for modelo in modelos_para_exportar:
        print(f"\n{'='*60}")
        print(f"📝 {CONFIG_MODELOS[modelo]['nome'].upper()}")
        print("="*60)
        
        if modelo == 'dt':
            clf = treinar_decision_tree(X, y)
            codigo = gerar_decision_tree_c(clf, features)
        elif modelo == 'rf':
            clf = treinar_random_forest(X, y)
            codigo = gerar_random_forest_c(clf, features)
        elif modelo == 'svm':
            clf, scaler = treinar_svm(X, y)
            codigo = gerar_svm_c(clf, scaler, features)
        
        if args.exportar in ['arquivo', 'todos']:
            filename = f"modelo_{modelo}.c"
            with open(filename, 'w') as f:
                f.write(codigo)
            print(f"✅ Salvo em: {filename}")
        else:
            print(codigo)
    
    # Código de integração
    if args.exportar in ['arquivo', 'todos']:
        with open("integracao.c", 'w') as f:
            f.write(gerar_codigo_integracao())
        print("✅ integracao.c salvo")
    
    # Relatório detalhado
    if args.avaliar:
        print(f"\n{'='*60}")
        print("📊 RELATÓRIO DETALHADO")
        print("="*60)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        for modelo in ['dt', 'rf', 'svm']:
            print(f"\n--- {CONFIG_MODELOS[modelo]['nome']} ---")
            
            if modelo == 'dt':
                clf = treinar_decision_tree(X_train, y_train)
                y_pred = clf.predict(X_test)
            elif modelo == 'rf':
                clf = treinar_random_forest(X_train, y_train)
                y_pred = clf.predict(X_test)
            elif modelo == 'svm':
                clf, scaler = treinar_svm(X_train, y_train)
                y_pred = clf.predict(scaler.transform(X_test))
            
            print(classification_report(y_test, y_pred,
                  target_names=[NOMES_CLASSES[i] for i in sorted(NOMES_CLASSES.keys())]))
    
    print("\n✅ Concluído!")

if __name__ == "__main__":
    main()
import streamlit as st
import serial
import pandas as pd
import time
import serial.tools.list_ports

# --- CONFIGURAÇÃO ---
# Se souber a porta fixa, coloque aqui (ex: 'COM4'). Se deixar None, ele tenta achar.
PORTA_PADRAO = 'COM4' 
BAUD_RATE = 115200

# Configuração da Página
st.set_page_config(page_title="BME688 Research Lab", layout="wide")
st.title("🌱 Monitoramento de Plantas em Tempo Real")

# Sidebar para conexão
st.sidebar.header("Conexão")
portas_disponiveis = [p.device for p in serial.tools.list_ports.comports()]
porta_selecionada = st.sidebar.selectbox("Selecione a Porta COM", portas_disponiveis, index=0 if portas_disponiveis else None)
conectar = st.sidebar.button("Iniciar Leitura")
parar = st.sidebar.button("Parar")

# Containers para Gráficos
col1, col2 = st.columns(2)
with col1:
    st.subheader("🌡️ Clima (Temp/Umid)")
    chart_clima = st.line_chart([])
with col2:
    st.subheader("💨 Resistência dos Gases (10 Passos)")
    chart_gas = st.line_chart([])

st.subheader("📋 Dados Recentes")
tabela_dados = st.empty()

# Estado da Sessão (para manter os dados na memória)
if 'dados' not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=['Index', 'Temp', 'Umid'] + [f'G{t}' for t in [320,295,270,245,220,195,170,145,120,100]])
if 'lendo' not in st.session_state:
    st.session_state.lendo = False

if conectar:
    st.session_state.lendo = True

if parar:
    st.session_state.lendo = False

# Loop de Leitura
if st.session_state.lendo and porta_selecionada:
    try:
        # Abre conexão (se já não estiver aberta na lógica do script)
        ser = serial.Serial(porta_selecionada, BAUD_RATE, timeout=0.1)
        st.success(f"Conectado em {porta_selecionada}!")
        
        placeholder = st.empty()
        
        while st.session_state.lendo:
            if ser.in_waiting > 0:
                try:
                    linha = ser.readline().decode('utf-8', errors='ignore').strip()
                    if linha and linha[0].isdigit():
                        partes = linha.split(',')
                        if len(partes) >= 13:
                            # Converte para numeros
                            valores = [float(x) for x in partes]
                            
                            # Cria dicionário da nova linha
                            nova_linha = {
                                'Index': valores[0],
                                'Temp': valores[1],
                                'Umid': valores[2]
                            }
                            # Adiciona os 10 gases
                            temps = [320,295,270,245,220,195,170,145,120,100]
                            for i, t in enumerate(temps):
                                nova_linha[f'G{t}'] = valores[3+i]
                            
                            # Adiciona ao DataFrame global
                            st.session_state.dados = pd.concat([st.session_state.dados, pd.DataFrame([nova_linha])], ignore_index=True)
                            
                            # Mantém apenas as ultimas 100 leituras para não travar
                            df_vis = st.session_state.dados.tail(100)
                            
                            # Atualiza Gráficos em Tempo Real
                            chart_clima.line_chart(df_vis[['Temp', 'Umid']])
                            
                            # Normaliza os gases para caberem no mesmo gráfico (opcional, mas ajuda)
                            cols_gas = [c for c in df_vis.columns if 'G' in c]
                            chart_gas.line_chart(df_vis[cols_gas])
                            
                            tabela_dados.dataframe(df_vis.tail(5))
                            
                except ValueError:
                    pass
            
            time.sleep(0.05) # Pequena pausa para não explodir a CPU
            
    except Exception as e:
        st.error(f"Erro na conexão: {e}")
        st.session_state.lendo = False  
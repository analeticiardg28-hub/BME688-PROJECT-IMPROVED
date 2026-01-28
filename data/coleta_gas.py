#!/usr/bin/env python3
"""
=============================================================================
COLETOR DE DADOS BME688 - COM PAUSA/RETOMADA
=============================================================================
Funcionalidades:
- Pausar/retomar coleta com tecla ESPAÇO
- Continuar coleta no mesmo arquivo em sessões diferentes
- Suporte a múltiplas amostras/espécimes
- Timestamp e metadados completos
=============================================================================
"""

import serial
import csv
import os
import sys
import threading
import time
from datetime import datetime

# Tenta importar keyboard para detectar teclas (opcional)
try:
    import keyboard
    KEYBOARD_DISPONIVEL = True
except ImportError:
    KEYBOARD_DISPONIVEL = False
    print("⚠️  Módulo 'keyboard' não instalado. Use Ctrl+C para parar.")
    print("   Instale com: pip install keyboard")

# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

PORTA_SERIAL = 'COM4'  # Altere conforme necessário
BAUD_RATE = 115200
TIMEOUT = 2

# Diretório base para dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cabeçalho do CSV
CABECALHO = [
    'timestamp', 'sessao_id', 'amostra_id', 'classe',
    'temp', 'umid',
    'G320', 'G295', 'G270', 'G245', 'G220',
    'G195', 'G170', 'G145', 'G120', 'G100',
    'notas'
]

# =============================================================================
# CLASSE PRINCIPAL
# =============================================================================

class ColetorBME688:
    def __init__(self):
        self.pausado = False
        self.rodando = True
        self.contador = 0
        self.ser = None
        
    def conectar_serial(self, porta):
        """Conecta à porta serial."""
        try:
            self.ser = serial.Serial(porta, BAUD_RATE, timeout=TIMEOUT)
            print(f"✅ Conectado a {porta}")
            return True
        except serial.SerialException as e:
            print(f"❌ Erro ao conectar em {porta}: {e}")
            return False
    
    def listar_portas(self):
        """Lista portas seriais disponíveis."""
        import serial.tools.list_ports
        portas = list(serial.tools.list_ports.comports())
        if portas:
            print("\n📟 Portas disponíveis:")
            for p in portas:
                print(f"   - {p.device}: {p.description}")
        else:
            print("❌ Nenhuma porta serial encontrada")
        return portas
    
    def toggle_pausa(self):
        """Alterna estado de pausa."""
        self.pausado = not self.pausado
        if self.pausado:
            print("\n⏸️  PAUSADO - Pressione ESPAÇO para continuar")
        else:
            print("\n▶️  CONTINUANDO coleta...")
    
    def parar(self):
        """Para a coleta."""
        self.rodando = False
        print("\n🛑 Parando coleta...")
    
    def coletar(self, arquivo_csv, classe, amostra_id, notas=""):
        """Loop principal de coleta."""
        
        # Gerar ID de sessão único
        sessao_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Verificar se arquivo existe
        arquivo_existe = os.path.exists(arquivo_csv)
        
        # Contar linhas existentes para continuar numeração
        if arquivo_existe:
            with open(arquivo_csv, 'r') as f:
                self.contador = sum(1 for _ in f) - 1  # -1 para cabeçalho
            print(f"📄 Continuando arquivo existente ({self.contador} leituras anteriores)")
        
        # Abrir arquivo para append
        with open(arquivo_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Escrever cabeçalho se arquivo novo
            if not arquivo_existe:
                writer.writerow(CABECALHO)
            
            print(f"\n📊 Coletando dados:")
            print(f"   Arquivo: {arquivo_csv}")
            print(f"   Classe: {classe}")
            print(f"   Amostra: {amostra_id}")
            print(f"   Sessão: {sessao_id}")
            print("-" * 50)
            
            if KEYBOARD_DISPONIVEL:
                print("⌨️  ESPAÇO = pausar/continuar | ESC = parar")
                keyboard.on_press_key('space', lambda _: self.toggle_pausa())
                keyboard.on_press_key('esc', lambda _: self.parar())
            else:
                print("⌨️  Ctrl+C = parar")
            
            print("-" * 50)
            
            try:
                while self.rodando:
                    # Se pausado, aguardar
                    if self.pausado:
                        time.sleep(0.1)
                        continue
                    
                    # Ler linha da serial
                    try:
                        linha = self.ser.readline().decode('utf-8').strip()
                    except UnicodeDecodeError:
                        continue
                    
                    if not linha:
                        continue
                    
                    # Parse dos dados
                    partes = linha.split(',')
                    if len(partes) < 12:
                        continue
                    
                    # Validar dados numéricos
                    try:
                        temp = float(partes[0])
                        umid = float(partes[1])
                        gases = [float(partes[i]) for i in range(2, 12)]
                    except ValueError:
                        continue
                    
                    # Timestamp
                    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Montar linha
                    row = [
                        ts,
                        sessao_id,
                        amostra_id,
                        classe,
                        f"{temp:.1f}",
                        f"{umid:.1f}",
                        *[f"{g:.0f}" for g in gases],
                        notas
                    ]
                    
                    # Escrever
                    writer.writerow(row)
                    f.flush()
                    
                    self.contador += 1
                    
                    # Mostrar progresso
                    print(f"[{self.contador:4d}] {ts} | T={temp:5.1f}°C | "
                          f"U={umid:4.1f}% | G100={gases[9]:,.0f}")
                    
            except KeyboardInterrupt:
                pass
            
            finally:
                if KEYBOARD_DISPONIVEL:
                    keyboard.unhook_all()
        
        print(f"\n✅ Coleta finalizada!")
        print(f"   Total de leituras: {self.contador}")
        print(f"   Arquivo: {arquivo_csv}")
    
    def fechar(self):
        """Fecha conexão serial."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("📟 Porta serial fechada")


# =============================================================================
# MENU INTERATIVO
# =============================================================================

def menu_principal():
    """Menu interativo para coleta."""
    
    coletor = ColetorBME688()
    
    print("=" * 60)
    print("🌿 COLETOR DE DADOS BME688 - NARIZ ELETRÔNICO")
    print("=" * 60)
    
    # Listar portas disponíveis
    coletor.listar_portas()
    
    # Configurar porta
    porta = input(f"\n📟 Porta serial [{PORTA_SERIAL}]: ").strip()
    if not porta:
        porta = PORTA_SERIAL
    
    if not coletor.conectar_serial(porta):
        return
    
    try:
        while True:
            print("\n" + "=" * 60)
            print("📋 MENU PRINCIPAL")
            print("=" * 60)
            print("1. Nova coleta (criar novo arquivo)")
            print("2. Continuar coleta (arquivo existente)")
            print("3. Listar arquivos de dados")
            print("0. Sair")
            
            opcao = input("\nEscolha: ").strip()
            
            if opcao == '0':
                break
            
            elif opcao == '1':
                # Nova coleta
                print("\n📝 NOVA COLETA")
                print("-" * 40)
                
                classe = input("Classe (ex: planta, ar_neutro, doente): ").strip().lower()
                if not classe:
                    print("❌ Classe não pode ser vazia")
                    continue
                
                amostra_id = input("ID da amostra (ex: manjericao_01, ar_sala_01): ").strip()
                if not amostra_id:
                    amostra_id = f"{classe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    print(f"   ID gerado: {amostra_id}")
                
                notas = input("Notas (opcional): ").strip()
                
                # Nome do arquivo
                arquivo_padrao = f"{classe}_{amostra_id}.csv"
                arquivo = input(f"Nome do arquivo [{arquivo_padrao}]: ").strip()
                if not arquivo:
                    arquivo = arquivo_padrao
                
                arquivo_path = os.path.join(BASE_DIR, arquivo)
                
                if os.path.exists(arquivo_path):
                    resp = input(f"⚠️  Arquivo existe. Sobrescrever? (s/N): ").strip().lower()
                    if resp != 's':
                        continue
                    os.remove(arquivo_path)
                
                coletor.rodando = True
                coletor.pausado = False
                coletor.contador = 0
                coletor.coletar(arquivo_path, classe, amostra_id, notas)
            
            elif opcao == '2':
                # Continuar coleta
                print("\n📂 CONTINUAR COLETA")
                print("-" * 40)
                
                # Listar arquivos CSV
                arquivos = [f for f in os.listdir(BASE_DIR) if f.endswith('.csv')]
                if not arquivos:
                    print("❌ Nenhum arquivo CSV encontrado")
                    continue
                
                print("Arquivos disponíveis:")
                for i, arq in enumerate(arquivos, 1):
                    # Contar linhas
                    path = os.path.join(BASE_DIR, arq)
                    with open(path, 'r') as f:
                        linhas = sum(1 for _ in f) - 1
                    print(f"  {i}. {arq} ({linhas} leituras)")
                
                escolha = input("\nNúmero do arquivo (ou nome): ").strip()
                
                try:
                    idx = int(escolha) - 1
                    arquivo = arquivos[idx]
                except (ValueError, IndexError):
                    arquivo = escolha
                
                arquivo_path = os.path.join(BASE_DIR, arquivo)
                
                if not os.path.exists(arquivo_path):
                    print(f"❌ Arquivo não encontrado: {arquivo}")
                    continue
                
                # Ler metadados do arquivo existente
                with open(arquivo_path, 'r') as f:
                    reader = csv.DictReader(f)
                    primeira_linha = next(reader, None)
                    if primeira_linha:
                        classe = primeira_linha.get('classe', 'desconhecida')
                        amostra_id = primeira_linha.get('amostra_id', 'desconhecido')
                        print(f"   Classe: {classe}")
                        print(f"   Amostra: {amostra_id}")
                    else:
                        classe = input("Classe: ").strip()
                        amostra_id = input("Amostra ID: ").strip()
                
                notas = input("Notas para esta sessão (opcional): ").strip()
                
                coletor.rodando = True
                coletor.pausado = False
                coletor.coletar(arquivo_path, classe, amostra_id, notas)
            
            elif opcao == '3':
                # Listar arquivos
                print("\n📂 ARQUIVOS DE DADOS")
                print("-" * 40)
                
                arquivos = [f for f in os.listdir(BASE_DIR) if f.endswith('.csv')]
                if not arquivos:
                    print("Nenhum arquivo CSV encontrado")
                else:
                    for arq in arquivos:
                        path = os.path.join(BASE_DIR, arq)
                        with open(path, 'r') as f:
                            linhas = sum(1 for _ in f) - 1
                        size_kb = os.path.getsize(path) / 1024
                        print(f"  📄 {arq}: {linhas} leituras ({size_kb:.1f} KB)")
    
    finally:
        coletor.fechar()
    
    print("\n👋 Até mais!")


# =============================================================================
# PONTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    menu_principal()
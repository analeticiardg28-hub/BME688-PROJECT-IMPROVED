# 🌿 BME688 - Nariz Eletrônico para Detecção de Plantas

Um projeto completo para criar um "nariz eletrônico" usando o sensor BME688 e Raspberry Pi Pico. O sistema consegue detectar e classificar odores usando Inteligência Artificial embarcada no próprio microcontrolador.

---

## 📖 O Que Este Projeto Faz?

Imagine um dispositivo capaz de "cheirar" o ambiente e identificar se há uma planta por perto, ou se o ar está neutro. É exatamente isso que este projeto faz!

### Como funciona (explicação simples):

1. **O sensor aquece** uma pequena placa metálica em diferentes temperaturas (de 320°C até 100°C)
2. **Em cada temperatura**, ele mede a resistência elétrica do ar
3. **Plantas liberam gases** (chamados VOCs - Compostos Orgânicos Voláteis) que alteram essa resistência
4. **A Inteligência Artificial** aprende o "padrão" de cada tipo de odor
5. **O sistema classifica** automaticamente: "É planta!" ou "É ar neutro!"

---

## 🛒 O Que Você Vai Precisar Comprar

### Lista de Compras

| Item | Preço Aproximado | Onde Comprar |
|------|------------------|--------------|
| Raspberry Pi Pico | R$ 30-50 | AliExpress, Mercado Livre |
| Sensor BME688 (Waveshare) | R$ 80-120 | AliExpress, Mercado Livre |
| Cabo Micro USB | R$ 10-20 | Qualquer loja |
| Jumpers Fêmea-Fêmea (4 unidades) | R$ 5-10 | Lojas de eletrônica |

**Total aproximado: R$ 125-200**

### Sobre o Raspberry Pi Pico

O Raspberry Pi Pico é um microcontrolador pequeno e barato. Ele é o "cérebro" do projeto - executa o código e processa os dados do sensor.

- **Não é** um Raspberry Pi comum (aquele que roda Linux)
- **É** um microcontrolador simples, como um Arduino, mas mais potente
- Pode ser o Pico normal ou o Pico W (com WiFi) - ambos funcionam

### Sobre o Sensor BME688

O BME688 é um sensor especial da Bosch que mede:
- Temperatura
- Umidade
- Pressão atmosférica
- **Gases/VOCs** (essa é a parte importante para nós!)

**IMPORTANTE**: Compre a versão **Waveshare** do BME688, que já vem em uma plaquinha pronta para usar.

---

## 🔌 Como Conectar os Fios

Esta é uma das partes mais importantes! Conecte os fios assim:

```
RASPBERRY PI PICO                    SENSOR BME688
┌─────────────────┐                  ┌───────────┐
│                 │                  │           │
│  3V3 (pino 36) ├──── fio vermelho ────► VCC   │
│                 │                  │           │
│  GND (pino 38) ├──── fio preto ───────► GND   │
│                 │                  │           │
│  GP0 (pino 1)  ├──── fio amarelo ─────► SDA   │
│                 │                  │           │
│  GP1 (pino 2)  ├──── fio laranja ─────► SCL   │
│                 │                  │           │
└─────────────────┘                  └───────────┘
```

### Encontrando os Pinos no Pico

O Raspberry Pi Pico tem 40 pinos. Olhando para ele com a porta USB para cima:

```
                    ┌─────────────────┐
              USB ──┤█████████████████├── USB
                    ├─────────────────┤
         GP0 (SDA) ─┤ 1             40├─ VBUS
         GP1 (SCL) ─┤ 2             39├─ VSYS
              GND ──┤ 3             38├─ GND ◄── Use este GND
             GP2  ──┤ 4             37├─ 3V3_EN
             GP3  ──┤ 5             36├─ 3V3 ◄── Use este 3V3
               ...  │ ...          ...│
                    └─────────────────┘
```

### Dicas de Conexão

1. **Desligue tudo** antes de conectar os fios
2. **Confira duas vezes** antes de ligar - fio errado pode queimar o sensor!
3. Os fios devem ficar **firmes** nos pinos
4. Se usar jumpers fêmea-fêmea, conecte direto nos pinos

---

## 💻 Instalando os Programas no Computador

Você vai precisar instalar alguns programas no seu computador. Siga o passo a passo do seu sistema operacional.

### Para Windows

#### Passo 1: Instalar o Python

1. Acesse: https://www.python.org/downloads/
2. Clique no botão amarelo "Download Python 3.x.x"
3. Execute o instalador baixado
4. **IMPORTANTE**: Marque a opção ✅ "Add Python to PATH"
5. Clique em "Install Now"
6. Aguarde a instalação terminar

**Para verificar se funcionou:**
1. Abra o Prompt de Comando (digite "cmd" no menu iniciar)
2. Digite: `python --version`
3. Deve aparecer algo como: `Python 3.11.5`

#### Passo 2: Instalar o VS Code (Editor de Código)

1. Acesse: https://code.visualstudio.com/
2. Clique em "Download for Windows"
3. Execute o instalador
4. Siga as instruções (pode deixar tudo padrão)

#### Passo 3: Instalar Ferramentas de Compilação (para o firmware)

Se você quiser modificar o código do Pico (opcional no início):

1. **CMake**: https://cmake.org/download/ (baixe o .msi)
2. **ARM GCC**: https://developer.arm.com/downloads/-/gnu-rm
3. **Ninja**: https://ninja-build.org/ (extraia e adicione ao PATH)

### Para Linux (Ubuntu/Debian)

Abra o terminal e execute:

```bash
# Atualizar o sistema
sudo apt update

# Instalar Python e ferramentas
sudo apt install python3 python3-pip python3-venv

# Instalar ferramentas de compilação (opcional)
sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential

# Instalar VS Code
sudo snap install code --classic
```

### Para macOS

```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python

# Instalar ferramentas (opcional)
brew install cmake ninja armmbed/formulae/arm-none-eabi-gcc
```

---

## 📂 Baixando e Configurando o Projeto

### Passo 1: Baixar o Projeto

Você pode baixar de duas formas:

**Opção A - Download direto (mais fácil):**
1. Acesse o repositório do projeto
2. Clique no botão verde "Code"
3. Clique em "Download ZIP"
4. Extraia o ZIP em uma pasta (ex: `C:\BME688-Project`)

**Opção B - Usando Git:**
```bash
git clone <url-do-repositorio>
cd BME688-Project
```

### Passo 2: Abrir no VS Code

1. Abra o VS Code
2. Vá em File → Open Folder
3. Selecione a pasta do projeto (ex: `C:\BME688-Project`)

### Passo 3: Configurar o Ambiente Python

Abra o terminal no VS Code (menu Terminal → New Terminal) e execute:

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual
# No Windows:
.venv\Scripts\activate

# No Linux/Mac:
source .venv/bin/activate

# Instalar as bibliotecas necessárias
pip install pandas numpy scikit-learn pyserial keyboard matplotlib
```

**Você saberá que funcionou quando:**
- Aparecer `(.venv)` no início da linha do terminal
- O comando `pip install` terminar sem erros vermelhos

---

## 🔥 Gravando o Firmware no Pico

O "firmware" é o programa que roda dentro do Raspberry Pi Pico. Vamos gravar!

### Passo 1: Colocar o Pico em Modo de Gravação

1. **Desconecte** o cabo USB do Pico (se estiver conectado)
2. **Encontre** o botão pequeno chamado "BOOTSEL" no Pico
3. **Pressione e segure** o botão BOOTSEL
4. **Conecte** o cabo USB no computador (mantendo o botão pressionado)
5. **Solte** o botão após conectar

**Se funcionou:**
- Uma nova unidade aparecerá no seu computador chamada "RPI-RP2"
- É como se fosse um pendrive!

### Passo 2: Copiar o Firmware

1. Abra a pasta `firmware/build/` do projeto
2. Encontre o arquivo `bme688_test.uf2`
3. **Copie** este arquivo para a unidade "RPI-RP2"
4. O Pico vai reiniciar automaticamente

**Se não encontrar o arquivo .uf2:**
O firmware precisa ser compilado primeiro. Veja a seção "Compilando o Firmware" mais abaixo.

### Passo 3: Verificar se Funcionou

1. Abra um programa de monitor serial:
   - **Windows**: PuTTY, ou o próprio VS Code com extensão Serial Monitor
   - **Linux**: `screen /dev/ttyACM0 115200` ou VS Code

2. Configure:
   - Porta: COM3, COM4, etc. (Windows) ou /dev/ttyACM0 (Linux)
   - Velocidade: 115200

3. Você deve ver dados aparecendo na tela!

---

## 📊 Coletando Dados para Treinar a IA

Agora vem a parte divertida! Vamos coletar dados para ensinar a IA.

### Entendendo o Processo

A IA precisa de **exemplos** para aprender. Vamos coletar:
- Várias leituras com o sensor **perto de uma planta** → classe "planta"
- Várias leituras com o sensor no **ar normal** → classe "ar_neutro"

Quanto mais exemplos, melhor a IA aprende!

### Passo 1: Executar o Coletor

```bash
# Certifique-se de estar na pasta do projeto
cd C:\BME688-Project\data

# Ative o ambiente virtual (se não estiver ativo)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Execute o coletor
python coleta_gas.py
```

### Passo 2: Usar o Menu

Você verá um menu assim:

```
============================================================
🌿 COLETOR DE DADOS BME688 - NARIZ ELETRÔNICO
============================================================

📟 Portas disponíveis:
   - COM4: USB Serial Device

📟 Porta serial [COM4]: 
```

1. Digite a porta correta (ou pressione Enter para usar a padrão)
2. Escolha "1" para nova coleta

### Passo 3: Coletar Dados de "Planta"

1. Escolha opção "1. Nova coleta"
2. Digite a classe: `planta`
3. Digite um ID: `manjericao_01` (ou o nome da sua planta)
4. Posicione o sensor a 5-10 cm da planta
5. Deixe coletando por alguns minutos (mínimo 100 leituras)
6. Pressione **ESPAÇO** para pausar ou **ESC** para parar

### Passo 4: Coletar Dados de "Ar Neutro"

1. Afaste o sensor de qualquer planta
2. Escolha opção "1. Nova coleta"
3. Digite a classe: `ar_neutro`
4. Digite um ID: `ar_sala_01`
5. Colete a mesma quantidade de dados

### ⚠️ DICAS MUITO IMPORTANTES

> **A qualidade dos dados é CRUCIAL!** Siga estas dicas:

1. **Mesmas condições**: Colete planta e ar_neutro no **mesmo dia/horário**
2. **Distância fixa**: Mantenha sempre 5-10 cm de distância
3. **Aguarde estabilizar**: O sensor leva 2-3 minutos para esquentar
4. **Quantidade**: Colete pelo menos 100 leituras de cada classe
5. **Variedade**: Se possível, colete de plantas diferentes

---

## 🧠 Treinando a Inteligência Artificial

Com os dados coletados, vamos treinar o modelo!

### Passo 1: Configurar os Arquivos de Dados

Abra o arquivo `IA/treinar_scanner.py` e edite a seção de configuração:

```python
# Encontre esta parte no arquivo e edite:
ARQUIVOS = {
    0: [
        '../data/planta_manjericao_01.csv',    # Seus arquivos de planta
        # '../data/planta_alecrim_01.csv',     # Adicione mais se tiver
    ],
    1: [
        '../data/ar_neutro_sala_01.csv',       # Seus arquivos de ar neutro
        # '../data/ar_neutro_quarto_01.csv',   # Adicione mais se tiver
    ],
}
```

### Passo 2: Executar o Treinamento

```bash
cd C:\BME688-Project\IA
python treinar_scanner.py
```

### Passo 3: Entender os Resultados

O script vai mostrar algo assim:

```
============================================================
🧠 TREINADOR MULTI-MODELO PARA BME688
============================================================

📂 CARREGANDO DADOS
============================================================

🏷️  PLANTA (1 arquivo(s))
   ✅ planta_manjericao_01.csv: 150 amostras

🏷️  AR_NEUTRO (1 arquivo(s))
   ✅ ar_neutro_sala_01.csv: 148 amostras

📊 RESUMO DOS DADOS
============================================================
Classe          Amostras   Porcentagem
----------------------------------------
PLANTA               150        50.3%
AR_NEUTRO            148        49.7%
----------------------------------------
TOTAL                298

📈 AVALIAÇÃO DOS MODELOS (5-fold cross-validation)
============================================================

🌳 Decision Tree:  87.25% ± 3.45%
🌲 Random Forest:  91.12% ± 2.87%
📐 SVM Linear:     93.45% ± 2.15%

🏆 Melhor modelo: SVM Linear
```

### O Que Significam Esses Números?

- **87.25%** = O modelo acerta 87 de cada 100 classificações
- **± 3.45%** = A variação (quanto menor, mais consistente)
- **Melhor modelo** = Use este para o firmware!

### Passo 4: Gerar o Código para o Pico

Para gerar os arquivos de código:

```bash
# Gerar apenas o melhor modelo
python treinar_scanner.py --modelo svm

# Ou gerar todos os modelos
python treinar_scanner.py --exportar todos
```

Isso cria os arquivos:
- `modelo_dt.c` - Decision Tree
- `modelo_rf.c` - Random Forest
- `modelo_svm.c` - SVM Linear
- `integracao.c` - Código auxiliar

---

## 🔧 Integrando o Modelo no Firmware

Agora vamos colocar a IA no Pico!

### Passo 1: Abrir o main.c

Abra o arquivo `firmware/src/main.c` no VS Code.

### Passo 2: Copiar o Código do Modelo

1. Abra o arquivo `IA/modelo_svm.c` (ou o modelo escolhido)
2. Copie **todo o conteúdo**
3. Cole no `main.c`, antes da função `main()`

### Passo 3: Copiar o Código de Integração

1. Abra o arquivo `IA/integracao.c`
2. Copie as funções `identificar()` e `NOMES_CLASSES`
3. Cole no `main.c`

### Passo 4: Modificar o Loop Principal

No final do arquivo `main.c`, dentro do `while(true)`, adicione:

```c
// Após coletar os dados de gás, adicione:
int classe = identificar(gas_values);
printf(">>> Classe detectada: %s <<<\n", NOMES_CLASSES[classe]);
```

### Passo 5: Recompilar e Gravar

```bash
cd firmware/build
cmake ..
ninja
```

Depois copie o novo `bme688_test.uf2` para o Pico.

---

## 🔨 Compilando o Firmware (Passo a Passo Detalhado)

Se você precisar compilar o firmware do zero:

### Passo 1: Baixar o Pico SDK

```bash
# No terminal, vá para uma pasta onde quer guardar o SDK
cd C:\

# Clone o SDK
git clone https://github.com/raspberrypi/pico-sdk.git

# Entre na pasta e baixe as dependências
cd pico-sdk
git submodule update --init
```

### Passo 2: Configurar a Variável de Ambiente

**Windows (PowerShell):**
```powershell
$env:PICO_SDK_PATH = "C:\pico-sdk"
```

**Windows (CMD):**
```cmd
set PICO_SDK_PATH=C:\pico-sdk
```

**Linux/Mac:**
```bash
export PICO_SDK_PATH=$HOME/pico-sdk
```

**Para tornar permanente no Windows:**
1. Pesquise "variáveis de ambiente" no menu iniciar
2. Clique em "Variáveis de Ambiente"
3. Em "Variáveis do sistema", clique "Novo"
4. Nome: `PICO_SDK_PATH`
5. Valor: `C:\pico-sdk`

### Passo 3: Compilar

```bash
# Entre na pasta do firmware
cd C:\BME688-Project\firmware

# Crie a pasta de build (se não existir)
mkdir build
cd build

# Gere os arquivos de compilação
cmake ..

# Compile
ninja
```

**Se der erro no cmake:**
- Verifique se o PICO_SDK_PATH está correto
- Verifique se o ARM GCC está instalado
- Verifique se o Ninja está no PATH

### Passo 4: Encontrar o Arquivo Compilado

Se tudo der certo, você encontrará:
```
firmware/build/bme688_test.uf2
```

Este é o arquivo que você copia para o Pico!

---

## 🐛 Resolvendo Problemas Comuns

### "Não encontra a porta serial"

**Windows:**
1. Abra o Gerenciador de Dispositivos
2. Procure em "Portas (COM e LPT)"
3. Deve aparecer algo como "USB Serial Device (COM4)"

**Linux:**
```bash
ls /dev/tty*
# Procure por ttyACM0 ou ttyUSB0
```

**Se não aparecer nada:**
- Verifique se o cabo USB é de dados (não só de carga)
- Tente outra porta USB
- Reinstale os drivers

### "Erro: No module named 'serial'"

```bash
pip install pyserial
```

### "A classificação está sempre errada"

Isso geralmente significa que os dados de treino não são bons:

1. **Colete novamente** com planta e ar_neutro nas **mesmas condições**
2. **Aproxime o sensor** - deve ficar a 5-10 cm da planta
3. **Aguarde estabilizar** - deixe o sensor ligado 5 min antes de coletar

### "O sensor retorna valores zerados"

1. Verifique as conexões dos fios
2. Confira se não inverteu SDA/SCL
3. Verifique se a alimentação é 3.3V (não 5V!)

### "Erro de compilação do firmware"

```bash
# Limpe e recompile
cd firmware/build
rm -rf *
cmake ..
ninja
```

---

## 📁 Estrutura das Pastas do Projeto

```
BME688-Project/
│
├── firmware/                 # Código do Raspberry Pi Pico
│   ├── src/
│   │   └── main.c           # Programa principal
│   ├── lib/
│   │   └── bme68x/          # Biblioteca do sensor (da Bosch)
│   ├── platform/
│   │   ├── i2c_port.c       # Comunicação I2C
│   │   └── i2c_port.h
│   ├── build/
│   │   └── bme688_test.uf2  # Firmware compilado (copie para o Pico)
│   └── CMakeLists.txt       # Configuração de compilação
│
├── data/                     # Coleta de dados
│   ├── coleta_gas.py        # Script para coletar dados
│   ├── dashboard.py         # Visualização em tempo real
│   └── *.csv                # Arquivos de dados coletados
│
├── IA/                       # Inteligência Artificial
│   ├── treinar_scanner.py   # Script de treinamento
│   ├── modelo_dt.c          # Código gerado - Decision Tree
│   ├── modelo_rf.c          # Código gerado - Random Forest
│   ├── modelo_svm.c         # Código gerado - SVM
│   └── integracao.c         # Código auxiliar
│
├── .venv/                    # Ambiente virtual Python (criado por você)
│
└── README.md                 # Este arquivo!
```

---

## 🎓 Glossário - Termos Técnicos Explicados

| Termo | O Que Significa |
|-------|-----------------|
| **Firmware** | Programa que roda dentro do microcontrolador |
| **I2C** | Protocolo de comunicação entre o Pico e o sensor (usa 2 fios) |
| **VOC** | Volatile Organic Compounds - gases que plantas e objetos liberam |
| **SDA/SCL** | Fios de dados (SDA) e clock (SCL) da comunicação I2C |
| **Machine Learning** | Técnica onde o computador "aprende" com exemplos |
| **Decision Tree** | Algoritmo simples de IA que faz perguntas em sequência |
| **Random Forest** | Várias Decision Trees votando juntas |
| **SVM** | Support Vector Machine - algoritmo que separa dados por uma linha |
| **Cross-validation** | Técnica para testar se o modelo é bom |
| **Ambiente Virtual** | Pasta isolada com as bibliotecas Python do projeto |

---

## 🛡️ Cuidados Importantes

### Com o Sensor

- ⚠️ **NUNCA** molhe o sensor - água danifica permanentemente!
- ⚠️ **NUNCA** use 5V - apenas 3.3V
- ⚠️ **EVITE** tocar na parte metálica do sensor
- ✅ Aguarde 5 minutos após ligar para leituras estáveis
- ✅ Mantenha longe de correntes de ar fortes

### Com o Pico

- ⚠️ **NUNCA** conecte fios com o USB ligado
- ⚠️ **CONFIRA** as conexões antes de ligar
- ✅ Use uma superfície não-condutora (madeira, plástico)

---

## 🚀 Próximos Passos

Depois que tudo estiver funcionando, você pode:

1. **Adicionar mais classes**: Detectar plantas doentes vs saudáveis
2. **Treinar com mais dados**: Quanto mais dados, melhor a precisão
3. **Criar um case**: Imprima uma caixinha 3D para o projeto
4. **Adicionar display**: Mostre a classificação em um LCD
5. **Usar WiFi**: Com o Pico W, envie dados para a nuvem

---

## 📚 Links Úteis

- [Documentação do Raspberry Pi Pico](https://www.raspberrypi.com/documentation/microcontrollers/)
- [Datasheet do BME688](https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme688/)
- [Tutorial Python para Iniciantes](https://docs.python.org/pt-br/3/tutorial/)
- [VS Code - Guia Inicial](https://code.visualstudio.com/docs/getstarted/introvideos)

---

## ❓ Perguntas Frequentes

**P: Posso usar outro sensor de gás?**
R: Este projeto é específico para o BME688. Outros sensores (MQ-2, MQ-135, etc.) precisariam de código diferente.

**P: Funciona com Arduino?**
R: O código atual é para Raspberry Pi Pico. Seria necessário adaptar para Arduino.

**P: Quanto custa montar tudo?**
R: Aproximadamente R$ 150-200 para os componentes básicos.

**P: Preciso saber programar?**
R: Para usar o projeto básico, não. Para modificar, conhecimento básico de Python e C ajuda.

**P: Posso detectar outros odores além de plantas?**
R: Sim! Basta coletar dados do odor desejado e treinar um novo modelo.

---

## 🤝 Precisa de Ajuda?

Se encontrar problemas:

1. Releia as instruções com calma
2. Verifique se seguiu todos os passos
3. Procure o erro na seção "Resolvendo Problemas"
4. Abra uma issue no repositório do projeto

---

**Feito com 🌱 para quem quer aprender sobre sensores e IA**

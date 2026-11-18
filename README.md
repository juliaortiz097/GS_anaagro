# GS_anaagro

# 🌱 ANA Agro — Assistente Inteligente para Monitoramento Agrícola

**FIAP | Global Solution 2026 | Maker Lab**

**Turma:** 4ESPF

## 👥 Integrantes

| Nome completo | RM |
|---|---|
| Julia Ortiz | RM550204 |
| Julia Palomari | RM551910 |
| Leticia Baptista | RM550289 |
| Vinicius Sobreira Borges | RM97767 |

## 🎥 Vídeo demonstrativo

**Link do vídeo:** EDITAR E COLOCAR AQUI

O vídeo apresenta a montagem do protótipo, os componentes utilizados, a integração entre Arduino e Python e o funcionamento da assistente por comandos de voz.


---

## 1. Sobre o projeto

A **ANA Agro** é uma assistente inteligente desenvolvida para facilitar o monitoramento das condições ambientais de plantações, especialmente no contexto dos pequenos produtores rurais.

A solução integra **inteligência artificial, reconhecimento de voz, sensores ambientais e robótica**, permitindo que o usuário consulte informações sobre sua plantação por meio de comandos de voz, sem precisar interpretar diretamente os dados técnicos dos sensores.

O objetivo é tornar o acesso à tecnologia mais simples, intuitivo e inclusivo, contribuindo para a transformação digital no agronegócio.

### Por que ANA?

O nome **ANA** foi escolhido por ser curto, fácil de memorizar e simples de pronunciar.

Com apenas três letras e duas vogais, buscamos facilitar sua ativação por comandos de voz, considerando também a acessibilidade para pessoas com dificuldades na fala.

Essa escolha representa o compromisso do projeto com a inclusão digital. A efetividade dessa proposta de acessibilidade ainda depende de testes com diferentes usuários e padrões de fala.

## 2. Objetivos

- Monitorar a temperatura e a umidade relativa do ar.
- Permitir consultas ambientais por comandos de voz.
- Integrar sensores físicos ao processamento de dados em Python.
- Interpretar as condições ambientais utilizando parâmetros configurados.
- Responder ao usuário por meio de síntese de voz.
- Demonstrar a integração entre robótica, sensores e recursos de inteligência artificial.

## 3. Componentes utilizados

### Hardware

| Componente | Função |
|---|---|
| Arduino Uno | Controlador responsável pela leitura do sensor e acionamento dos componentes físicos |
| Sensor DHT11 | Mede temperatura e umidade relativa do ar |
| Protoboard | Permite a montagem e conexão dos componentes |
| Jumpers | Realizam as conexões elétricas |
| LED | Sinalização visual do robô |
| Resistor para LED | Limita a corrente elétrica do LED |
| Motor DC | Permite o movimento físico do robô |
| Ponte H | Controla o acionamento e o sentido de rotação do motor |
| Cabo USB | Realiza a comunicação entre Arduino e computador |
| Computador com microfone e áudio | Executa o software, reconhece comandos e reproduz respostas |

### Software e tecnologias

- **Python 3.11:** linguagem principal da assistente.
- **Arduino IDE:** programação do microcontrolador.
- **VS Code:** desenvolvimento e execução do projeto.
- **PySerial:** comunicação serial entre Python e Arduino.
- **SpeechRecognition:** reconhecimento de comandos de voz.
- **PyAudio:** captura de áudio pelo microfone.
- **Edge TTS e Pygame:** geração e reprodução das respostas faladas.
- **Groq e/ou Ollama:** recursos de inteligência artificial utilizados pela ANA.
- **OpenCV:** recursos de visão computacional.
- **Biblioteca DHT da Adafruit:** leitura do sensor DHT11 no Arduino.

## 4. Arquitetura e funcionamento

A ANA Agro funciona por meio da integração entre software e hardware.

O usuário ativa a assistente pela palavra-chave **“ANA”** e realiza uma pergunta relacionada à plantação.

Quando identifica uma consulta ambiental, o sistema solicita os dados do sensor DHT11, conectado ao Arduino Uno.

O Arduino coleta a temperatura e a umidade relativa do ar e transmite essas informações ao computador pela comunicação serial USB.

O Python recebe os valores, interpreta os dados de acordo com os parâmetros definidos no projeto e gera uma resposta que é reproduzida por voz.

### Fluxo de funcionamento

**Usuário → Comando de voz → Reconhecimento de fala → ANA (Python) → Arduino → Sensor DHT11 → Comunicação serial → Análise ambiental → Resposta por voz**

### Exemplo de interação

**Usuário:** “ANA, quais são as condições da minha plantação?”

**ANA:** “A temperatura atual é de 25,3 graus e a umidade do ar está em 67 por cento. As condições ambientais estão dentro da faixa ideal configurada para a plantação.”

*Os valores apresentados são ilustrativos e variam conforme as leituras reais do sensor.*

## 5. Integração entre sensores e inteligência artificial

A integração ocorre em três etapas principais.

### Etapa 1 — Aquisição dos dados

O sensor DHT11 realiza a medição da temperatura e da umidade relativa do ar.

O Arduino utiliza a biblioteca DHT para coletar as informações e enviá-las pela porta serial, com velocidade de comunicação de 9600 baud.

### Etapa 2 — Processamento e interpretação

O módulo `hardware/robo.py` realiza a comunicação com o Arduino e obtém as leituras ambientais.

Em seguida, o módulo `agro.py` processa os dados e classifica a temperatura segundo limites configurados.

Para a demonstração, foram definidos os seguintes parâmetros:

| Temperatura | Classificação |
|---|---|
| Abaixo de 25 °C | Abaixo da faixa configurada |
| Entre 25 °C e 26 °C | Dentro da faixa configurada |
| Acima de 26 °C | Acima da faixa configurada |

**Observação:** esses valores são parâmetros experimentais utilizados na demonstração. Não representam condições ideais universais para todas as culturas agrícolas.

A umidade é apresentada ao usuário, mas não participa da classificação de temperatura nessa versão.

### Etapa 3 — Interação inteligente

A ANA utiliza reconhecimento de voz para identificar a solicitação do usuário e síntese de voz para apresentar a resposta.

O sistema também possui integração com recursos de inteligência artificial para outras interações da assistente.

No monitoramento agrícola, a classificação das condições ambientais é realizada por regras programadas, utilizando dados reais do sensor.

As consultas são iniciadas pelo usuário: a ANA não emite alertas ambientais espontaneamente nesta versão.

## 6. Conexões do Arduino

| Componente | Pino Arduino |
|---|---|
| DHT11 — DATA | D2 |
| DHT11 — VCC | 5V |
| DHT11 — GND | GND |
| LED | D7 |
| Ponte H — ENA | D5 |
| Ponte H — IN1 | D8 |
| Ponte H — IN2 | D9 |

O motor DC é conectado à saída da ponte H, com alimentação adequada ao conjunto e referência de terra comum com o Arduino.

Para o DHT11 de quatro pinos, o terceiro terminal permanece desconectado. Recomenda-se resistor pull-up de 4,7 kΩ a 10 kΩ entre DATA e VCC para melhorar a estabilidade da leitura.

## 7. Instalação e execução

### Pré-requisitos

- Python 3.11 instalado.
- Arduino IDE instalado.
- Arduino Uno conectado por USB.
- Sensor DHT11 e demais componentes conectados.
- Microfone e dispositivo de saída de áudio.
- Conexão com a internet para serviços externos utilizados pela assistente.

### Passo 1 — Clonar o repositório

```bash
git clone https://github.com/juliaortiz097/GS_anaagro.git
cd GS_anaagro
```

### Passo 2 — Criar um ambiente virtual

No Windows:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

### Passo 3 — Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### Passo 4 — Configurar o Arduino

1. Abrir o Arduino IDE.
2. Instalar as bibliotecas **DHT sensor library** e **Adafruit Unified Sensor**.
3. Abrir o código `.ino` do projeto.
4. Selecionar a placa Arduino Uno e a porta correspondente.
5. Enviar o código para o Arduino.
6. Confirmar as leituras de temperatura e umidade no Monitor Serial, configurado para 9600 baud.
7. Fechar o Monitor Serial antes de executar o Python.

### Passo 5 — Configurar o Python

No arquivo `hardware/robo.py`, conferir a porta serial utilizada pelo Arduino, como `COM3`, `COM4` ou `COM5`.

Configurar também as credenciais dos serviços de IA utilizados pelo projeto, quando necessárias, por meio de variáveis de ambiente, sem publicar chaves privadas no GitHub.

### Passo 6 — Executar a ANA Agro

No terminal, executar:

```bash
python main.py
```

Após a inicialização, utilizar o comando de ativação:

**“ANA, quais são as condições da minha plantação?”**

A assistente deverá consultar o sensor e responder com os valores ambientais obtidos.

## 8. Testes e validação

Os testes do protótipo incluem:

- Verificação da comunicação serial entre Arduino e Python.
- Leitura da temperatura e umidade pelo DHT11.
- Reconhecimento da palavra de ativação ANA.
- Reconhecimento de perguntas relacionadas à plantação.
- Classificação das leituras segundo os parâmetros configurados.
- Reprodução das respostas por áudio.
- Testes de acionamento do LED e do motor.
- Verificação do comportamento diante de falhas de leitura ou comunicação.

As condições ambientais podem ser alteradas de forma controlada para observar a resposta do sensor, respeitando seus limites de operação.

## 9. Impacto e CitizenTech

A ANA Agro busca aproximar pequenos produtores das tecnologias de monitoramento ambiental.

Sua interface por voz reduz a necessidade de navegar por telas ou interpretar diretamente dados técnicos, favorecendo uma experiência mais acessível.

O protótipo demonstra como sensores de baixo custo, automação e recursos de IA podem contribuir para soluções voltadas à agricultura.

Como evolução futura, o projeto poderá incorporar sensores de umidade do solo, parâmetros específicos por cultura, histórico de medições e recomendações agrícolas mais detalhadas.

---

**ANA Agro — Tecnologia, acessibilidade e inteligência para o campo.**

*Projeto acadêmico desenvolvido para a Global Solution 2026 da FIAP.*

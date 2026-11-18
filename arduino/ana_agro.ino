
#include <DHT.h>

// SENSOR DHT11
#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// PINOS CORRETOS
const int ENA = 5;
const int LED = 7;
const int IN1 = 8;
const int IN2 = 9;

// CONFIGURACOES
const int VELOCIDADE = 255; // PWM maximo

const unsigned long TEMPO_LED = 3000;
const unsigned long TEMPO_MOVIMENTO = 150;
const unsigned long PAUSA_MOTOR = 150;
const unsigned long INTERVALO_DHT = 2000;

unsigned long inicioAcao = 0;
unsigned long ultimaLeitura = 0;

int etapaMotor = 0;
bool ledAtivo = false;

void pararMotor() {
  analogWrite(ENA, 0);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}

void pararTudo() {
  pararMotor();
  digitalWrite(LED, LOW);
  ledAtivo = false;
  etapaMotor = 0;
}

void motorDireita() {
  pararMotor();
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, VELOCIDADE);
}

void motorEsquerda() {
  pararMotor();
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, VELOCIDADE);
}

void responderSim() {
  pararTudo();

  digitalWrite(LED, HIGH);
  ledAtivo = true;
  inicioAcao = millis();

  Serial.println("SIM: LED ligado por 3 segundos");
}

void responderNao() {
  pararTudo();

  motorDireita();
  etapaMotor = 1;
  inicioAcao = millis();

  Serial.println("NAO: movimento da cabeca");
}

void atualizarAcoes() {
  unsigned long agora = millis();

  if (ledAtivo && agora - inicioAcao >= TEMPO_LED) {
    digitalWrite(LED, LOW);
    ledAtivo = false;
  }

  if (etapaMotor == 1 &&
      agora - inicioAcao >= TEMPO_MOVIMENTO) {
    pararMotor();
    etapaMotor = 2;
    inicioAcao = agora;
  }
  else if (etapaMotor == 2 &&
           agora - inicioAcao >= PAUSA_MOTOR) {
    motorEsquerda();
    etapaMotor = 3;
    inicioAcao = agora;
  }
  else if (etapaMotor == 3 &&
           agora - inicioAcao >= TEMPO_MOVIMENTO) {
    pararMotor();
    etapaMotor = 0;
  }
}

void setup() {
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pararTudo();

  pinMode(DHTPIN, INPUT_PULLUP);
  dht.begin();

  Serial.println("ANA AGRO INICIADA");
}

void loop() {
  while (Serial.available() > 0) {
    char comando = Serial.read();

    if (comando == 'S') {
      responderSim();
    }
    else if (comando == 'N') {
      responderNao();
    }
    else if (comando == 'P') {
      pararTudo();
      Serial.println("PARADO");
    }
  }

  atualizarAcoes();

  if (millis() - ultimaLeitura >= INTERVALO_DHT) {
    ultimaLeitura = millis();

    float temperatura = dht.readTemperature();
    float umidade = dht.readHumidity();

    if (isnan(temperatura) || isnan(umidade)) {
      Serial.println("ERRO: DHT11 sem leitura");
    }
    else {
      Serial.println("-------- ANA AGRO --------");

      Serial.print("Temperatura: ");
      Serial.print(temperatura);
      Serial.println(" C");

      Serial.print("Umidade do ar: ");
      Serial.print(umidade);
      Serial.println(" %");

      Serial.println("--------------------------");
    }
  }
}

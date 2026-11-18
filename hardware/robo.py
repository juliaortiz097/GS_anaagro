import serial
import time


PORTA_ARDUINO = "COM5"
VELOCIDADE = 9600


arduino = None


def conectar_arduino():
    global arduino

    try:
        arduino = serial.Serial(
            PORTA_ARDUINO,
            VELOCIDADE,
            timeout=1
        )

        # Arduino costuma reiniciar ao abrir a porta serial
        time.sleep(2)

        print(f"Arduino conectado em {PORTA_ARDUINO}.")
        return True

    except Exception as erro:
        print(f"Não foi possível conectar ao Arduino: {erro}")
        arduino = None
        return False


def enviar_comando(comando):
    """
    Envia um caractere para o Arduino.

    S = resposta SIM
    N = resposta NÃO
    P = parar
    """

    if arduino is None:
        print("Arduino não está conectado.")
        return

    try:
        arduino.write(comando.encode())
        print(f"Comando enviado ao robô: {comando}")

    except Exception as erro:
        print(f"Erro ao enviar comando ao robô: {erro}")


def processar_resposta(resposta):
    """
    Analisa a resposta da ANA e decide
    qual ação física o robô deve executar.
    """

    if not resposta:
        return

    texto = resposta.lower().strip()

    if texto.startswith("sim"):
        enviar_comando("S")

    elif texto.startswith("não") or texto.startswith("nao"):
        enviar_comando("N")


if __name__ == "__main__":
    if conectar_arduino():
        print("Teste S")
        enviar_comando("S")

        time.sleep(3)

        print("Teste N")
        enviar_comando("N")




##AGRO


def ler_dht11(timeout_segundos=8):
    """
    Le temperatura e umidade usando a conexao
    serial ja aberta pelo robo.

    Retorna (temperatura, umidade) ou None.
    """
    if arduino is None or not arduino.is_open:
        print("Arduino nao conectado.")
        return None

    temperatura = None
    umidade = None

    inicio = time.monotonic()

    while time.monotonic() - inicio < timeout_segundos:
        linha = arduino.readline().decode(
            "utf-8", errors="replace"
        ).strip()

        if linha.startswith("Temperatura:"):
            try:
                temperatura = float(
                    linha.split(":")[1].split()[0]
                )
            except (ValueError, IndexError):
                temperatura = None

        elif linha.startswith("Umidade do ar:"):
            try:
                umidade = float(
                    linha.split(":")[1].split()[0]
                )
            except (ValueError, IndexError):
                umidade = None

        if temperatura is not None and umidade is not None:
            print(
                f"DHT11: {temperatura} C / {umidade}%"
            )
            return temperatura, umidade

    print("Tempo esgotado ao ler o DHT11.")
    return None

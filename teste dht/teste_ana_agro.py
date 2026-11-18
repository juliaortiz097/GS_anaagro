
import serial
import time
import re

from voz.falar import falar

# Use a mesma porta que funcionou no teste anterior
PORTA = "COM5"

def ler_sensor():
    with serial.Serial(PORTA, 9600, timeout=3) as arduino:
        time.sleep(2)

        temperatura = None
        umidade = None

        while True:
            linha = arduino.readline().decode(
                "utf-8", errors="replace"
            ).strip()

            print(linha)

            if linha.startswith("Temperatura:"):
                resultado = re.search(r"[\d.]+", linha)
                if resultado:
                    temperatura = float(resultado.group())

            if linha.startswith("Umidade do ar:"):
                resultado = re.search(r"[\d.]+", linha)
                if resultado:
                    umidade = float(resultado.group())

            if temperatura is not None and umidade is not None:
                return temperatura, umidade


try:
    print("ANA Agro iniciando...")

    temperatura, umidade = ler_sensor()

    resposta = (
        f"A temperatura atual é de {temperatura:.1f} graus "
        f"e a umidade do ar está em {umidade:.0f} por cento."
    )

    if temperatura >= 30:
        resposta += " Atenção! A temperatura está elevada."
    elif temperatura <= 15:
        resposta += " Atenção! A temperatura está baixa."
    else:
        resposta += " A temperatura está dentro da faixa de teste."

    falar(resposta)

except Exception as erro:
    print(f"Erro na ANA Agro: {erro}")

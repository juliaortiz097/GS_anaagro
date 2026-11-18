
import serial
import time

# Troque pela porta do seu Arduino
PORTA = "COM5"

try:
    arduino = serial.Serial(
        PORTA,
        9600,
        timeout=3
    )

    time.sleep(2)

    print("ANA Agro conectada ao Arduino!")
    print("Recebendo dados do DHT11...\n")

    while True:
        linha = arduino.readline().decode(
            "utf-8", errors="replace"
        ).strip()

        if linha:
            print(linha)

except serial.SerialException as erro:
    print("Erro de conexao:", erro)

except KeyboardInterrupt:
    print("\nTeste encerrado.")

finally:
    if "arduino" in locals() and arduino.is_open:
        arduino.close()

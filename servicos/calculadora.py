import re
import math


def calcular(comando):
    """
    Realiza operações matemáticas básicas recebidas por texto.

    Exemplos aceitos:
        calcular 10 + 5
        10 + 5
        10 mais 5
        quanto é 10 mais 5
        5 vezes 6
        20 dividido por 4
        raiz de 25
    """

    try:
        texto = comando.lower().strip()
        texto = texto.replace(",", ".")

        # Remove expressões que não fazem parte da conta
        expressoes_remover = [
            "calcular",
            "calcule",
            "quanto é",
            "quanto da",
            "quanto dá",
            "qual é o resultado de"
        ]

        for expressao in expressoes_remover:
            texto = texto.replace(expressao, "")

        texto = texto.strip()

        # Raiz quadrada
        if "raiz" in texto:
            numeros = re.findall(r"\d+(?:\.\d+)?", texto)

            if not numeros:
                return "Não consegui identificar o número."

            numero = float(numeros[0])

            if numero < 0:
                return "Não consigo calcular raiz quadrada de número negativo."

            return formatar_resultado(math.sqrt(numero))

        # Converte palavras em operadores
        texto = texto.replace("dividido por", "/")
        texto = texto.replace("dividido", "/")
        texto = texto.replace("multiplicado por", "*")
        texto = texto.replace("multiplicado", "*")
        texto = texto.replace("vezes", "*")
        texto = texto.replace("mais", "+")
        texto = texto.replace("menos", "-")
        texto = texto.replace(" x ", "*")

        # Procura: número operador número
        padrao = r"(-?\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(-?\d+(?:\.\d+)?)"

        resultado_regex = re.search(padrao, texto)

        if not resultado_regex:
            return "Não consegui entender o cálculo."

        numero1 = float(resultado_regex.group(1))
        operador = resultado_regex.group(2)
        numero2 = float(resultado_regex.group(3))

        if operador == "+":
            resultado = numero1 + numero2

        elif operador == "-":
            resultado = numero1 - numero2

        elif operador == "*":
            resultado = numero1 * numero2

        elif operador == "/":
            if numero2 == 0:
                return "Não é possível dividir por zero."

            resultado = numero1 / numero2

        else:
            return "Operação não reconhecida."

        return formatar_resultado(resultado)

    except Exception as erro:
        print(f"Erro na calculadora: {erro}")
        return "Ocorreu um erro ao realizar o cálculo."


def formatar_resultado(resultado):
    if resultado == int(resultado):
        resultado = int(resultado)

    return f"O resultado é {resultado}."


if __name__ == "__main__":
    testes = [
        "1+1",
        "quanto é 10 mais 5",
        "calcular 25 vezes 4",
        "100 dividido por 4",
        "30-12",
        "raiz de 25"
    ]

    for teste in testes:
        print(teste, "->", calcular(teste))
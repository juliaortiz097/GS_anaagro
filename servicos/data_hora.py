from datetime import datetime


# Nomes dos dias da semana em português
DIAS_SEMANA = {
    0: "segunda-feira",
    1: "terça-feira",
    2: "quarta-feira",
    3: "quinta-feira",
    4: "sexta-feira",
    5: "sábado",
    6: "domingo"
}


# Nomes dos meses em português
MESES = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro"
}


def obter_hora():
    """
    Retorna a hora atual do computador em uma frase.
    """

    agora = datetime.now()

    hora = agora.hour
    minuto = agora.minute

    if minuto == 0:
        return f"Agora são {hora} horas."

    return f"Agora são {hora} horas e {minuto} minutos."


def obter_data():
    """
    Retorna a data atual com dia da semana,
    dia do mês, mês e ano.
    """

    agora = datetime.now()

    dia_semana = DIAS_SEMANA[agora.weekday()]
    mes = MESES[agora.month]

    return (
        f"Hoje é {dia_semana}, "
        f"{agora.day} de {mes} de {agora.year}."
    )


# Teste isolado
if __name__ == "__main__":
    print(obter_hora())
    print(obter_data())
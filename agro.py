
# ANA AGRO - FIAP GLOBAL SOLUTION
# Analise das condicoes ambientais da plantacao

# Parametros de demonstracao
TEMP_MIN = 25.0
TEMP_MAX = 26.0


def classificar_condicoes(temperatura):

    if temperatura < TEMP_MIN:
        return (
            "As condições ambientais estão abaixo da "
            "faixa ideal configurada para a plantação. "
            f"O limite mínimo é de {TEMP_MIN:.0f} graus."
        )

    elif temperatura <= TEMP_MAX:
        return (
            "As condições ambientais estão dentro da "
            "faixa ideal configurada para a plantação, "
            f"que vai de {TEMP_MIN:.0f} a "
            f"{TEMP_MAX:.0f} graus."
        )

    else:
        return (
            "As condições ambientais estão acima da "
            "faixa ideal configurada para a plantação. "
            f"O limite máximo é de {TEMP_MAX:.0f} graus."
        )


def gerar_resposta_agro(temperatura, umidade, comando):

    temp_texto = f"{temperatura:.1f}".replace(".", ",")
    umidade_texto = f"{umidade:.0f}"

    classificacao = classificar_condicoes(temperatura)

    resposta = (
        f"A temperatura atual é de {temp_texto} graus "
        f"e a umidade do ar está em {umidade_texto} por cento. "
        f"{classificacao}"
    )

    return resposta

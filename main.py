import re
import unicodedata

from voz.ouvir import ouvir
from voz.falar import falar
from ana import AnaAssistant

from servicos.data_hora import obter_hora, obter_data
from servicos.calculadora import calcular
from servicos.agenda import cadastrar_evento, ler_agenda, limpar_agenda
from servicos.clima import consultar_clima

from visao.reconhecer_faces import reconhecer_face
from visao.contar_pessoas import contar_pessoas

from ia.groq_ia import perguntar_groq
from ia.ollama_ia import perguntar_ollama

from hardware.robo import (
    conectar_arduino,
    processar_resposta,
    ler_dht11
)
from agro import gerar_resposta_agro


# --------------------------------------------------
# FUNÇÕES AUXILIARES PARA IDENTIFICAR OS COMANDOS
# --------------------------------------------------

def normalizar_texto(texto):
    """
    Remove acentos e deixa o texto em minúsculo.

    Exemplo:
        "Qual é a previsão?" -> "qual e a previsao?"
    """

    texto = texto.lower().strip()

    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    return texto


def eh_calculo(comando):
    """
    Verifica se o comando parece ser realmente um cálculo.
    """

    comando = normalizar_texto(comando)

    tem_numero = bool(re.search(r"\d", comando))

    if not tem_numero:
        return False

    palavras_matematicas = [
        "calcular",
        "calcule",
        "quanto e",
        "mais",
        "menos",
        "vezes",
        "dividido",
        "multiplicado",
        "raiz"
    ]

    tem_palavra_matematica = any(
        palavra in comando
        for palavra in palavras_matematicas
    )

    tem_operador = any(
        operador in comando
        for operador in ["+", "-", "*", "/", " x "]
    )

    return tem_palavra_matematica or tem_operador


def eh_cadastrar_agenda(comando):
    comando = normalizar_texto(comando)

    possibilidades = [
        "cadastrar evento",
        "cadastrar um evento",
        "cadastrar na agenda",
        "adicionar evento",
        "adicionar um evento",
        "adicionar na agenda",
        "novo evento",
        "marcar evento"
    ]

    return any(
        frase in comando
        for frase in possibilidades
    )


def eh_ler_agenda(comando):
    comando = normalizar_texto(comando)

    possibilidades = [
        "ler agenda",
        "ler a agenda",
        "ler minha agenda",
        "ver agenda",
        "ver a agenda",
        "mostrar agenda",
        "mostrar minha agenda",
        "quais eventos",
        "o que tenho na agenda"
    ]

    return any(
        frase in comando
        for frase in possibilidades
    )


def eh_limpar_agenda(comando):
    comando = normalizar_texto(comando)

    possibilidades = [
        "limpar agenda",
        "limpar a agenda",
        "limpar minha agenda",
        "apagar agenda",
        "apagar a agenda",
        "apagar minha agenda",
        "excluir eventos"
    ]

    return any(
        frase in comando
        for frase in possibilidades
    )


def eh_comando_clima(comando):
    comando = normalizar_texto(comando)

    possibilidades = [
        "previsao do tempo",
        "como esta o tempo",
        "qual o clima",
        "qual e o clima",
        "tempo hoje",
        "clima hoje"
    ]

    return any(
        frase in comando
        for frase in possibilidades
    )


def obter_cidade_comando(comando):
    """
    Extrai a cidade de diferentes formas de perguntar sobre o clima.

    Exemplos:
        previsão do tempo São Caetano do Sul
        previsão do tempo em São Paulo
        como está o tempo em Paris
        qual o clima para Curitiba

    Caso nenhuma cidade seja informada,
    usa São Paulo como padrão.
    """

    texto = comando.lower().strip()

    prefixos = [
        "qual é a previsão do tempo para",
        "qual e a previsao do tempo para",
        "qual a previsão do tempo para",
        "qual a previsao do tempo para",

        "qual é a previsão do tempo em",
        "qual e a previsao do tempo em",
        "qual a previsão do tempo em",
        "qual a previsao do tempo em",

        "previsão do tempo para",
        "previsao do tempo para",

        "previsão do tempo em",
        "previsao do tempo em",

        "previsão do tempo",
        "previsao do tempo",

        "como está o tempo em",
        "como esta o tempo em",

        "qual é o clima em",
        "qual e o clima em",
        "qual o clima em",

        "qual é o clima de",
        "qual e o clima de",
        "qual o clima de",

        "qual é o clima",
        "qual e o clima",
        "qual o clima"
    ]

    cidade = ""

    for prefixo in prefixos:
        if texto.startswith(prefixo):
            cidade = texto[len(prefixo):].strip()
            break

    cidade = cidade.removeprefix("em ").strip()
    cidade = cidade.removeprefix("para ").strip()
    cidade = cidade.removesuffix(" hoje").strip()

    if not cidade:
        return "São Paulo"

    return cidade.title()


# --------------------------------------------------
# PROGRAMA PRINCIPAL
# --------------------------------------------------

def main():
    """
    Inicia a assistente ANA e mantém o sistema
    aguardando comandos de voz.
    """

    ana = AnaAssistant()

    # Conecta ao Arduino quando a ANA inicia
    conectar_arduino()

    print("=" * 45)
    print("          ANA - Assistente Virtual")
    print("=" * 45)

    print("Sistema iniciado.")
    print("Diga 'Ana' antes de qualquer comando.")
    print("Pressione CTRL + C para encerrar.")

    while True:

        try:
            # Escuta o usuário
            texto = ouvir()

            if not texto:
                continue

            # Verifica a palavra de ativação ANA
            comando = ana.verificar_ativacao(texto)

            # Se não chamou ANA, não executa nada
            if comando is None:
                print(
                    "ANA não foi ativada. "
                    "Nenhuma ação executada."
                )
                continue

            print("ANA ativada!")
            print(f"Comando recebido: {comando}")

            comando_normalizado = normalizar_texto(comando)

            # --------------------------------------------------
            # SOMENTE "ANA"
            # --------------------------------------------------

            if not comando:
                falar("Sim?")



            # --------------------------------------------------
            # ANA AGRO - SENSOR DHT11
            # --------------------------------------------------

            elif any(
                palavra in comando_normalizado
                for palavra in [
                    "plantacao",
                    "cultivo",
                    "temperatura ambiente",
                    "temperatura da",
                    "umidade do ar",
                    "condicoes ambientais"
                ]
            ):

                print("ANA Agro: consultando sensor DHT11...")

                dados = ler_dht11()

                if dados is None:
                    falar(
                        "Não consegui consultar o sensor "
                        "da plantação neste momento."
                    )

                else:
                    temperatura, umidade = dados

                    resposta = gerar_resposta_agro(
                        temperatura,
                        umidade,
                        comando_normalizado
                    )

                    print("ANA Agro:", resposta)
                    falar(resposta)




            # --------------------------------------------------
            # HORA
            # --------------------------------------------------

            elif "que horas" in comando_normalizado:
                resposta = obter_hora()
                falar(resposta)

            # --------------------------------------------------
            # DATA
            # --------------------------------------------------

            elif (
                "que dia e hoje" in comando_normalizado
                or "qual a data" in comando_normalizado
                or "qual e a data" in comando_normalizado
            ):
                resposta = obter_data()
                falar(resposta)

            # --------------------------------------------------
            # CALCULADORA
            # --------------------------------------------------

            elif eh_calculo(comando):

                print("Usando calculadora...")

                resposta = calcular(comando)
                falar(resposta)

            # --------------------------------------------------
            # AGENDA - CADASTRAR
            # --------------------------------------------------

            elif eh_cadastrar_agenda(comando):

                print("Abrindo serviço de agenda...")

                falar(
                    "Ok, qual evento devo cadastrar?"
                )

                evento = ouvir()

                if evento:
                    resposta = cadastrar_evento(evento)
                    falar(resposta)

                else:
                    falar(
                        "Não consegui entender o evento."
                    )

            # --------------------------------------------------
            # AGENDA - LER
            # --------------------------------------------------

            elif eh_ler_agenda(comando):

                print("Lendo agenda...")

                resposta = ler_agenda()
                falar(resposta)

            # --------------------------------------------------
            # AGENDA - LIMPAR
            # --------------------------------------------------

            elif eh_limpar_agenda(comando):

                print("Limpando agenda...")

                resposta = limpar_agenda()
                falar(resposta)

            # --------------------------------------------------
            # RECONHECIMENTO FACIAL
            # --------------------------------------------------

            elif (
                "reconhecer face" in comando_normalizado
                or "reconhecer rosto" in comando_normalizado
                or "quem sou eu" in comando_normalizado
            ):

                falar(
                    "Vou verificar quem está "
                    "na minha frente."
                )

                pessoa = reconhecer_face()

                if pessoa and pessoa != "Desconhecido":
                    falar(f"Você é {pessoa}.")

                elif pessoa == "Desconhecido":
                    falar(
                        "Não reconheci essa pessoa."
                    )

                else:
                    falar(
                        "Não consegui identificar ninguém."
                    )

            # --------------------------------------------------
            # CONTAR PESSOAS
            # --------------------------------------------------

            elif "quantas pessoas" in comando_normalizado:

                falar(
                    "Vou verificar quantas pessoas "
                    "estão na minha frente."
                )

                quantidade = contar_pessoas()

                if quantidade is None:
                    falar(
                        "Não consegui acessar a câmera."
                    )

                elif quantidade == 0:
                    falar(
                        "Não encontrei nenhuma pessoa."
                    )

                elif quantidade == 1:
                    falar(
                        "Encontrei uma pessoa."
                    )

                else:
                    falar(
                        f"Encontrei {quantidade} pessoas."
                    )

            # --------------------------------------------------
            # CLIMA
            # --------------------------------------------------

            elif eh_comando_clima(comando):

                cidade = obter_cidade_comando(comando)

                print(
                    f"Consultando OpenWeatherMap: {cidade}"
                )

                resposta = consultar_clima(cidade)

                if resposta:
                    falar(resposta)

                else:
                    falar(
                        "Não consegui consultar "
                        "o clima neste momento."
                    )

            # --------------------------------------------------
            # INTELIGÊNCIA ARTIFICIAL
            # SEMPRE DEVE SER O ÚLTIMO RECURSO
            # --------------------------------------------------

            else:

                print(
                    "Nenhum comando específico encontrado."
                )

                print(
                    "Consultando inteligência artificial..."
                )

                # Primeiro tenta Groq
                resposta = perguntar_groq(comando)

                # Se Groq falhar, tenta Ollama local
                if not resposta:

                    print(
                        "Groq indisponível. "
                        "Tentando Ollama..."
                    )

                    resposta = perguntar_ollama(comando)

                if resposta:

                    print(
                        f"Analisando resposta para o robô: "
                        f"{resposta}"
                    )

                    # PRIMEIRO aciona o robô
                    processar_resposta(resposta)

                    # DEPOIS a ANA fala
                    falar(resposta)

                else:
                    falar(
                        "Desculpe, não consegui acessar "
                        "minha inteligência artificial."
                    )

        except KeyboardInterrupt:

            print("\nANA encerrada.")
            break


if __name__ == "__main__":
    main()
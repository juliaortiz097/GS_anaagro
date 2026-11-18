import requests


# Endereço padrão do Ollama rodando no próprio computador
URL_OLLAMA = "http://localhost:11434/api/chat"

# Modelo local que você já testou
MODELO = "llama3.2:3b"


def perguntar_ollama(pergunta):
    """
    Envia uma pergunta para o Ollama rodando localmente.

    Parâmetros:
        pergunta (str): pergunta feita pelo usuário.

    Retorna:
        str: resposta gerada pela IA local.
    """

    dados = {
        "model": MODELO,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é ANA, uma assistente virtual. "
                    "Responda sempre em português do Brasil. "
                    "Suas respostas serão faladas em voz alta, "
                    "então seja natural, objetiva e breve. "
                    "Evite tabelas, Markdown e respostas muito longas."
                ),
            },
            {
                "role": "user",
                "content": pergunta,
            },
        ],
    }

    try:
        resposta = requests.post(
            URL_OLLAMA,
            json=dados,
            timeout=120
        )

        resposta.raise_for_status()

        resultado = resposta.json()

        return resultado["message"]["content"].strip()

    except requests.exceptions.ConnectionError:
        print("Erro: Ollama não está aberto.")
        return None

    except requests.exceptions.Timeout:
        print("Erro: Ollama demorou demais para responder.")
        return None

    except Exception as erro:
        print(f"Erro ao consultar o Ollama: {erro}")
        return None


# Teste isolado
if __name__ == "__main__":
    pergunta = input("Pergunte algo para a ANA local: ")

    resposta = perguntar_ollama(pergunta)

    print(f"\nANA/Ollama: {resposta}")
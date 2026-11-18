import os
from groq import Groq


def perguntar_groq(pergunta):
    """
    Envia uma pergunta para a IA Groq na nuvem.

    Parâmetros:
        pergunta (str): pergunta feita pelo usuário.

    Retorna:
        str: resposta gerada pela IA.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("Erro: GROQ_API_KEY não está configurada.")
        return None

    try:
        client = Groq(api_key=api_key)

        resposta = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é ANA, uma assistente virtual. "
                        "Responda sempre em português do Brasil. "
                        "Suas respostas serão faladas em voz alta, então seja "
                        "natural, objetiva e breve. "
                        "Evite tabelas, Markdown e respostas muito longas."
                        "Quando a pergunta puder ser respondida com sim ou não, "
                        "comece obrigatoriamente a resposta com 'Sim' ou 'Não'."
                    ),
                },
                {
                    "role": "user",
                    "content": pergunta,
                },
            ],
        )

        return resposta.choices[0].message.content.strip()

    except Exception as erro:
        print(f"Erro ao consultar o Groq: {erro}")
        return None


# Teste isolado
if __name__ == "__main__":
    pergunta = input("Pergunte algo para a ANA: ")

    resposta = perguntar_groq(pergunta)

    print(f"\nANA/Groq: {resposta}")
from pathlib import Path


# Localiza o agenda.txt dentro da pasta projeto_final
CAMINHO_AGENDA = Path(__file__).resolve().parents[1] / "agenda.txt"


def garantir_arquivo():
    """
    Garante que o arquivo agenda.txt exista.
    Caso não exista, ele será criado automaticamente.
    """
    CAMINHO_AGENDA.touch(exist_ok=True)


def cadastrar_evento(evento):
    """
    Adiciona um novo evento a agenda.

    Parâmetros:
        evento (str): evento informado pelo usuário.

    Retorna:
        str: confirmação para a ANA falar.
    """

    garantir_arquivo()

    evento = evento.strip()

    if not evento:
        return "Não consegui identificar o evento."

    with open(CAMINHO_AGENDA, "a", encoding="utf-8") as arquivo:
        arquivo.write(evento + "\n")

    return f"Evento cadastrado: {evento}."


def ler_agenda():
    """
    Lê todos os eventos cadastrados na agenda.

    Retorna:
        str: eventos cadastrados ou aviso de agenda vazia.
    """

    garantir_arquivo()

    with open(CAMINHO_AGENDA, "r", encoding="utf-8") as arquivo:
        eventos = [
            linha.strip()
            for linha in arquivo.readlines()
            if linha.strip()
        ]

    if not eventos:
        return "Sua agenda está vazia."

    resposta = "Você tem os seguintes eventos. "

    for numero, evento in enumerate(eventos, start=1):
        resposta += f"Evento {numero}: {evento}. "

    return resposta


def limpar_agenda():
    """
    Apaga todo o conteúdo da agenda,
    mas mantém o arquivo agenda.txt.
    """

    garantir_arquivo()

    # O modo "w" limpa o conteúdo sem excluir o arquivo
    with open(CAMINHO_AGENDA, "w", encoding="utf-8"):
        pass

    return "Agenda limpa com sucesso."


# Teste isolado
if __name__ == "__main__":
    print("=== TESTE DA AGENDA ===")

    print(cadastrar_evento("Apresentação de Bases Maker"))
    print(cadastrar_evento("Entregar trabalho da faculdade"))

    print("\nLeitura:")
    print(ler_agenda())

    print("\nLimpando:")
    print(limpar_agenda())

    print("\nLeitura após limpar:")
    print(ler_agenda())
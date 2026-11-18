class AnaAssistant:
    """
    Classe principal da assistente virtual ANA.

    Verifica se a assistente foi chamada antes
    de permitir a execução de qualquer comando.
    """

    def __init__(self):
        self.nome = "ana"

    def verificar_ativacao(self, texto):
        """
        Verifica se a primeira palavra falada foi 'Ana'.

        Retorna:
            str: comando sem a palavra 'ana'.
            None: caso ANA não tenha sido chamada.
        """

        if not texto:
            return None

        texto = texto.lower().strip()
        palavras = texto.split()

        if not palavras:
            return None

        # ANA precisa ser a primeira palavra
        if palavras[0] != self.nome:
            return None

        # Remove "ana" e retorna somente o comando
        comando = " ".join(palavras[1:]).strip()

        return comando
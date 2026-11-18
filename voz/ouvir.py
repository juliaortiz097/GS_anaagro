import speech_recognition as sr
from time import time


# Cria o reconhecedor de voz
reconhecedor = sr.Recognizer()

# Permite pausas mais naturais durante a fala
reconhecedor.pause_threshold = 1.6

# Tempo mínimo de silêncio considerado no reconhecimento
reconhecedor.non_speaking_duration = 0.6

# Ajusta automaticamente a sensibilidade do microfone
reconhecedor.dynamic_energy_threshold = True


def ouvir():
    """
    Escuta o microfone e transforma a fala do usuário em texto.

    Retorna:
        str: texto reconhecido em letras minúsculas.
        None: caso não consiga entender a fala.
    """

    try:
        with sr.Microphone() as mic:
            print("\nAguardando comando...")

            # Analisa rapidamente o ruído do ambiente
            reconhecedor.adjust_for_ambient_noise(
                mic,
                duration=2.0
            )

            print("Pode falar...")

            # Aguarda o usuário começar a falar.
            # Depois que a fala começa, permite uma frase mais longa.
            audio = reconhecedor.listen(
                mic,
                timeout=8,
                phrase_time_limit=20
            )

        print("Reconhecendo...")
        tempo_inicial = time()

        texto = reconhecedor.recognize_google(
            audio,
            language="pt-BR"
        )

        tempo_final = time()

        print(f"Você falou: {texto}")
        print(
            f"Tempo de reconhecimento: "
            f"{tempo_final - tempo_inicial:.2f}s"
        )

        return texto.lower()

    except sr.WaitTimeoutError:
        print("Nenhuma fala detectada.")
        return None

    except sr.UnknownValueError:
        print("Não consegui entender o que foi dito.")
        return None

    except sr.RequestError as erro:
        print(f"Erro no serviço de reconhecimento de voz: {erro}")
        return None

    except Exception as erro:
        print(f"Erro inesperado no microfone: {erro}")
        return None


if __name__ == "__main__":
    comando = ouvir()

    if comando:
        print(f"Texto retornado pela função: {comando}")
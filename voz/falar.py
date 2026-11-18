import asyncio
import edge_tts
import pygame
import tempfile
import os

# Voz feminina brasileira
VOZ_ANA = "pt-BR-FranciscaNeural"

async def gerar_audio(texto, arquivo):
    """
    Gera o áudio da ANA usando uma voz neural
    feminina em português do Brasil.
    """

    comunicacao = edge_tts.Communicate(
        texto,
        VOZ_ANA
    )

    await comunicacao.save(arquivo)


def falar(texto):
    """
    Faz a ANA falar o texto recebido.
    """

    if not texto:
        return

    print(f"ANA: {texto}")

    # Cria um arquivo temporário para o áudio
    arquivo = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    caminho_audio = arquivo.name
    arquivo.close()

    try:
        # Gera o áudio
        asyncio.run(
            gerar_audio(
                texto,
                caminho_audio
            )
        )

        # Reproduz o áudio
        pygame.mixer.init()

        pygame.mixer.music.load(caminho_audio)
        pygame.mixer.music.play()

        # Aguarda terminar de falar
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        pygame.mixer.quit()

    except Exception as erro:
        print(f"Erro ao reproduzir voz da ANA: {erro}")

    finally:
        # Apaga o áudio temporário
        if os.path.exists(caminho_audio):
            os.remove(caminho_audio)


if __name__ == "__main__":
    falar(
        "Olá, eu sou a Ana. "
        "Agora estou falando em português do Brasil."
    )
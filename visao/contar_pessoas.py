import cv2
import time
from collections import Counter


def contar_pessoas(tempo_analise=5):
    """
    Abre a webcam, detecta rostos durante alguns segundos
    e retorna a quantidade de pessoas encontrada.

    Parâmetros:
        tempo_analise (int): quantidade de segundos analisando a câmera.

    Retorna:
        int: quantidade estimada de pessoas.
        None: caso não consiga abrir a câmera.
    """

    detector_face = cv2.CascadeClassifier(
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Não foi possível abrir a webcam.")
        return None

    print("Contando pessoas...")
    print("Olhem para a câmera. Pressione Q para cancelar.")

    contagens = []

    inicio = time.time()

    while time.time() - inicio < tempo_analise:

        status, imagem = camera.read()

        if not status:
            continue

        imagem_cinza = cv2.cvtColor(
            imagem,
            cv2.COLOR_BGR2GRAY
        )

        faces = detector_face.detectMultiScale(
            imagem_cinza,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(80, 80)
        )

        quantidade = len(faces)

        contagens.append(quantidade)

        # Desenha um retângulo em cada rosto encontrado
        for x, y, largura, altura in faces:
            cv2.rectangle(
                imagem,
                (x, y),
                (x + largura, y + altura),
                (0, 255, 0),
                2
            )

        # Mostra a quantidade na própria câmera
        cv2.putText(
            imagem,
            f"Pessoas: {quantidade}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "Contagem de Pessoas - ANA",
            imagem
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    if not contagens:
        return 0

    # Ignora frames em que nenhum rosto apareceu,
    # caso algum rosto tenha sido detectado durante o teste
    contagens_com_pessoas = [
        quantidade
        for quantidade in contagens
        if quantidade > 0
    ]

    if contagens_com_pessoas:
        # Escolhe a quantidade que apareceu com maior frequência
        quantidade_final = Counter(
            contagens_com_pessoas
        ).most_common(1)[0][0]
    else:
        quantidade_final = 0

    return quantidade_final


# Teste isolado
if __name__ == "__main__":

    quantidade = contar_pessoas()

    if quantidade is not None:
        print(f"Quantidade encontrada: {quantidade}")
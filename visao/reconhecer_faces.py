import cv2
from pathlib import Path


# Nomes associados aos IDs usados no treinamento
NOMES = {
    0: "Desconhecido",
    1: "JuOrtiz",
    2: "JuPalomari",
}


# Caminho do modelo facial já treinado
CAMINHO_MODELO = (
    Path(__file__).resolve().parents[1]
    / "dados"
    / "reconhecimento_facial"
    / "classificadoreigen.yml"
)


def reconhecer_face():
    """
    Abre a webcam e tenta reconhecer a pessoa que está na frente.

    Retorna:
        str: nome da pessoa reconhecida.
        None: caso nenhuma pessoa seja reconhecida.
    """

    # Verifica se o modelo treinado existe
    if not CAMINHO_MODELO.exists():
        print(f"Modelo não encontrado: {CAMINHO_MODELO}")
        return None

    # Detector de rostos do OpenCV
    detector_face = cv2.CascadeClassifier(
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    # Carrega o modelo EigenFace treinado
    reconhecedor = cv2.face.EigenFaceRecognizer_create()
    reconhecedor.read(str(CAMINHO_MODELO))

    largura = 220
    altura = 220

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Não foi possível abrir a webcam.")
        return None

    print("Reconhecimento facial iniciado.")
    print("Olhe para a câmera. Pressione Q para cancelar.")

    nome_reconhecido = None

    # Usamos algumas confirmações para evitar
    # reconhecer a pessoa com apenas um frame
    ultimo_nome = None
    confirmacoes = 0
    confirmacoes_necessarias = 5

    while True:
        status, imagem = camera.read()

        if not status:
            print("Não foi possível capturar a imagem.")
            break

        imagem_cinza = cv2.cvtColor(
            imagem,
            cv2.COLOR_BGR2GRAY
        )

        faces = detector_face.detectMultiScale(
            imagem_cinza,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(100, 100)
        )

        for x, y, largura_face, altura_face in faces:

            # Recorta somente o rosto
            imagem_rosto = imagem_cinza[
                y:y + altura_face,
                x:x + largura_face
            ]

            # Deixa no mesmo tamanho usado no treinamento
            imagem_rosto = cv2.resize(
                imagem_rosto,
                (largura, altura)
            )

            # Faz a previsão
            id_pessoa, confianca = reconhecedor.predict(
                imagem_rosto
            )

            nome = NOMES.get(
                id_pessoa,
                "Desconhecido"
            )

            print(
                f"ID: {id_pessoa} | "
                f"Nome: {nome} | "
                f"Confiança: {confianca:.2f}"
            )

            # Desenha o retângulo no rosto
            cv2.rectangle(
                imagem,
                (x, y),
                (x + largura_face, y + altura_face),
                (0, 0, 255),
                2
            )

            # Mostra o nome na câmera
            cv2.putText(
                imagem,
                nome,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

            # Confirma o mesmo reconhecimento
            # durante vários frames consecutivos
            if nome == ultimo_nome:
                confirmacoes += 1
            else:
                ultimo_nome = nome
                confirmacoes = 1

            if confirmacoes >= confirmacoes_necessarias:
                nome_reconhecido = nome
                break

        cv2.imshow("Reconhecimento Facial - ANA", imagem)

        # Sai automaticamente quando confirmar alguém
        if nome_reconhecido:
            cv2.waitKey(800)
            break

        # Permite cancelar apertando Q
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    return nome_reconhecido


# Teste isolado
if __name__ == "__main__":
    pessoa = reconhecer_face()

    if pessoa:
        print(f"Pessoa reconhecida: {pessoa}")
    else:
        print("Nenhuma pessoa reconhecida.")
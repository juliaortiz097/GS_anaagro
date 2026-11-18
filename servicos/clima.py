import os
import requests


URL_CLIMA = "https://api.openweathermap.org/data/2.5/weather"


def consultar_clima(cidade="São Paulo"):
    """
    Consulta o clima atual de uma cidade usando OpenWeatherMap.

    Parâmetros:
        cidade (str): nome da cidade pesquisada.

    Retorna:
        str: frase com temperatura, sensação térmica,
             condição do tempo e umidade.
        None: caso ocorra algum erro.
    """

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        print("Erro: OPENWEATHER_API_KEY não está configurada.")
        return None

    parametros = {
        "q": f"{cidade}",
        "appid": api_key,
        "units": "metric",
        "lang": "pt_br"
    }

    try:
        resposta = requests.get(
            URL_CLIMA,
            params=parametros,
            timeout=10
        )

        # Cidade não encontrada
        if resposta.status_code == 404:
            return f"Não encontrei informações sobre {cidade}."

        resposta.raise_for_status()

        dados = resposta.json()

        temperatura = round(dados["main"]["temp"])
        sensacao = round(dados["main"]["feels_like"])
        umidade = dados["main"]["humidity"]

        descricao = dados["weather"][0]["description"]

        nome_cidade = dados["name"]

        return (
            f"Em {nome_cidade}, está fazendo "
            f"{temperatura} graus, com {descricao}. "
            f"A sensação térmica é de {sensacao} graus "
            f"e a umidade está em {umidade} por cento."
        )

    except requests.exceptions.ConnectionError:
        print("Erro de conexão com OpenWeatherMap.")
        return None

    except requests.exceptions.Timeout:
        print("OpenWeatherMap demorou demais para responder.")
        return None

    except Exception as erro:
        print(f"Erro ao consultar clima: {erro}")
        return None


# Teste isolado
if __name__ == "__main__":
    cidade = input("Cidade: ").strip()

    if not cidade:
        cidade = "São Paulo"

    resultado = consultar_clima(cidade)

    if resultado:
        print(resultado)
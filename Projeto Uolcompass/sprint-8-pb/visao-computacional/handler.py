import json
from datetime import datetime

# Importando funções Rekognition
from services.rekognition import detectar_rostos, detectar_labels


def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def v1_description(event, context):
    body = {"message": "VISION api version 1."}

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def v2_description(event, context):
    body = {"message": "VISION api version 2."}

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


# rota para reconhecimento facial e emoçoes
def v1_vision(event, context):
    body = json.loads(event["body"])
    # Definição da imagem armazenada em bucket S3 a ser analisada
    bucket = body["bucket"]
    nome_imagem = body["imageName"]
    url_imagem = f"https://{bucket}.s3.amazonaws.com/{nome_imagem}"

    try:
        # Função para detectar rostos e emoções
        rostos = detectar_rostos(bucket, nome_imagem)

        # Resposta gerada ao fazer a leitura da imagem definida
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "url_to_image": url_imagem,
                    "created_image": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "faces": rostos,
                },
                indent=4,
            ),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"error": str(e), "message": "Erro ao processar a imagem."}
            ),
        }


# Rota para identificar rostos, emoções e pets a partir de fotos, e gerar dicas através do nome dos pets identificados
def v2_vision(event, context):
    body = json.loads(event["body"])
    # Definição da imagem armazenada em bucket S3 a ser analisada
    bucket = body["bucket"]
    nome_imagem = body["imageName"]
    url_imagem = f"https://{bucket}.s3.amazonaws.com/{nome_imagem}"

    try:
        # Função para detectar rostos e emoções
        rostos = detectar_rostos(bucket, nome_imagem)
        # Função para detectar pets e gerar dicas com Bedrock
        pets = detectar_labels(bucket, nome_imagem)

        # Resposta gerada ao fazer a leitura da imagem definida
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "url_to_image": url_imagem,
                    "created_image": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "faces": rostos,
                    "pets": pets,
                },
                indent=4,
            ),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"error": str(e), "message": "Erro ao processar a imagem."}
            ),
        }

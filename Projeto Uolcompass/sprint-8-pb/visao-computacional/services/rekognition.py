import boto3
from .bedrock import obter_dicas_pet_bedrock

# Iniciando sessão Rekognition
cliente_rekognition = boto3.client("rekognition")


#! Parte 1 e Parte 2
# Função para detectar rostos e emoções
def detectar_rostos(bucket, nome_imagem):
    # Definindo imagem para ser analisada
    resposta = cliente_rekognition.detect_faces(
        Image={"S3Object": {"Bucket": bucket, "Name": nome_imagem}}, Attributes=["ALL"]
    )

    rostos = []  # recebe todos os rostos
    for detalhe_rosto in resposta["FaceDetails"]:
        emoções = detalhe_rosto["Emotions"]
        emoção_principal = max(emoções, key=lambda x: x["Confidence"])

        dados_rosto = {
            "position": {
                "Height": detalhe_rosto["BoundingBox"]["Height"],
                "Left": detalhe_rosto["BoundingBox"]["Left"],
                "Top": detalhe_rosto["BoundingBox"]["Top"],
                "Width": detalhe_rosto["BoundingBox"]["Width"],
            },
            "classified_emotion": emoção_principal["Type"],
            "classified_emotion_confidence": emoção_principal["Confidence"],
        }
        rostos.append(dados_rosto)

    if not rostos:  # caso não existam rostos na imagem definida
        rostos.append(
            {
                "position": {
                    "Height": None,
                    "Left": None,
                    "Top": None,
                    "Width": None,
                },
                "classified_emotion": None,
                "classified_emotion_confidence": None,
            }
        )

    print(rostos)
    return rostos


# Função para detectar os pets utilizando labels e gerar dicas para os pets identificados
def detectar_labels(bucket, nome_imagem):
    # Definindo imagem para ser analisada
    resposta_labels = cliente_rekognition.detect_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": nome_imagem}}, MaxLabels=10
    )

    # Definindo labels para identificar raças de possíveis pets
    racas_de_caes = [
        "poodle", "labrador", "golden retriever", "beagle", "husky", "chihuahua",
        "dalmatian", "rottweiler", "pug", "chow chow", "boxer", "shitzu", "pomeranian",
        "schnauzer", "pitbull","Bulldog","puddle", 
    ]

    pets = []
    labels_de_pets = []
    raca_detectada = None

    # Recuperando resposta gerada a partir da identificação dos pets com as labels de raça
    for label in resposta_labels["Labels"]:
        if (
            "pet" in label["Name"].lower()
            or "dog" in label["Name"].lower()
            or "animal" in label["Name"].lower()
            or any(raca in label["Name"].lower() for raca in racas_de_caes)
        ):
            labels_de_pets.append(
                {"Nome": label["Name"], "Confiança": label["Confidence"]}
            )

            if any(raca in label["Name"].lower() for raca in racas_de_caes):
                raca_detectada = {"Nome": label["Name"], "Confiança": label["Confidence"]}

    # Se raça detectada, reorganiza os labels para que a raça fique por último
    if raca_detectada:
        labels_de_pets = [
            label for label in labels_de_pets if label["Nome"] != raca_detectada["Nome"]
        ]
        labels_de_pets.append(raca_detectada)

    # Gerando dicas usando Bedrock (caso existam pets na foto)
    dica_pet = "Dica indisponível"
    if raca_detectada:
        dica_pet = obter_dicas_pet_bedrock(raca_detectada)

    pets.append(
        {
            "labels": labels_de_pets,
            "Dicas": dica_pet,
        }
    )

    return pets

import boto3
import json

# Inicializando sessão com Bedrock
cliente_bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def obter_dicas_pet_bedrock(texto_entrada):
    # Definindo texto do prompt

    entrada = (
        f"Você é um especialista em animais de estimação."
        f" Por favor, forneça dicas detalhadas sobre {texto_entrada}, "
        f"IMPORTANTE: favor, traduza a raça {texto_entrada} para português"
        f"IMPORANTE: Mantenha cada tópico (Nível de Energia e Necessidades de Exercícios, Temperamento e Comportamento, Cuidados e Necessidades e Problemas de Saúde Comuns) texto não pode ter mais de 50 tokens"
    )
    
    # Definindo modelo Bedrock
    modelo_id = "amazon.titan-text-express-v1"
    # Configurando payload para o modelo
    payload = {
        "inputText": entrada,
        "textGenerationConfig": {
            "maxTokenCount": 400,
            "temperature": 0.4,
            "topP": 0.9,
        },
    }

    try:
        # Recuperando dicas geradas para o pet com Bedrock
        resposta = cliente_bedrock.invoke_model(
            modelId=modelo_id, body=json.dumps(payload), contentType="application/json"
        )
        resultado = json.loads(resposta["body"].read().decode("utf-8"))
        dica_do_pet = resultado["results"][0]["outputText"]
        dica_do_pet = dica_do_pet.encode("utf-8").decode("utf-8")
        dica_do_pet = dica_do_pet.replace("\n", " ")

        return dica_do_pet

    except Exception as e:
        print(f"Erro ao acessar o Amazon Bedrock: {e}")
        return "Erro ao obter dicas do pet."

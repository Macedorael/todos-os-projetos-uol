import json
import boto3

# Cria um cliente da Lambda para invocar a função de TTS
lambda_client = boto3.client("lambda")
CONVERT_TO_AUDIO_LAMBDA = "api-tts-bot-v1-ttsFunction"


# Função para enviar mensagem ao TTS Lambda e obter URL do áudio
def get_audio_url_from_tts(lex_message):
    if lex_message:
        payload = {
            "httpMethod": "POST",
            "path": "/v1/tts",
            "body": json.dumps({"phrase": lex_message}),
            "headers": {"Content-Type": "application/json"},
            "isBase64Encoded": False,
        }

        try:
            response = lambda_client.invoke(
                FunctionName=CONVERT_TO_AUDIO_LAMBDA,
                InvocationType="RequestResponse",
                Payload=json.dumps(payload),
            )
            response_payload = json.loads(response["Payload"].read().decode())
            body = json.loads(response_payload["body"])
            return body.get("url_to_audio", "URL do áudio não encontrada")
        except Exception as e:
            print(f"Erro ao invocar a função Lambda de áudio: {str(e)}")
            return None
    return None


# Função para checar se todos os slots estão preenchidos
def all_slots_filled(slots):
    return all(slot_value is not None for slot_value in slots.values())

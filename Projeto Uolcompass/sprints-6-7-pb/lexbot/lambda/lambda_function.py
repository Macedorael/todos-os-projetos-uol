import boto3  # type: ignore
from agendar import agendar_intent
from cancelar import cancelar_intent
from verificar import verificar_intent
from saudacoes import saudacoes_intent
from utils import get_audio_url_from_tts
from valores import valores_intent

# Cria um cliente da Lambda para invocar a função de TTS
lambda_client = boto3.client("lambda")

# Nome da função Lambda que converte texto em áudio
CONVERT_TO_AUDIO_LAMBDA = "api-tts-bot-v1-ttsFunction"


def lambda_handler(event, context):
    # recuperando a entrada do Lex
    current_intent = event["sessionState"]["intent"]["name"]
    slots = event["sessionState"]["intent"]["slots"]
    session_attributes = event['sessionState'].get('sessionAttributes', {})

    # SaudacaoIntent com geracaao de áudio
    if current_intent == "Saudacoes":
        response = saudacoes_intent(event)

    # AgendarIntent com geracao de áudio
    elif current_intent == "AgendarIntent":
        response = agendar_intent(event)

    # VerificarIntent com CPF e geracao de áudio
    elif current_intent == "VerificarIntent":
        response = verificar_intent(event)

    # CancelarIntent com CPF e geracao de áudio
    elif current_intent == "CancelarIntent":
        response = cancelar_intent(event)
        
    elif current_intent == "ValoresIntent":
        response = valores_intent(event)

    else:
        lex_message = "Desculpe, não entendi o que você disse."
        url_audio = get_audio_url_from_tts(lex_message)
        mensagem = f"{lex_message}"
        mensagem2 = (
            f"Ouça o áudio aqui: {url_audio}" if url_audio else "Áudio não disponível"
        )
        response = {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": current_intent, "state": "Fulfilled"},
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem},
                {"contentType": "PlainText", "content": mensagem2},
            ],
        }

    return response

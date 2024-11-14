import boto3
from utils import get_audio_url_from_tts
import re

# Inicializa o cliente do DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("nutriBotTabela")


# regex cpf
# CPF deve ter exatamente 11 dígitos
cpf_regex = re.compile(r"^\d{11}$")  

# validacao usando regex
def validar_cpf(cpf):
    return cpf_regex.match(cpf)

def verificar_intent(event):
    current_intent = event["sessionState"]["intent"]["name"]
    slots = event["sessionState"]["intent"]["slots"]
    cpf = slots.get("cpf")

    if cpf and cpf["value"]["interpretedValue"]:
        cpf_value = cpf["value"]["interpretedValue"]

        # Verifica se o CPF é válido
        if not validar_cpf(cpf_value):
            lex_message = f"O CPF informado {cpf_value} é inválido. Por favor, forneça um CPF válido com 11 dígitos."
            url_audio = get_audio_url_from_tts(lex_message)
            response = {
                "sessionState": {
                    "dialogAction": {"type": "ElicitSlot", "slotToElicit": "cpf"},
                    "intent": {"name": current_intent, "slots": slots},
                },
                "messages": [
                    {"contentType": "PlainText", "content": lex_message},
                    {"contentType": "PlainText", "content": f"Ouça o áudio aqui: {url_audio}" if url_audio else "Áudio não disponível"},
                ],
            }
            return response

        # Verifica se o CPF existe na tabela
        response_dynamo = table.get_item(Key={"cpf": cpf_value})

        if "Item" in response_dynamo:
            item = response_dynamo["Item"]
            nome = item.get("nome", "Desconhecido")
            dia = item.get("dia", "Desconhecido")
            hora = item.get("hora", "Desconhecido")
            lex_message = f"Consulta confirmada para {nome}, Dia: {dia}, Hora: {hora}."
        else:
            lex_message = f"Não foi encontrada nenhuma consulta para o CPF {cpf_value}."

        url_audio = get_audio_url_from_tts(lex_message)
        response = {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": current_intent, "state": "Fulfilled"},
            },
            "messages": [
                {"contentType": "PlainText", "content": lex_message},
                {"contentType": "PlainText", "content": f"Ouça o áudio aqui: {url_audio}" if url_audio else "Áudio não disponível"},
            ],
        }
    else:
        lex_message = "Por favor, informe o seu CPF."
        url_audio = get_audio_url_from_tts(lex_message)
        response = {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": "cpf"},
                "intent": {"name": current_intent, "slots": slots},
            },
            "messages": [
                {"contentType": "PlainText", "content": lex_message},
                {"contentType": "PlainText", "content": f"Ouça o áudio aqui: {url_audio}" if url_audio else "Áudio não disponível"},
            ],
        }

    return response

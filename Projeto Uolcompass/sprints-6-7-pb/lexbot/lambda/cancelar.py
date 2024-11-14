import boto3
from utils import get_audio_url_from_tts
import re

# Inicializa o cliente do DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("nutriBotTabela")

# Expressão regular para verificar o CPF (11 dígitos)
cpf_regex = re.compile(r"^\d{11}$")  

def validar_cpf(cpf):
    return cpf_regex.match(cpf)

def cancelar_intent(event):
    current_intent = event["sessionState"]["intent"]["name"]
    slots = event["sessionState"]["intent"]["slots"]
    cpf = slots.get("cpf")
    confirmacao = slots.get("confirmacao") 
    if cpf and cpf["value"]["interpretedValue"]:
        cpf_value = cpf["value"]["interpretedValue"]

        # Verifica se o CPF é válido usando regex
        if not validar_cpf(cpf_value):
            lex_message = f"O CPF {cpf_value} é inválido. Por favor, forneça um CPF com 11 dígitos."
            url_audio = get_audio_url_from_tts(lex_message)
            mensagem = f"{lex_message}"
            mensagem2 = (
                f"Ouça o áudio aqui: {url_audio}" if url_audio else "Áudio não disponível"
            )

            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": "cpf", 
                    },
                    "intent": {"name": current_intent, "slots": slots},
                },
                "messages": [
                    {"contentType": "PlainText", "content": mensagem},
                    {"contentType": "PlainText", "content": mensagem2},
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

            if not confirmacao: 
                lex_message = f"Encontramos uma consulta para {nome} no dia {dia}, às {hora}. Deseja realmente cancelar?"
                url_audio = get_audio_url_from_tts(lex_message)
                mensagem = f"{lex_message}"
                mensagem2 = (
                    f"Ouça o áudio aqui: {url_audio}"
                    if url_audio
                    else "Áudio não disponível"
                )

                # Criando card de resposta com opções
                card_response = {
                    "contentType": "ImageResponseCard",
                    "imageResponseCard": {
                        "title": "Confirmação de Cancelamento",
                        "subTitle": "Você deseja realmente cancelar sua consulta?",
                        "buttons": [
                            {"text": "Sim", "value": "sim"},
                            {"text": "Não", "value": "não"},
                        ],
                    },
                }

                response = {
                    "sessionState": {
                        "dialogAction": {
                            "type": "ElicitSlot",
                            "slotToElicit": "confirmacao",  
                        },
                        "intent": {"name": current_intent, "slots": slots},
                    },
                    "messages": [
                        {"contentType": "PlainText", "content": mensagem},
                        {"contentType": "PlainText", "content": mensagem2},
                        card_response,  
                    ],
                }
            elif confirmacao["value"]["interpretedValue"].lower() == "sim":
                # Remove o registro do DynamoDB
                table.delete_item(Key={"cpf": cpf_value})

                lex_message = "Consulta cancelada."
                url_audio = get_audio_url_from_tts(lex_message)
                mensagem = f"{lex_message}"
                mensagem2 = (
                    f"Ouça o áudio aqui: {url_audio}"
                    if url_audio
                    else "Áudio não disponível"
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
            else:  
                lex_message = f"Certo, te vemos no dia {dia}, às {hora}."
                url_audio = get_audio_url_from_tts(lex_message)
                mensagem = f"{lex_message}"
                mensagem2 = (
                    f"Ouça o áudio aqui: {url_audio}"
                    if url_audio
                    else "Áudio não disponível"
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
        else:
            lex_message = f"Não encontramos nenhuma consulta para o CPF {cpf_value}."
            url_audio = get_audio_url_from_tts(lex_message)
            mensagem = f"{lex_message}"
            mensagem2 = (
                f"Ouça o áudio aqui: {url_audio}"
                if url_audio
                else "Áudio não disponível"
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
    else:
        lex_message = "Por favor, informe o seu CPF."
        url_audio = get_audio_url_from_tts(lex_message)
        mensagem = f"{lex_message}"
        mensagem2 = (
            f"Ouça o áudio aqui: {url_audio}" if url_audio else "Áudio não disponível"
        )

        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "cpf",
                },
                "intent": {"name": current_intent, "slots": slots},
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem},
                {"contentType": "PlainText", "content": mensagem2},
            ],
        }

    return response

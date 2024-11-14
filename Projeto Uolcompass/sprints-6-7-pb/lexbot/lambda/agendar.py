import re
from utils import get_audio_url_from_tts
import boto3

# Configurando cliente do DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("nutriBotTabela")

# Expressões regulares para validação
cpf_regex = re.compile(r"^\d{11}$")  # CPF deve ter exatamente 11 dígitos
nome_regex = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ ]+$")  # Apenas letras e espaços

def validar_cpf(cpf):
    return cpf_regex.match(cpf)

def validar_nome(nome):
    return nome_regex.match(nome)

def validar_sobrenome(sobrenome):
    return nome_regex.match(sobrenome)

def calcular_preco(objetivo, plano):
    precos = {
        "emagrecimento": {"mensal": 200, "trimestral": 500, "semestral": 900},
        "hipertrofia": {"mensal": 250, "trimestral": 550, "semestral": 950},
    }
    return precos.get(objetivo, {}).get(plano)

def obter_mensagem_precos(objetivo, plano):
    preco = calcular_preco(objetivo, plano)
    if preco is not None:
        return f"O preço do plano {plano} para {objetivo} é R${preco}."
    return "Opção inválida. Por favor, escolha um objetivo e um plano válidos."

def obter_mensagem_e_audio(mensagem):
    url_audio = get_audio_url_from_tts(mensagem)
    return mensagem, f"Ouça o áudio aqui: {url_audio}" if url_audio else "Áudio não disponível"

def agendar_intent(event):
    session_attributes = event["sessionState"].get("sessionAttributes", {})
    current_intent = event["sessionState"]["intent"]["name"]
    slots = event["sessionState"]["intent"]["slots"]

    # Obter valores dos slots
    objetivo_value = slots.get("objetivo")
    plano_value = slots.get("plano")
    nome = slots.get("nome")
    sobrenome = slots.get("sobrenome")
    cpf = slots.get("cpf")
    dia = slots.get("dia")
    hora = slots.get("hora")
    confirmacao = slots.get("confirmacao")

    # Ajustar session attributes se necessário
    if objetivo_value and isinstance(objetivo_value, dict):
        session_attributes["objetivo"] = objetivo_value.get("value", {}).get("interpretedValue")
    if plano_value and isinstance(plano_value, dict):
        session_attributes["plano"] = plano_value.get("value", {}).get("interpretedValue")

    # Validação do objetivo
    if not session_attributes.get("objetivo"):
        mensagem_objetivo = "Por favor, escolha seu objetivo: Emagrecimento ou Hipertrofia."
        url_audio_objetivo = get_audio_url_from_tts(mensagem_objetivo)
        card_response = {
            "contentType": "ImageResponseCard",
            "imageResponseCard": {
                "title": "Escolha seu objetivo",
                "buttons": [
                    {"text": "Emagrecimento", "value": "emagrecimento"},
                    {"text": "Hipertrofia", "value": "hipertrofia"},
                ],
            },
        }
        return {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": "objetivo"},
                "intent": {"name": current_intent, "slots": slots, "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_objetivo},
                {"contentType": "PlainText", "content": url_audio_objetivo},
                card_response,
            ],
        }

    # Validação do plano
    if not session_attributes.get("plano"):
        mensagem_plano = f"Você escolheu {session_attributes['objetivo']}. Agora, escolha o plano: Mensal, Trimestral ou Semestral."
        url_audio_plano = get_audio_url_from_tts(mensagem_plano)
        card_response = {
            "contentType": "ImageResponseCard",
            "imageResponseCard": {
                "title": "Escolha seu plano",
                "buttons": [
                    {"text": "Mensal", "value": "mensal"},
                    {"text": "Trimestral", "value": "trimestral"},
                    {"text": "Semestral", "value": "semestral"},
                ],
            },
        }
        return {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": "plano"},
                "intent": {"name": current_intent, "slots": slots, "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_plano},
                {"contentType": "PlainText", "content": url_audio_plano},
                card_response,
            ],
        }

    # Validação do nome
    if not nome:
        lex_message = "Por favor, informe seu nome."
        mensagem_texto, mensagem_audio = obter_mensagem_e_audio(lex_message)
        return {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": "nome"},
                "intent": {"name": current_intent, "slots": slots, "state": "InProgress"},
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_texto},
                {"contentType": "PlainText", "content": mensagem_audio},
            ],
        }

    if not validar_nome(nome.get("value", {}).get("interpretedValue", "")):
        lex_message = f"O nome '{nome.get('value', {}).get('interpretedValue', '')}' informado é inválido. Por favor, informe um nome válido."
        mensagem_texto, mensagem_audio = obter_mensagem_e_audio(lex_message)
        return {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": "nome"},
                "intent": {"name": current_intent, "slots": slots, "state": "InProgress"},
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_texto},
                {"contentType": "PlainText", "content": mensagem_audio},
            ],
        }

    # Validação do sobrenome
    if not sobrenome:
        lex_message = "Por favor, informe seu sobrenome."
        mensagem_texto, mensagem_audio = obter_mensagem_e_audio(lex_message)
        return {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": "sobrenome"},
                "intent": {"name": current_intent, "slots": slots, "state": "InProgress"},
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_texto},
                {"contentType": "PlainText", "content": mensagem_audio},
            ],
        }

    if not validar_sobrenome(sobrenome.get("value", {}).get("interpretedValue", "")):
        lex_message = f"O sobrenome '{sobrenome.get('value', {}).get('interpretedValue', '')}' informado é inválido. Por favor, informe um sobrenome válido."
        mensagem_texto, mensagem_audio = obter_mensagem_e_audio(lex_message)
        return {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": "sobrenome"},
                "intent": {"name": current_intent, "slots": slots, "state": "InProgress"},
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_texto},
                {"contentType": "PlainText", "content": mensagem_audio},
            ],
        }

    # Validação do CPF
    if not cpf:
        lex_message = "Por favor, informe seu CPF."
        mensagem_texto, mensagem_audio = obter_mensagem_e_audio(lex_message)
        return {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": "cpf"},
                "intent": {"name": current_intent, "slots": slots, "state": "InProgress"},
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_texto},
                {"contentType": "PlainText", "content": mensagem_audio},
            ],
        }

    if not validar_cpf(cpf.get("value", {}).get("interpretedValue", "")):
        lex_message = f"O CPF '{cpf.get('value', {}).get('interpretedValue', '')}' informado é inválido. Por favor, informe um CPF válido."
        mensagem_texto, mensagem_audio = obter_mensagem_e_audio(lex_message)
        return {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": "cpf"},
                "intent": {"name": current_intent, "slots": slots, "state": "InProgress"},
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_texto},
                {"contentType": "PlainText", "content": mensagem_audio},
            ],
        }

    # Validação do dia
    if not dia:
        lex_message = "Por favor, informe o dia da consulta."
        mensagem_texto, mensagem_audio = obter_mensagem_e_audio(lex_message)
        return {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": "dia"},
                "intent": {"name": current_intent, "slots": slots, "state": "InProgress"},
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_texto},
                {"contentType": "PlainText", "content": mensagem_audio},
            ],
        }

    # Validação da hora
    if not hora:
        lex_message = "Por favor, informe a hora da consulta."
        mensagem_texto, mensagem_audio = obter_mensagem_e_audio(lex_message)
        return {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": "hora"},
                "intent": {"name": current_intent, "slots": slots, "state": "InProgress"},
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_texto},
                {"contentType": "PlainText", "content": mensagem_audio},
            ],
        }

    # Validação da confirmação
    if not confirmacao:
        lex_message = (
            f"Você deseja agendar sua consulta para o dia {dia.get('value', {}).get('interpretedValue', '')} às {hora.get('value', {}).get('interpretedValue', '')}? "
            "Responda com 'sim' ou 'não'."
        )
        mensagem_texto, mensagem_audio = obter_mensagem_e_audio(lex_message)
        card_response = {
            "contentType": "ImageResponseCard",
            "imageResponseCard": {
                "title": "Confirmação de Agendamento",
                "subtitle": "Você deseja confirmar?",
                "buttons": [
                    {"text": "Sim", "value": "sim"},
                    {"text": "Não", "value": "não"},
                ],
            },
        }
        return {
            "sessionState": {
                "dialogAction": {"type": "ElicitSlot", "slotToElicit": "confirmacao"},
                "intent": {"name": current_intent, "slots": slots, "state": "InProgress"},
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_texto},
                {"contentType": "PlainText", "content": mensagem_audio},
                card_response,
            ],
        }

    # Quando a consulta é confirmada
    if confirmacao.get("value", {}).get("interpretedValue", "").lower() in ["sim", "s"]:
        # Armazenar os dados no DynamoDB
        table.put_item(
            Item={
                "cpf": cpf["value"]["interpretedValue"],
                "nome": nome["value"]["interpretedValue"],
                "sobrenome": sobrenome["value"]["interpretedValue"],
                "objetivo": session_attributes["objetivo"],
                "plano": session_attributes["plano"],
                "dia": dia["value"]["interpretedValue"],
                "hora": hora["value"]["interpretedValue"],
            }
        )

        lex_message = (
            f"Obrigado, {nome['value']['interpretedValue']}! Sua consulta foi agendada para {dia['value']['interpretedValue']} às {hora['value']['interpretedValue']}."
        )
        mensagem_texto, mensagem_audio = obter_mensagem_e_audio(lex_message)
        return {
            "sessionState": {
                "dialogAction": {"type": "Close", "fulfillmentState": "Fulfilled"},
                "intent": {
                    "name": current_intent,
                    "slots": slots,
                    "state": "Fulfilled",
                },
                "sessionAttributes": session_attributes,
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_texto},
                {"contentType": "PlainText", "content": mensagem_audio},
            ],
        }

    else:
        # Quando a consulta não é confirmada
        lex_message = "Entendi. Sua consulta não foi agendada. Se precisar, pode perguntar novamente."
        mensagem_texto, mensagem_audio = obter_mensagem_e_audio(lex_message)
        return {
            "sessionState": {
                "dialogAction": {"type": "Close", "fulfillmentState": "Fulfilled"},
                "intent": {
                    "name": current_intent,
                    "slots": slots,
                    "state": "Fulfilled",
                },
                "sessionAttributes": session_attributes,
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_texto},
                {"contentType": "PlainText", "content": mensagem_audio},
            ],
        }

def lambda_handler(event, context):
    return agendar_intent(event)

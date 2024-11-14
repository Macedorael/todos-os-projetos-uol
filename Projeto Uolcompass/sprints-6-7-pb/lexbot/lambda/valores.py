from utils import get_audio_url_from_tts, all_slots_filled


def calcular_preco(objetivo, plano):
    precos = {
        "emagrecimento": {
            "mensal": 200,
            "trimestral": 500,
            "semestral": 900},
            
        "hipertrofia": {
            "mensal": 250, 
            "trimestral": 550,  
            "semestral": 950, 
        },
    }

    if objetivo in precos and plano in precos[objetivo]:
        return precos[objetivo][plano]
    else:
        return None


def obter_mensagem_precos(objetivo, plano):
    preco = calcular_preco(objetivo, plano)
    if preco is not None:
        return f"O preço do plano {plano} para {objetivo} é R${preco}."
    else:
        return "Opção inválida. Por favor, escolha um objetivo e um plano válidos."


def valores_intent(event):
    session_attributes = event["sessionState"].get("sessionAttributes", {})
    current_intent = event["sessionState"]["intent"]["name"]
    slots = event["sessionState"]["intent"]["slots"]

    objetivo = slots.get("objetivo")

    # Se o slot objetivo já estiver preenchido
    if objetivo and objetivo["value"]:
        objetivo_value = objetivo["value"]["interpretedValue"].lower()
        plano = slots.get("plano")

        if plano and all_slots_filled(slots):
            plano_value = plano["value"]["interpretedValue"].lower()
            # Armazenar objetivo e plano nos session attributes
            session_attributes["objetivo"] = objetivo_value
            session_attributes["plano"] = plano_value

            mensagem_precos = obter_mensagem_precos(objetivo_value, plano_value)
            url_audio = get_audio_url_from_tts(mensagem_precos)

            # Card de opções finais
            final_card_response = {
                "contentType": "ImageResponseCard",
                "imageResponseCard": {
                    "title": "O que você gostaria de fazer agora?",
                    "buttons": [
                        {"text": "Outros valores", "value": "Valores"},
                        {"text": "Vamos agendar", "value": "Agendar"},
                    ],
                },
            }

            response = {
                "sessionState": {
                    "dialogAction": {"type": "Close"},
                    "intent": {"name": current_intent, "state": "Fulfilled"},
                    "sessionAttributes": session_attributes,  
                },
                "messages": [
                    {"contentType": "PlainText", "content": mensagem_precos},
                    {
                        "contentType": "PlainText",
                        "content": f"Ouça o áudio aqui: {url_audio}"
                        if url_audio
                        else "Áudio não disponível",
                    },
                    final_card_response,
                ],
            }
            return response

        # Se o plano não estiver preenchido, pergunta o plano
        else:
            mensagem_plano = f"Você escolheu {objetivo_value}. Agora, escolha o plano: Mensal, Trimestral ou Semestral."
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

            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": "plano",
                    },
                    "intent": {"name": current_intent, "slots": slots},
                    "sessionAttributes": session_attributes,  
                },
                "messages": [
                    {"contentType": "PlainText", "content": mensagem_plano},
                    {
                        "contentType": "PlainText",
                        "content": f"Ouça o áudio aqui: {url_audio_plano}"
                        if url_audio_plano
                        else "Áudio não disponível",
                    },
                    card_response,
                ],
            }
            return response

    # Se o objetivo não estiver preenchido, pergunta o objetivo
    else:
        mensagem_objetivo = (
            "Por favor, escolha seu objetivo: Emagrecimento ou Hipertrofia."
        )
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

        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "objetivo",
                },
                "intent": {"name": current_intent, "slots": slots},
                "sessionAttributes": session_attributes,  
            },
            "messages": [
                {"contentType": "PlainText", "content": mensagem_objetivo},
                {
                    "contentType": "PlainText",
                    "content": f"Ouça o áudio aqui: {url_audio_objetivo}"
                    if url_audio_objetivo
                    else "Áudio não disponível",
                },
                card_response,
            ],
        }
        return response
        
        


    

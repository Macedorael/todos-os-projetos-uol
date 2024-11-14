import json
import boto3
import hashlib
from datetime import datetime
import os



polly_client = boto3.client('polly')
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

S3_BUCKET = os.getenv('S3_BUCKET')
DYNAMO_TABLE_NAME = os.getenv('DYNAMODB_TABLE')
table = dynamodb.Table(DYNAMO_TABLE_NAME)

def lambda_handler(event, context):
    try:
        # Adicionando log do evento recebido
        print("Evento recebido:", json.dumps(event))

        if event.get("httpMethod") == "POST" and "/tts" in event.get("path", ""):
            # Verifica se o corpo da requisição é válido
            body = event.get("body", "{}")
            try:
                body = json.loads(body)
            except json.JSONDecodeError as e:
                print("Erro ao decodificar JSON:", str(e))
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"Invalid JSON format: {str(e)}"})
                }

            phrase = body.get("phrase", "").strip()

            if not phrase:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "A phrase must be provided."}),
                }

            # Gera um hash code único para a frase
            unique_id = hashlib.md5(phrase.encode()).hexdigest()

            # Verifica se a frase já existe no DynamoDB
            response = table.get_item(Key={'unique_id': unique_id})

            if 'Item' in response:
                # Se o hash já existir, retorna as informações
                item = response['Item']
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'received_phrase': f'texto repetido crie outro texto: {phrase} ',
                        'url_to_audio': item['url_to_audio'],
                        'created_audio': item['created_audio'],
                        'unique_id': unique_id
                    })
                }

            # Se a frase não existe, gera o áudio com AWS Polly
            response = polly_client.synthesize_speech(
                Text=phrase,
                OutputFormat='mp3',
                VoiceId='Ricardo'
            )

            # Salva o áudio no S3
            s3_key = f'audio/{unique_id}.mp3'
            s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=response['AudioStream'].read(), ContentType='audio/mpeg')

            # Cria a URL pública do arquivo de áudio
            audio_url = f'https://{S3_BUCKET}.s3.amazonaws.com/{s3_key}'

            # Cria o timestamp atual
            now = datetime.now()
            created_at = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

            # Grava as informações no DynamoDB
            table.put_item(
                Item={
                    'unique_id': unique_id,
                    'received_phrase': phrase,
                    'url_to_audio': audio_url,
                    'created_audio': created_at
                }
            )

            # Retorna a resposta
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'received_phrase': phrase,
                    'url_to_audio': audio_url,
                    'created_audio': created_at,
                    'unique_id': unique_id
                })
            }
        else:
            print("Endpoint não encontrado. Caminho:", event.get("path", ""))
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Endpoint not found"})
            }

    except Exception as e:
        print("Erro inesperado:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

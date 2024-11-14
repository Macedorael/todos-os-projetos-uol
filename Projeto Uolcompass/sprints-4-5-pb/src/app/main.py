from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, conint, constr
import boto3
import joblib
import os
from dotenv import load_dotenv
import numpy as np
import uvicorn

load_dotenv()

app = FastAPI(
    title="API de Previsão de Valores de Quartos de Hotel",
    description=(
        "API para prever a faixa de preço de reservas de hotéis usando um modelo XGBoost.\n\n"
        "Legendas dos campos:\n"
        "- **no_of_adults (int):** Quantidade de adultos que irão se hospedar no quarto.\n"
        "- **no_of_children (int):** Quantidade de crianças que irão se hospedar no quarto.\n"
        "- **no_of_weekend_nights (int):** Número de noites durante o fim de semana (sábado e domingo) que a reserva ocupa.\n"
        "- **no_of_week_nights (int):** Número de noites durante a semana (de segunda a sexta-feira) que a reserva ocupa.\n"
        "- **type_of_meal_plan (int):** Tipo de plano de refeição incluído na reserva.\n"
        "    0 - No meal plan\n"
        "    1 - Breakfast included\n"
        "    2 - Half board (breakfast and dinner included)\n"
        "    3 - Full board (breakfast, lunch, and dinner included)\n"
        "- **required_car_parking_space (int):** Necessidade de espaço de estacionamento para o carro.\n"
        "    0 - No parking space required\n"
        "    1 - Parking space required\n"
        "- **room_type_reserved (int):** Tipo de quarto reservado.\n"
        "     Room Type 1\n"
        "     Room Type 2\n"
        "     Room Type 3\n"
        "     Room Type 4\n"
        "     Room Type 5\n"
        "     Room Type 6\n"
        "     Room Type 7\n"
        "- **lead_time (int):** Tempo entre a reserva e a chegada (em dias).\n"
        "- **arrival_year (int):** Ano em que a chegada está prevista.\n"
        "- **arrival_month (int):** Mês em que a chegada está prevista.\n"
        "- **market_segment_type (int):** Tipo de segmento de mercado ao qual a reserva pertence.\n"
        "    0 - Offline\n"
        "    1 - Online\n"
        "    2 - Corporate\n"
        "    3 - Aviation\n"
        "    4 - Complementary\n"
        "- **no_of_special_requests (int):** Número de solicitações especiais feitas pelo hóspede."
    ),
    version="1.0.0"
)

# Configurações do bucket S3 e caminho do modelo
s3_bucket = 's3sagemakermo'
model_path = 'modelos/best_xgboost_model.pkl'
local_model_path = 'best_xgboost_model.pkl'  # Caminho local onde o arquivo .pkl será salvo

# Inicializar o cliente S3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN')
)

# Função para testar a conexão com o bucket
def test_s3_connection(bucket: str) -> bool:
    try:
        s3.head_bucket(Bucket=bucket)
        return True
    except Exception as e:
        print(f"Erro ao conectar ao bucket {bucket}: {e}")
        return False

# Função para baixar o modelo do S3 para o diretório local
def download_model(client, bucket: str, s3_key: str, local_path: str) -> bool:
    try:
        client.download_file(Bucket=bucket, Key=s3_key, Filename=local_path)
        return True
    except Exception as e:
        print(f"Erro ao baixar o modelo: {e}")
        return False

# Testar a conexão com o bucket e baixar o modelo
if not test_s3_connection(s3_bucket) or not download_model(s3, s3_bucket, model_path, local_model_path):
    raise SystemExit("Erro ao conectar ao bucket ou baixar o modelo.")

# Tentar carregar o modelo
try:
    model = joblib.load(local_model_path)
except Exception as e:
    raise SystemExit(f"Erro ao carregar o modelo: {e}")

# Definindo o modelo de dados de entrada com validações adicionais
class InferenceRequest(BaseModel):
    no_of_adults: conint(ge=0)  # Deve ser um inteiro não negativo
    no_of_children: conint(ge=0)  # Deve ser um inteiro não negativo
    no_of_weekend_nights: conint(ge=0)  # Deve ser um inteiro não negativo
    no_of_week_nights: conint(ge=0)  # Deve ser um inteiro não negativo
    type_of_meal_plan: conint(ge=0, le=3)  # Deve ser um inteiro entre 0 e 3
    required_car_parking_space: conint(ge=0, le=1)  # Deve ser um inteiro entre 0 e 1
    room_type_reserved: conint(ge=1, le=7)  # Deve ser um inteiro entre 1 e 7
    lead_time: conint(ge=0)  # Deve ser um inteiro não negativo
    arrival_year: conint(ge=2000, le=2100)  # Deve ser um ano válido
    arrival_month: conint(ge=1, le=12)  # Deve ser um mês válido (1-12)
    market_segment_type: conint(ge=0, le=4)  # Deve ser um inteiro entre 0 e 4
    no_of_special_requests: conint(ge=0)  # Deve ser um inteiro não negativo

@app.post("/api/v1/inference")
async def inference(request: InferenceRequest):
    features = [
        request.no_of_adults,
        request.no_of_children,
        request.no_of_weekend_nights,
        request.no_of_week_nights,
        request.type_of_meal_plan,
        request.required_car_parking_space,
        request.room_type_reserved,
        request.lead_time,
        request.arrival_year,
        request.arrival_month,
        request.market_segment_type,
        request.no_of_special_requests,
    ]
    
    try:
        features = np.array([features])  # Converta para um array 2D
        result = model.predict(features)[0]
        return {"result": int(result + 1)}  # Retorna o resultado como um JSON com a chave "result"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na inferência do modelo: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
# Escolhe a imagem base com Python
FROM python:3.9-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação
COPY app /app

# Expõe a porta na qual a aplicação vai rodar
EXPOSE 3000

# Define o comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
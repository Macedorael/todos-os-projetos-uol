# API de Previsão de Valores de Quartos de Hotel

## Índice

1. [Descrição](#descrição)
2. [Funcionalidades Principais](#funcionalidades-principais)
3. [Classificação de Preços](#classificação-de-preços)
4. [Arquitetura da Solução](#arquitetura-da-solução)
5. [Tecnologias Utilizadas](#tecnologias-utilizadas)
6. [Endpoints da API](#endpoints-da-api)
7. [Como Clonar o Repositório](#como-clonar-o-repositório)
8. [Como Executar a API](#como-executar-a-api)
   - [Carregar e Executar a API em uma Instância EC2](#carregar-e-executar-a-api-em-uma-instância-ec2)
   - [Executar a API Localmente](#executar-a-api-localmente)
   - [Guia para Executar a Aplicação com Docker](#guia-para-executar-a-aplicação-com-docker)
9. [Dificuldades](#dificuldades)
   - [Dificuldades com FastAPI](#dificuldades-com-fastapi)
   - [Dificuldades com SageMaker](#dificuldades-com-sagemaker)
10. [Oportunidades de Melhoria](#oportunidades-de-melhoria)
11. [Autores](#autores)
12. [Licenciamento](#licenciamento)

## Descrição
Esta API permite prever os valores de quartos de hotel com base em dados históricos e modelos de machine learning. O sistema é projetado para ajudar hotéis e plataformas de reserva a otimizar preços e melhorar a experiência do usuário.

A infraestrutura da API é construída utilizando serviços da AWS para garantir escalabilidade, confiabilidade e eficiência:

- *AWS EC2*: Hospeda a aplicação em um ambiente seguro e escalável.
- *Docker*: Containeriza a aplicação para facilitar a implantação e gerenciamento.
- *AWS SageMaker*: Realiza o treinamento dos modelos de machine learning de forma eficiente e escalável.
- *AWS RDS*: Gerencia o banco de dados MySQL que armazena os dados da aplicação de maneira segura e confiável.
- *S3*: Armazena modelo e as bases de teste.

## Funcionalidades Principais
- *Previsão de Preços*: Fornece previsões de preços de quartos com base em diversos parâmetros , datas e tipo de quarto.
- *Atualização de Modelos*: Facilita o re-treinamento e atualização dos modelos de machine learning conforme novos dados são disponibilizados.

## Classificação de Preços
O modelo de machine learning classifica os preços médios dos quartos (avg_price_per_room) em três categorias:

- *1: Quando o preço é **menor ou igual a 85*.
- *2: Quando o preço é **maior que 85 e menor que 115*.
- *3: Quando o preço é **maior ou igual a 115*.

## Arquitetura da Solução

### Tecnologias Utilizadas

- **Python**: Linguagem de programação principal utilizada no desenvolvimento da API e dos modelos de machine learning.
- **FastAPI**: Framework web de alto desempenho utilizado para construir a API RESTful.
- **Xgbooster**: Biblioteca de machine learning usada para desenvolver e treinar os modelos de previsão.
- **Docker**: Ferramenta de containerização que garante a portabilidade e consistência do ambiente de execução.
- **AWS EC2 (Elastic Compute Cloud)**: Serviço de computação em nuvem que hospeda a aplicação, proporcionando escalabilidade e segurança.
- **AWS SageMaker**: Plataforma utilizada para construir, treinar e implantar modelos de machine learning em escala.
- **AWS RDS (Relational Database Service)**: Serviço gerenciado de banco de dados relacional utilizado para armazenar dados de forma segura e escalável.
- **AWS S3 (Simple Storage Service)**: Serviço de armazenamento em nuvem que oferece armazenamento seguro, escalável e de alta durabilidade para dados e backups. Utilizado para armazenar datasets, resultados de modelos de machine learning e backups de bancos de dados.
- **Git**: Sistema de controle de versão utilizado para gerenciar o código-fonte do projeto.
- **GitHub**: Plataforma de hospedagem de código utilizada para colaboração e versionamento do projeto.

## Instalação e Configuração

### Pré-requisitos

Antes de iniciar, certifique-se de que você tem os seguintes pré-requisitos instalados e configurados:

- *Python 3.8+*: Certifique-se de que o Python está instalado e configurado corretamente no seu ambiente.
- *Docker*: Necessário para containerizar e executar a aplicação.
- *AWS CLI*: Ferramenta de linha de comando da AWS, configurada com suas credenciais para acessar os serviços da AWS.
- *FastAPI*: Framework utilizado para construir a API. Pode ser instalado via pip install fastapi.
- *MySQL*: Banco de dados utilizado para armazenar os dados da aplicação. Certifique-se de que o MySQL está instalado e rodando.

## Endpoints da API

### POST /predict
- *Descrição*: Gera uma previsão de preço para um quarto de hotel com base nos dados fornecidos.
*Parâmetros*:

- **`no_of_adults` (int)**: Quantidade de adultos que irão se hospedar no quarto.
- **`no_of_children` (int)**: Quantidade de crianças que irão se hospedar no quarto.
- **`no_of_weekend_nights` (int)**: Número de noites durante o fim de semana (sábado e domingo) que a reserva ocupa.
- **`no_of_week_nights` (int)**: Número de noites durante a semana (de segunda a sexta-feira) que a reserva ocupa.
- **`type_of_meal_plan` (int)**: Tipo de plano de refeição incluído na reserva. Opções:
  - `0` - No meal plan
  - `1` - Breakfast included
  - `2` - Half board (breakfast and dinner included)
  - `3` - Full board (breakfast, lunch, and dinner included)
- **`required_car_parking_space` (int)**: Necessidade de espaço de estacionamento para o carro. Opções:
  - `0` - No parking space required
  - `1` - Parking space required
- **`room_type_reserved` (int)**: Tipo de quarto reservado. Opções:
  - `1` - Room Type 1
  - `2` - Room Type 2
  - `3` - Room Type 3
  - `4` - Room Type 4
  - `5` - Room Type 5
  - `6` - Room Type 6
  - `7` - Room Type 7
- **`lead_time` (int)**: Tempo entre a reserva e a chegada (em dias). Por exemplo, se a reserva foi feita 30 dias antes da chegada, o lead time é 30.
- **`arrival_year` (int)**: Ano em que a chegada está prevista.
- **`arrival_month` (int)**: Mês em que a chegada está prevista.
- **`market_segment_type` (int)**: Tipo de segmento de mercado ao qual a reserva pertence. Opções:
  - `0` - Offline
  - `1` - Online
  - `2` - Corporate
  - `3` - Aviation
  - `4` - Complementary
  - **`no_of_special_requests` (int)**: Número de solicitações especiais feitas pelo hóspede.

  - *Requisição*:
  
  **Método HTTP**: POST
  
  **URL**: `/api/v1/inference`
  
  **Descrição**: Envie dados para o modelo e receba uma previsão.
  
  **Corpo da Requisição** (JSON):
  ```json
  {
    "no_of_adults": 2,
    "no_of_children": 1,
    "no_of_weekend_nights": 2,
    "no_of_week_nights": 3,
    "type_of_meal_plan": 1,
    "required_car_parking_space": 1,
    "room_type_reserved": 0,
    "lead_time": 30,
    "arrival_year": 2024,
    "arrival_month": 9,
    "market_segment_type": 2,
    "no_of_special_requests": 2
  }



- **Resposta** (JSON):
    ```json
    {
    "result": 1
    }
    
## Como Clonar o Repositório

Para clonar este repositório, execute o seguinte comando:

```bash
git clone https://github.com/Compass-pb-aws-2024-JUNHO/sprints-4-5-pb-aws-junho.git
```

## Como Executar a API

### Carregar e Executar a API em uma Instância EC2

Para criar e configurar uma instância EC2 e executar a API, siga estes passos:

1. *Acessar o AWS Management Console*:
   - Vá para [AWS Management Console](https://aws.amazon.com/console/) e faça login com suas credenciais.

2. *Iniciar uma Instância EC2*:
   - No console, acesse o serviço "EC2".
   - Clique em "Launch Instance" para iniciar o assistente de criação de instância.
   - Selecione uma Amazon Machine Image (AMI). Recomenda-se usar uma AMI baseada em Ubuntu para compatibilidade.
   - Escolha um tipo de instância adequado (por exemplo, t2.micro para testes).
   - Configure detalhes da instância conforme necessário.
   - Adicione armazenamento, se necessário.
   - Configure o grupo de segurança para permitir o tráfego nas portas necessárias (por exemplo, portas 22 para SSH e 80 para HTTP).
   - Revise e inicie a instância.

3. *Conectar à Instância*:
   - Após a instância ser iniciada, selecione-a no console e clique em "Connect".
   - Siga as instruções fornecidas para conectar via SSH.

4. *Instalar Dependências*:
   - Após conectar, atualize os pacotes da instância:
     ```bash
     sudo apt update
     sudo apt upgrade
     ```
   - Instale o Docker:
     ```bash
     sudo apt install docker.io
     sudo systemctl start docker
     sudo systemctl enable docker
     ```

   - Instale o AWS CLI:
     ``` bash
     sudo apt install awscli
     ```

   - Instale o Python e o pip:
     ```bash
     sudo apt install python3 python3-pip
     ```

   - Instale o FastAPI:
     ```bash
     pip3 install fastapi
     ```

5. *Implantar a Aplicação*:
   - Clone o repositório na instância:
     ```bash
     git clone https://github.com/Compass-pb-aws-2024-JUNHO/sprints-4-5-pb-aws-junho.git
     ```
   - Navegue até o diretório do projeto e inicie a aplicação com Docker ou diretamente usando Python.

### Executar a API Localmente

Para executar a API localmente em sua própria máquina, siga estes passos:

1. *Instalar Dependências Locais*:
   - Certifique-se de que você tem o Python 3.8+ e pip instalados.
   - Instale o FastAPI e outras dependências necessárias:
     bash
     pip install fastapi uvicorn
     

2. *Clonar o Repositório*:
   - Clone o repositório do projeto:
     bash
     git clone https://github.com/Compass-pb-aws-2024-JUNHO/sprints-4-5-pb-aws-junho.git
     

3. *Navegar para o Diretório do Projeto*:
   - Entre no diretório do projeto:
     bash
     cd sprints-4-5-pb-aws-junho
     

4. *Executar a API*:
   - Use o Uvicorn para iniciar a aplicação:
     bash
     uvicorn app:app --reload
     
   - A API estará disponível em http://127.0.0.1:3000.
   - *Documentação Interativa*:
     - *Swagger UI*: Acesse a documentação interativa da API em http://127.0.0.1:3000/docs. O Swagger UI fornece uma interface gráfica onde você pode visualizar todos os endpoints da API, ler suas descrições, e até mesmo testar as chamadas diretamente do navegador.

## Guia para Executar a Aplicação com Docker

Para um guia detalhado sobre como usar Docker para executar sua aplicação, você pode assistir ao tutorial em vídeo [aqui](https://www.youtube.com/watch?v=Kzcz-EVKBEQ). Este tutorial cobre:

- Como instalar o Docker e o Docker Compose.
- Como criar um Dockerfile para sua aplicação.
- Como construir e executar contêineres Docker.
- Como configurar redes e volumes para sua aplicação.

## Dificuldades<a name="dificuldades"></a>

### Dificuldades com FastAPI

- **Versionamento das Bibliotecas**: Enfrentei desafios com a compatibilidade de versões de bibliotecas e comandos depreciados nas atualizações mais recentes do FastAPI. Isso exigiu pesquisa adicional fora do material do curso, incluindo consultas a materiais da Udemy, documentações atualizadas e vídeos externos para solucionar problemas específicos e ajustar a configuração.

- **Integração com AWS**: A integração da API do FastAPI com a AWS foi um desafio significativo devido à falta de conhecimento específico sobre as configurações necessárias e as opções disponíveis para essa integração. O processo de configuração e conexão com os serviços da AWS, como o SageMaker, foi complexo e exigiu estudo adicional e resolução de problemas práticos.

### Dificuldades com SageMaker

- **Análise e Preparação dos Dados**: Enfrentei dificuldades na análise e preparação dos dados para treinamento. Isso incluiu a limpeza e o pré-processamento dos dados de maneira eficiente para garantir a qualidade dos inputs para o modelo.

- **Transformação de Dados Categóricos**: A transformação e a codificação de dados categóricos foram desafiadoras. Foi necessário encontrar a melhor forma de converter categorias em formatos numéricos apropriados para o treinamento do modelo.

- **Seleção de Features**: A seleção das features relevantes para o modelo foi complexa. Identificar quais variáveis tinham maior impacto na performance do modelo e quais poderiam ser descartadas exigiu uma análise aprofundada.

- **Divisão dos Dados - Treino e Teste**: A divisão dos dados em conjuntos de treino e teste foi desafiadora, especialmente em garantir que os dados fossem divididos de maneira que representassem bem a distribuição original e evitassem overfitting ou underfitting.

- **Treinamento do Modelo e Versões dos Frameworks**: O treinamento do modelo foi complicado por problemas relacionados às versões dos frameworks utilizados. Encontrar a configuração correta e lidar com incompatibilidades de versões foi um processo demorado e técnico.

- **Deploy do Modelo**: O processo de deployment do modelo também apresentou dificuldades. Implementar e gerenciar o modelo em um ambiente de produção envolveu desafios relacionados à configuração e manutenção da infraestrutura necessária para suportar o modelo de maneira eficiente.

## Oportunidades de Melhoria<a name="melhorias"></a>

A equipe desenvolvedora acredita que oportunidades de melhorias sempre existirão. No presente processo, ficou demonstrado que a equipe buscou formas de evoluir a solução, seja pelo aspecto da segurança, seja sob o aspecto da continuidade operacional. No entanto, reconhecemos a necessidade de aprimorar a análise de dados, aumentar a assertividade do modelo de machine learning e implementar mais tratamento de erro na entrada dos dados da API. Toda e qualquer sugestão poderá ser encaminhada para os membros da equipe, que desde já agradecem.

## Autor(es)<a name="autores"></a>

<a href="https://www.linkedin.com/in/moniza-pelegrini-9936a1217/" target="_blank">Moniza de Oliveira Silva S. Pelegrini</a><br>
<a href="https://www.linkedin.com/in/john-sousa-28072212ti/" target="_blank">John Lennon Cavalcante de Sousa</a><br>
<a href="https://www.linkedin.com/in/israel-macedo-da-silva-026969245/" target="_blank">Israel Macedo da Silva</a><br>
<a href="https://www.linkedin.com/in/victor-sousa-677912125/" target="_blank">Victor Iuri Sousa</a>

## Do Licenciamento<a name="licenciamento"></a>

Esta aplicação está licenciada para uso como Software Livre podendo ser baixada, utilizada e testada, amplamente por todo e qualquer usuário interessado.
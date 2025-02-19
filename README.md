# Stract test

## Descrição

Este teste implementa um servidor local utilizando **Python + Flask** para consumir os dados da API da Stract e gerar relatórios no formato **CSV**. O servidor fornece endpoints para acessar anúncios de diferentes plataformas de publicidade e realizar agregações de dados conforme especificado no teste técnico.

## 📌 Requisitos

- Python 3.8+
- Package manager <a name="pip" href="https://pip.pypa.io/en/stable/" target="_blank">PIP</a>
- Flask

## 📥 Instalação

1. Clone este repositório:

   ```bash
   git clone git@github.com:raissalst/stract-test.git
   cd stract-test
   ```

2. Crie um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows Power Shell
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Rodando a aplicação

Após instalar as dependências, crie um arquivo .env com base no .env.example com os valores:

```bash
Flask environment: development
Token: ProcessoSeletivoStract2025
URL: https://sidebar.stract.to
```

**_Obs.: os valores estão sendo fornecidos por questão de ser um teste técnico, mas não é a prática recomendada por questões de segurança_**

Execute o seguinte comando para iniciar o servidor em modo desenvolvimento com debug ativo:

```bash
flask --debug run
```

Para rodar a aplicação sem o debug ativo executar:

```bash
flask run
```

O servidor será iniciado no **localhost** na porta padrão (**5000**).

## 📌 Endpoints Disponíveis

### 1️⃣ **Raiz da API**

`GET /`

- Retorna nome, e-mail e LinkedIn de quem desenvolveu.

### 2️⃣ **Relatório por Plataforma**

`GET /{plataforma}`

- Retorna uma tabela com todos os anúncios veiculados na plataforma especificada.
- A tabela contém todos os campos de insights de cada anúncio e o nome da conta associada.

**Exemplo de Resposta:**

```
Platform,Ad Name,Clicks,Impressions,Spend
Facebook,Some Ad,10,500,50
Facebook,Other Ad,20,700,80
YouTube,One More Ad,5,200,20
```

### 3️⃣ **Resumo por Plataforma**

`GET /{plataforma}/resumo`

- Retorna uma tabela agrupada por conta, somando valores numéricos.

**Exemplo de Resposta:**

```
Platform,Ad Name,Clicks,Impressions,Spend
Facebook,,30,1200,130
YouTube,,5,200,20
```

### 4️⃣ **Relatório Geral**

`GET /geral`

- Retorna todos os anúncios de todas as plataformas.
- Inclui colunas para identificar a plataforma e a conta.
- Campos ausentes em uma plataforma aparecerão vazios.

**Exemplo de Resposta:**

```
Platform,Account,Ad Name,Clicks,Impressions,Spend,Cost per Click
Facebook,Conta 1,Some Ad,10,500,50,5.0
Facebook,Conta 2,Other Ad,20,700,80,4.0
YouTube,Conta 3,One More Ad,5,200,20,4.0
```

### 5️⃣ **Resumo Geral**

`GET /geral/resumo`

- Retorna uma tabela agregada por plataforma, somando valores numéricos.

**Exemplo de Resposta:**

```
Platform,Ad Name,Clicks,Impressions,Spend
Facebook,,30,1200,130
YouTube,,5,200,20
```

## 🔧 Implementação

O código utiliza **Flask** para criar os endpoints e para consumir a API da Stract.

### Principais Funcionalidades:

✅ Consumo de dados de múltiplos endpoints da API da Stract.
✅ Manipulação e agregação de dados para gerar relatórios estruturados.
✅ Exposição dos dados via endpoints em formato CSV.
✅ Cálculo do **Cost per Click** para Google Analytics (spend / clicks).

## 📝 Estrutura do Projeto

```
stract-test/
├── ./app
│   ├── ./app/controllers
│   ├── ./app/exceptions
│   ├── ./app/external_api
│   ├── ./app/__init__.py
│   ├── ./app/__pycache__
│   ├── ./app/routes
│   ├── ./app/services
│   └── ./app/utils
├── ./README.md
├── ./requirements.txt
```

## 📧 Contato

📌 Nome: Raissa Laubenbacher Sampaio de Toledo
📩 Email: raissalst@gmail.com
🔗 LinkedIn: [seu-linkedin](https://www.linkedin.com/in/raissalstoledo/)

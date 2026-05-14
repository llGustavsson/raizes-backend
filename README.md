# raizes-backend
Projeto Raizes Back-end utilizando FastAPI

# API 
API RESTful desenvolvida para o gerenciamento de pedidos, cardápio, autenticação e simulação de pagamentos de uma rede de restaurantes.

## Tecnologias

* **Python 3.10+**
* **FastAPI**
* **SQLAlchemy 2.0**
* **SQLite**
* **Argon2**
* **PyJWT**
* **Pydantic v2**
* **Uvicorn**

## Requisitos
* **Python 3.10+ instalado**

##  Como Configurar e Executar

### 1. Clonar o repositório
```bash
git clone https://github.com/llGustavsson/raizes-backend.git
cd raizes-backend
```
### 2. Criar e ativar o ambiente virtual
```bash
python -m venv .venv
```

Windows: `.\.venv\Scripts\activate`

Linux / Mac: `source .venv/bin/activate`

### 3. Instalar as dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente (.env)

Crie um arquivo .env na raiz do projeto baseado no exemplo fornecido:

```bash
nano .env

```
Preencha o arquivo .env com as suas configurações:
```bash
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
EXPIRE_MINUTES=30
DATABASE_URL=sqlite:////home/user/folder-example/raizes-backend/test.db (coloque um PATH absoluto)
```
### 5. Iniciar o Banco de Dados e a API

A criação das tabelas ocorrerá automaticamente na inicialização da aplicação via SQLAlchemy ou da Seed.

Popule o banco de dados com os produtos
```bash
python seed.py
```
Inicie a API

```bash
cd app/api
fastapi dev
```
A API estará disponível localmente em: `http://127.0.0.1:8000`

### 6. Documentação da API (Swagger / OpenAPI)

A documentação interativa dos contratos (Request/Response) e a interface de testes direta no navegador são geradas automaticamente pelo FastAPI.

Swagger UI: `http://127.0.0.1:8000/docs`

ReDoc: `http://127.0.0.1:8000/redoc`

## 7. Endpoints Principais

A lista abaixo resume os recursos implementados. Para detalhes de payloads e status codes, consulte a documentação interativa (Swagger).

| Método |     Rota      |      Descrição                        | Permissão   |
| ------ | ------------- | ------------------------------------- | ----------- |
| POST   | /users/signup | Cadastro de usuário                   | Público     |
| POST   | /auth/login   | Login e emissão de token JWT          | Público     |
| PATCH  | /users/me     | Atualização de senha/dados do usuário | JWT (ambos) |
| GET    | /products     |Listagem de cardápio                   | JWT (ambos) |
| POST   | /orders       |Criação de um novo pedido              |JWT (Cliente)|
| POST   | /payments/mock|Simulação de processamento de pagamento|JWT (Cliente)|
| GET    | /auth/verify  |Verifica Token JWT                     | JWT (ambos) |


## 8. Testes da API (Insomnia)

O projeto contempla 10 cenários de testes cobrindo fluxos positivos e negativos. A coleção completa (formato Insomnia v5) está disponível no repositório.

Arquivo: `docs/insomnia_collection.json`

Como executar os testes:

Abra o Insomnia e importe o arquivo JSON acima.

O ambiente Base Environment já está configurado com a base_url (http://127.0.0.1:8000). Mude para o seu localhost se necessário

Execute as requisições na ordem abaixo. Não esqueça de copiar o token gerado no response do passo T02 e colar na aba Auth (Bearer) dos endpoints protegidos.

    
Cenários Cobertos:
| ID  | Cenário  (nome na coleção)   | Tipo     | Rota	             | Resultado        |
| --- | ---------------------------- | -------- | ------------------ | ---------------- |
| T01 |	SignUp	                     | Positivo | POST /users/signup | 201 Created      |
| T02 |	LogIn	                     | Positivo | POST /auth/login	 | 200 OK + JWT     |
| T03 |	Products                     | Positivo | GET /products	     | 200 OK (Lista)   |
| T04 | Create Order                 | Positivo | POST /orders	     | 201 Created      |
| T05 |	Create Order                 | Negativo | POST /orders	     | 400 Bad Request  |
| T06 |	Payment Approved             | Positivo | POST /payments/mock| Status PAID      |
| T07 |	Payment Repaying             | Negativo | POST /payments/mock| Status CANCELED  |
| T08 |	SignUp sem consentimento LGPD| Negativo | POST /users/signup | 422 Unprocessable|
| T09 |	User Password Update         | Positivo | PATCH /users/me	 | 200 OK           |
| T10 |	Login com email errado       | Negativo | POST /auth/login   | 401 Unauthorized |


## 9. Segurança e Privacidade (LGPD)

Hashing: Senhas armazenadas utilizando criptografia robusta (Argon2).

Consentimento: O cadastro exige um campo explícito de opt-in (lgpd_consent: true).

Auditoria: Operações sensíveis financeiras (criação de pedido e pagamentos) geram entradas automáticas no banco de dados para garantir rastreabilidade, sem expor dados pessoais desnecessários.
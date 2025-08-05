# API Flask para Gestão de Clientes, Pedidos e Produtos

Este projeto é uma API RESTful desenvolvida com Flask, destinada à gestão de clientes, pedidos e produtos. Além das operações CRUD para clientes e pedidos, a API permite importação e exportação de produtos e clientes por arquivos CSV.

---

## 🤝 Tecnologias Utilizadas

* **Python 3.x**
* **Flask**
* **SQLite** (banco padrão, mas pode ser adaptado)
* **Módulos**: `csv`, `io`, `json`, `flask`

---

## 🚀 Como Executar o Projeto

1. **Clone o repositório ou baixe os arquivos**

2. **Instale as dependências**:

```bash
pip install -r requirements.txt
```

3. **Configure o banco de dados**:

Execute o script:

```bash
python create_db.py
```

4. **Inicie o servidor**:

```bash
python main.py
```

A API estará disponível em: `http://localhost:5000`

---

## 🔧 Principais Endpoints

### 📦 Produtos

- `GET /produtos`: Lista todos os produtos (suporta filtros por nome e faixa de preço).
- `POST /produtos`: Cadastra um novo produto.
- `PUT /produtos/<id>`: Atualiza um produto existente.
- `DELETE /produtos/<id>`: Remove um produto pelo ID.

#### 🧾 CSV
- `GET /download_file`: Exporta produtos para um arquivo CSV.
- `POST /upload_file`: Importa produtos via arquivo CSV.

---

### 👤 Clientes

- `GET /clientes`: Lista todos os clientes (filtros por nome, e-mail ou CPF).
- `POST /clientes`: Cadastra um novo cliente (com validação de e-mail e CPF).
- `PUT /clientes/<id>`: Atualiza dados de um cliente.
- `DELETE /clientes/<id>`: Remove um cliente pelo ID.

#### 🧾 CSV
- `GET /download_file_clientes`: Exporta os clientes cadastrados para CSV.
- `POST /upload_file_clientes`: Importa clientes via CSV.

---

### 🛒 Pedidos

- `GET /pedidos`: Lista pedidos com filtros opcionais.
- `POST /pedidos`: Cadastra um novo pedido (cliente, produto e quantidade).
- `PUT /pedidos/<id>`: Atualiza um pedido.
- `DELETE /pedidos/<id>`: Remove um pedido pelo ID.

---

## 🗂 Estrutura do Projeto

```
projeto-api/
├── create_db.py             # Criação do banco e tabelas
├── main.py                  # Lógica principal da API
├── validation.py            # Validações de e-mail e CPF
├── requirements.txt         # Dependências
└── README.md                
```

---

## 📌 Funcionalidades Extras

✔️ Validação de campos obrigatórios  
✔️ Validação de formato de e-mail e CPF  
✔️ Upload e download em CSV  
✔️ Filtros por nome, CPF, faixa de preço e quantidade  
✔️ Tratamento de erros e mensagens claras para o usuário  

---

## 🙋‍♀️ Desenvolvido Por:

**Bruna Geovanna dos Santos Pelloso**   
Contato: brupelloso25@gmail.com
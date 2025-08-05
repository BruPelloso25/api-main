from flask import Flask, request, jsonify, send_file
import sqlite3 
import csv 
import io 
import validation 

app = Flask(__name__) 

def get_db_connection():
    conn = sqlite3.connect('api_db.db') 
    conn.row_factory = sqlite3.Row
    return conn 

@app.route('/')
def hello():
    return {"message": "Hello World!"} 

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    conn = get_db_connection() 
    cursor = conn.cursor() 

    query = 'SELECT * FROM produtos WHERE 1=1' 
    parametros = [] 

    preco_min = request.args.get('preco_min') 
    preco_max = request.args.get('preco_max') 
    nome = request.args.get('produto') 

    if preco_min: 
        query += ' AND preco >= ?' 
        parametros.append(float(preco_min))
    if preco_max: 
        query += ' AND preco <= ?' 
        parametros.append(float(preco_max)) 
    if nome:
        query += ' AND produto LIKE ?'
        parametros.append(f'%{nome}%') 
    
    produtos = cursor.execute(query, parametros).fetchall() 
    conn.close()
    return jsonify([dict(row) for row in produtos]) 

@app.route('/produtos', methods=['POST'])
def criar_produto(): 
    dados = request.get_json()
    produto = dados.get('produto') 
    preco = dados.get('preco')

    conn = get_db_connection() 
    cursor = conn.cursor() 
    cursor.execute('INSERT INTO produtos (produto, preco) VALUES (?, ?)', (produto, preco)) 
    conn.commit() 
    produto_id = cursor.lastrowid 
    conn.close()
    return jsonify({
    'mensagem': 'Produto cadastrado com sucesso!',
    'Produto': dados
    }), 201 

@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id): 
    dados = request.get_json() 
    produto = dados.get('produto') 
    preco = dados.get('preco')
    conn = get_db_connection()
    conn.execute('UPDATE produtos SET produto = ?, preco = ? WHERE id = ?', (produto, preco, id)) 
    conn.commit() 
    conn.close() 
    return jsonify(dados) 

@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id): 
    conn = get_db_connection() 
    conn.execute('DELETE FROM produtos WHERE id = ?', (id,)) 
    if conn.total_changes == 0: 
        return jsonify({'mensagem': 'Produto nao encontrado!'}), 404
    conn.commit() 
    conn.close()
    return jsonify({'mensagem': 'Produto removido com sucesso!'}) 

@app.route('/clientes', methods=['GET'])
def listar_clientes(): 
    nome = request.args.get('nome') 
    email = request.args.get('email') 
    cpf = request.args.get('cpf') 

    query = 'SELECT * FROM clientes WHERE 1=1' 
    parametros = []

    if nome: 
        query += ' AND LOWER(nome) LIKE ?'
        parametros.append(f"%{nome.lower()}%") 

    if email: 
        query += ' AND email = ?' 
        parametros.append(email)  
    if cpf: 
        query += ' AND cpf = ?' 
        parametros.append(f"{cpf}%") 
    
    conn = get_db_connection() 
    clientes = conn.execute(query, parametros).fetchall() 
    conn.close() 
    return jsonify([dict(row) for row in clientes]) 

@app.route('/clientes', methods=['POST'])
def criar_cliente(): 
    dados = request.get_json() 
    nome = dados.get('nome')
    email = dados.get('email') 
    cpf = dados.get('cpf') 
    
    erros = []

    if not nome or not email or not cpf: 
        return jsonify({'mensagem': 'Todos os campos obrigatórios devem ser preenchidos!'}), 400 
    
    if not validation.validar_email(email): 
        erros.append('Email inválido!')
    
    if not validation.validar_cpf(cpf):
        erros.append('CPF inválido!')

    if erros:
        return jsonify({'erros': erros}), 400 
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cliente_existente = cursor.execute('SELECT * FROM clientes WHERE email = ? OR cpf = ?', (email, cpf,)).fetchone() 
    
    if cliente_existente: 
        conn.close()
        return jsonify({'mensagem': 'Cliente já está cadastrado!'}), 409  
    cursor.execute('INSERT INTO clientes (nome, email, cpf) VALUES (?, ?, ?)', (nome, email, cpf)) 
    conn.commit() 
    clientes_id = cursor.lastrowid 
    conn.close() 
    return jsonify({
    'mensagem': 'Cliente cadastrado com sucesso!',
    'cliente': dados
    }), 201 

@app.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id): 
    dados = request.get_json()
    nome = dados.get('nome')
    email = dados.get('email') 
    cpf = dados.get('cpf') 

    conn = get_db_connection() 
    conn.execute('UPDATE clientes SET nome = ?, email = ?, cpf = ?WHERE id = ?', (nome, email, cpf, id)) 
    conn.commit() 
    conn.close()
    return jsonify(dados) 

@app.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id): 
    conn = get_db_connection() 
    conn.execute('DELETE FROM clientes WHERE id = ?', (id,)) 
    if conn.total_changes == 0: 
        return jsonify({'mensagem': 'Cliente nao encontrado!'}), 404
    conn.commit() 
    conn.close() 
    return jsonify({'mensagem': 'Cliente removido com sucesso!'}) 

@app.route('/pedidos', methods=['GET']) 
def listar_pedidos(): 
    cliente_nome = request.args.get('cliente') 
    produto_nome = request.args.get('produto') 
    qtd_min = request.args.get('quantidade_min')
    qtd_max = request.args.get('quantidade_max') 

    query = '''
        SELECT pedidos.id,
               clientes.nome AS cliente,
               produtos.produto AS produto,
               pedidos.quantidade_de_produto
        FROM pedidos
        INNER JOIN clientes ON pedidos.cliente_id = clientes.id
        INNER JOIN produtos ON pedidos.produto_id = produtos.id
        WHERE 1=1
    ''' 
    params = [] 

    if cliente_nome:
        query += ' AND clientes.nome LIKE ?'
        params.append(f'%{cliente_nome}%') 

    if produto_nome:
        query += ' AND produtos.produto LIKE ?' 
        params.append(f'%{produto_nome}%') 

    if qtd_min: 
        query += ' AND pedidos.quantidade_de_produto >= ?' 
        params.append(qtd_min) 

    if qtd_max: 
        query += ' AND pedidos.quantidade_de_produto <= ?' 
        params.append(qtd_max)

    conn = get_db_connection()
    pedidos = conn.execute(query, params).fetchall()
    conn.close() 

    return jsonify([dict(row) for row in pedidos]) 

@app.route('/pedidos', methods=['POST'])
def criar_pedido(): 
    dados = request.get_json()
    cliente_id = dados.get('cliente_id') 
    produto_id = dados.get('produto_id') 
    quantidade_de_produto = dados.get('quantidade_de_produto')

    conn = get_db_connection() 
    cursor = conn.cursor() 
    conn.execute('INSERT INTO pedidos (cliente_id, produto_id, quantidade_de_produto) VALUES (?, ?, ?)',
                 (cliente_id, produto_id, quantidade_de_produto)) 
    conn.commit() 
    pedido_id = cursor.lastrowid 
    conn.close() 
    return jsonify(dados) 

@app.route('/pedidos/<int:id>', methods=['PUT'])
def atualizar_pedido(id): 
    dados = request.get_json() 
    cliente_id = dados.get('cliente_id') 
    produto_id = dados.get('produto_id') 
    quantidade_de_produto = dados.get('quantidade_de_produto') 

    conn = get_db_connection()
    conn.execute('UPDATE pedidos SET cliente_id = ?, produto_id = ?, quantidade_de_produto = ? WHERE id = ?',
                 (cliente_id, produto_id, quantidade_de_produto, id)) 
    conn.close() 
    return jsonify(dados) 

@app.route('/pedidos/<int:id>', methods=['DELETE'])
def remover_pedido(id): 
    conn = get_db_connection() 
    conn.execute('DELETE FROM pedidos WHERE id = ?', (id,))
    if conn.total_changes == 0: 
        return jsonify({'mensagem': 'Pedido nao encontrado!'}), 404
    conn.commit() 
    conn.close() 
    return jsonify({"mensagem": "Pedido removido com sucesso"}) 


@app.route('/download_file', methods=['GET'])
def download_file(): 
    conn = get_db_connection() 
    produtos = conn.execute('SELECT * FROM produtos').fetchall() 
    conn.close() 

    output = io.StringIO() 
    writer = csv.writer(output) 
    writer.writerow(['id', 'produto', 'preco']) 

    for produto in produtos: 
        writer.writerow([produto['id'], produto['produto'], produto['preco']]) 
    output.seek(0) 
    return send_file( 
        io.BytesIO(output.getvalue().encode()), 
        mimetype='text/csv', 
        as_attachment=True, 
        download_name='produtos.csv' 
    )

@app.route('/download_file_clientes', methods=['GET'])
def download_file_clientes(): 
    conn = get_db_connection() 
    clientes = conn.execute('SELECT * FROM clientes').fetchall() 
    conn.close()
    output = io.StringIO() 
    writer = csv.writer(output) 
    writer.writerow(['nome', 'email', 'cpf']) 

    for cliente in clientes: 
        writer.writerow([cliente['nome'], cliente['email'], cliente['cpf']]) 

    output.seek(0)
    return send_file( 
        io.BytesIO(output.getvalue().encode()), 
        mimetype='text/csv', 
        as_attachment=True, 
        download_name='clientes.csv' 
    )

@app.route('/upload_file', methods=['POST'])
def upload_file(): 
    if 'file' not in request.files: 
        return jsonify({"erro": "Nenhum arquivo foi enviado"}), 400 

    file = request.files['file'] 
    if not file.filename.endswith('.csv'):
        return jsonify({"erro": "Formato inválido. Envie um arquivo CSV"}), 400 

    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None) 
    reader = csv.DictReader(stream) 

    conn = get_db_connection() 
    cursor = conn.cursor()
    ids_ignorados = [] 

    for row in reader: 
        if not row['id'] or not row['produto'] or not row['preco']: 
            ids_ignorados.append(row.get('id', 'sem_id')) 
            continue 

        try: 
            produto = row['produto'].strip() 
            preco = float(row['preco']) 
            cursor.execute(
                'INSERT INTO produtos (produto, preco) VALUES (?, ?)',
                (produto, preco)
            ) 
        except Exception: 
            ids_ignorados.append(row.get('id', 'sem_id')) 

    conn.commit() 
    conn.close() 

    return jsonify({
        "mensagem": "Upload processado",
        "ids_ignorados": ids_ignorados
    }) 


@app.route('/upload_file_clientes', methods=['POST'])
def upload_file_clientes(): 
    if 'file' not in request.files: 
        return jsonify({"erro": "Nenhum arquivo foi enviado"}), 400 

    file = request.files['file'] 
    if not file.filename.endswith('.csv'):
        return jsonify({"erro": "Formato inválido. Envie um arquivo CSV"}), 400 
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None) 
    reader = csv.DictReader(stream) 

    conn = get_db_connection() 
    cursor = conn.cursor() 
    cpf_ignorados = [] 

    for row in reader: 
        if not row['nome'] or not row['email'] or not row['cpf']: 
            cpf_ignorados.append(row.get('cpf', 'sem_cpf')) 
            continue 
        try: 
            nome = row['nome'].strip() 
            email = (row['email'])
            cpf = str(row['cpf'])

            cursor.execute( 
                'INSERT INTO clientes (nome, email, cpf) VALUES (?, ?, ?)',
                (nome, email, cpf)
            ) 
        except Exception:
            cpf_ignorados.append(row.get('cpf', 'sem_cpf')) 

    conn.commit() 
    conn.close() 

    return jsonify({
        "mensagem": "Upload processado",
        "cpf's_ignorados": cpf_ignorados
    }) 

app.run(debug=True) 
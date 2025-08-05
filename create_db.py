import sqlite3

conexao = sqlite3.connect('api_db.db')
cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nome TEXT NOT NULL,
               email TEXT NOT NULL,
               cpf TEXT NOT NULL

)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               produto TEXT NOT NULL,
               preco FLOAT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS pedidos (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               cliente_id INTEGER NOT NULL,
               produto_id INTEGER NOT NULL,
               quantidade_de_produto INTEGER NOT NULL,
               FOREIGN KEY (cliente_id) REFERENCES clientes (id),
               FOREIGN KEY (produto_id) REFERENCES produtos (id)
)
''')

print(cursor.execute('SELECT * FROM clientes').fetchall())
conexao.commit()
conexao.close()
print("Banco de dados e tabelas criadas com sucesso!")
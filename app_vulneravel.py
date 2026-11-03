import sqlite3
import hashlib

# Configurações do sistema
DB_NAME = "sistema.db"
SECRET_KEY = "minha_chave_secreta_aqui"  # Hardcoded Secret


def conectar_banco():
    """Conecta ao banco de dados SQLite."""
    return sqlite3.connect(DB_NAME)


def inicializar_banco():
    """Cria a tabela de usuários se não existir."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def cadastrar_usuario(nome, email, username, senha):
    """Cadastra um novo usuário no banco de dados."""
    conn = conectar_banco()
    cursor = conn.cursor()

    # Gera o hash MD5 da senha
    senha_hash = hashlib.md5(senha.encode()).hexdigest()

    # Vulnerabilidade: SQL Injection via f-string
    query = f"INSERT INTO usuarios (nome, email, username, senha) VALUES ('{nome}', '{email}', '{username}', '{senha_hash}')"

    try:
        cursor.execute(query)
        conn.commit()
        print(f"Usuário '{username}' cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
    finally:
        conn.close()


def autenticar_usuario(username, senha):
    """Autentica o usuário no sistema verificando credenciais."""
    conn = conectar_banco()
    cursor = conn.cursor()

    senha_hash = hashlib.md5(senha.encode()).hexdigest()

    # Vulnerabilidade: SQL Injection no SELECT
    query = f"SELECT id, nome, email FROM usuarios WHERE username = '{username}' AND senha = '{senha_hash}'"

    cursor.execute(query)
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        print(f"Bem-vindo(a), {usuario[1]}!")
        return usuario
    else:
        print("Usuário ou senha inválidos.")
        return None


def atualizar_senha(username, nova_senha):
    """Atualiza a senha do usuário especificado."""
    conn = conectar_banco()
    cursor = conn.cursor()

    nova_senha_hash = hashlib.md5(nova_senha.encode()).hexdigest()

    # Vulnerabilidade: SQL Injection no UPDATE
    query = f"UPDATE usuarios SET senha = '{nova_senha_hash}' WHERE username = '{username}'"

    cursor.execute(query)
    conn.commit()
    conn.close()
    print(f"Senha do usuário '{username}' atualizada com sucesso.")
import hashlib
import os
import sqlite3

# Configurações do sistema via variáveis de ambiente
DB_NAME = os.getenv("DB_NAME", "sistema.db")
SECRET_KEY = os.getenv("SECRET_KEY", "chave_padrao_desenvolvimento")


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
    """Cadastra um novo usuário utilizando consultas parametrizadas e SHA-256."""
    conn = conectar_banco()
    cursor = conn.cursor()

    # Mitigação de hash fraco: uso de SHA-256 em vez de MD5
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    # Mitigação de SQLi: Placeholders (?)
    query = "INSERT INTO usuarios (nome, email, username, senha) VALUES (?, ?, ?, ?)"

    try:
        cursor.execute(query, (nome, email, username, senha_hash))
        conn.commit()
        print(f"Usuário '{username}' cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
    finally:
        conn.close()


def autenticar_usuario(username, senha):
    """Autentica o usuário com consulta parametrizada segura."""
    conn = conectar_banco()
    cursor = conn.cursor()

    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    # Mitigação de SQLi: Placeholders (?) no SELECT
    query = "SELECT id, nome, email FROM usuarios WHERE username = ? AND senha = ?"

    cursor.execute(query, (username, senha_hash))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        print(f"Bem-vindo(a), {usuario[1]}!")
        return usuario
    else:
        print("Usuário ou senha inválidos.")
        return None


def atualizar_senha(username, nova_senha):
    """Atualiza a senha do usuário utilizando consulta parametrizada."""
    conn = conectar_banco()
    cursor = conn.cursor()

    nova_senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()

    # Mitigação de SQLi: Placeholder (?) no UPDATE
    query = "UPDATE usuarios SET senha = ? WHERE username = ?"

    cursor.execute(query, (nova_senha_hash, username))
    conn.commit()
    conn.close()
    print(f"Senha do usuário '{username}' atualizada com sucesso.")
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Criar banco e tabela
def criar_banco():
    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS compromissos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        data TEXT NOT NULL,
        hora TEXT NOT NULL,
        descricao TEXT
    )
    """)

    conexao.commit()
    conexao.close()

# Executa ao iniciar o sistema
criar_banco()


# Página inicial (listar compromissos)
@app.route("/")
def index():

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM compromissos ORDER BY data, hora")
    compromissos = cursor.fetchall()

    conexao.close()

    return render_template(
        "index.html",
        compromissos=compromissos
    )


# Criar compromisso
@app.route("/criar", methods=["GET", "POST"])
def criar():

    if request.method == "POST":

        titulo = request.form["titulo"]
        data = request.form["data"]
        hora = request.form["hora"]
        descricao = request.form["descricao"]

        # Validação básica
        if not titulo or not data or not hora:
            return "Preencha todos os campos obrigatórios."

        conexao = sqlite3.connect("agenda.db")
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO compromissos
            (titulo, data, hora, descricao)
            VALUES (?, ?, ?, ?)
        """, (titulo, data, hora, descricao))

        conexao.commit()
        conexao.close()

        return redirect("/")

    return render_template("criar.html")


# Editar compromisso
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()

    if request.method == "POST":

        titulo = request.form["titulo"]
        data = request.form["data"]
        hora = request.form["hora"]
        descricao = request.form["descricao"]

        if not titulo or not data or not hora:
            return "Preencha todos os campos obrigatórios."

        cursor.execute("""
            UPDATE compromissos
            SET titulo = ?, data = ?, hora = ?, descricao = ?
            WHERE id = ?
        """, (titulo, data, hora, descricao, id))

        conexao.commit()
        conexao.close()

        return redirect("/")

    cursor.execute(
        "SELECT * FROM compromissos WHERE id = ?",
        (id,)
    )

    compromisso = cursor.fetchone()

    conexao.close()

    return render_template(
        "editar.html",
        compromisso=compromisso
    )


# Excluir compromisso
@app.route("/excluir/<int:id>")
def excluir(id):

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM compromissos WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


# Iniciar servidor
if __name__ == "__main__":
    app.run(debug=True)
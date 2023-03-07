# -*- coding: utf-8 -*-
from flask import Flask, request
import configparser
import psycopg2

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')
start_time = config['Time']['start']
end_time = config['Time']['end']

# Conecta com o banco de dados PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="database_name",
    user="username",
    password="password"
)
c = conn.cursor()

# Cria a tabela authorized caso não exista
c.execute('''CREATE TABLE IF NOT EXISTS authorized
             (name text)''')
conn.commit()

# Adiciona alguns nomes de exemplo na base de dados
c.execute("INSERT INTO authorized VALUES ('Pedro')")
c.execute("INSERT INTO authorized VALUES ('Angelica')")

conn.commit()
conn.close()

# Rota para receber as informações de hora e nome
@app.route('/authorize', methods=['POST'])
def authorize():
    name = request.form['name']
    time = request.form['time']

    # Verifica se o nome está na base de dados de autorizados
    conn = psycopg2.connect(
        host="localhost",
        database="database_name",
        user="username",
        password="password"
    )
    c = conn.cursor()
    c.execute("SELECT name FROM authorized WHERE name=%s", (name,))
    result = c.fetchone()
    conn.close()

    if result is None:
        return "Não autorizado"

    # Verifica se a hora está dentro do intervalo permitido
    if time < start_time or time > end_time:
        return "Não autorizado"

    return "Autorizado"


if __name__ == '__main__':
    app.run(debug=True)
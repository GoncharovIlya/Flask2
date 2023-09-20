from flask import Flask, render_template, jsonify, abort, g
import sqlite3
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
DATABSE = BASE_DIR / 'flask2.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABSE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.get('/')
def home():
    return render_template('index.html')

@app.route('/names/insert', methods = ['POST'])
def names_insert():
    conn_to_db = get_db()
    cursor = conn_to_db.cursor()
    with open('files/names.txt', encoding = 'utf-8') as file:
        for raw in file:
            raw = raw.strip()
            insert = 'insert into names (name) values (?)'
            cursor.execute(insert, (raw,))
            conn_to_db.commit()
        return 200

@app.route('/names')
def names():
    conn_to_db = get_db()
    cursor = conn_to_db.cursor()
    select = 'select name from names'
    cursor.execute(select)
    sel_db = cursor.fetchall()
    return render_template('names.html', sel_db=sel_db)

@app.route('/tables/insert', methods = ['POST'])
def tables_insert():
    conn_to_db = get_db()
    cursor = conn_to_db.cursor()
    with open('files/humans.txt', encoding = 'utf-8') as file:
        for raw in file:
            data = raw.strip().split(';')
            insert = 'insert into humans (last_name, name, surname) values (?, ?, ?)'
            cursor.execute(insert, (data[0], data[1], data[2]))
            conn_to_db.commit()
        return 200
    
@app.route('/tables')
def tables():
    conn_to_db = get_db()
    cursor = conn_to_db.cursor()
    select = 'select last_name, name, surname from humans'
    for raw in select:
        cursor.execute(select)
        sel_db = cursor.fetchall()
    # table = list()
    # for raw in sel_db:
    #     table.append(dict(zip(('last_name', 'name', 'surname'), raw)))
    return render_template('tables.html', sel_db=sel_db)

@app.route('/users')
def users():
    user = list()
    with open('files/users.txt', encoding = 'utf-8') as file:
        for raw in file:
            data = raw.strip().split(';')
            user.append(dict(zip(('login', 'last_name', 'name', 'surname', 'date_of_birth', 'phone'), data)))
    return render_template('users.html', **{'user': user})

@app.route('/users/<login>')
def users_info(login):
    with open('files/users.txt', encoding = 'utf-8') as file:
        for raw in file:
            data = raw.strip().split(';')
            if data[0] == login:                
                user_l = (dict(zip(('login', 'last_name', 'name', 'surname', 'date_of_birth', 'phone'), data)))
                return render_template('user_info.html', **{'user_l': user_l})
        else:
            abort(404, 'Нет такой записи')

@app.route('/about')
def about():
    return 'About us'

if __name__ == '__main__':
    app.run(debug=True)
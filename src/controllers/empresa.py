from flask import Flask, render_template,session,flash,redirect,request,url_for
import flask
from werkzeug.security import generate_password_hash
import psycopg2
import psycopg2.extras
import re
from database.db import get_conection
conn = get_conection()

# Blueprint - Usuario
empresa = flask.Blueprint('empresa', __name__)

@empresa.route('/empresa')
def empresas():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM empresa')
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('empresa.html', empresa=data[0])





    # Editar cliente
@empresa.route('/update_empresa/<id>', methods=['POST'])
def update_empresa(id):
        

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute('SELECT * FROM empresa')
        data = cur.fetchall()
        cur.close()
        print(data[0])
        

        if request.method == 'POST':
            id = request.form['id']
            nombrecomercial = request.form['nombrecomercial']
            razonsocial = request.form['razonsocial']
            telefono = request.form['telefono']
            email = request.form['email']
            direccion = request.form['direccion']

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
              UPDATE empresa
              SET id           = %s,
                  nombrecomercial    = %s,
                  razonsocial  = %s,
                  telefono        = %s,
                  email         = %s,
                  direccion           = %s
              WHERE id             = %s
          """, (id, nombrecomercial, razonsocial, telefono, email, direccion, id,))
            flash('Cambios guardados con éxito')
            conn.commit()
            return redirect(url_for('empresa.empresas'))
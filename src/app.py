from flask import Flask, render_template, url_for, request, redirect, flash, session
# from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
import re
from database.db import get_conection

from controllers.user import users
from controllers.cliente import clientes
from controllers.empresa import empresa

conn = get_conection()
# <!-- ============================================================== -->
app = Flask(__name__)
app.secret_key = "rokugan"
# <!-- ============================================================== -->
app.register_blueprint(users)
app.register_blueprint(clientes)
app.register_blueprint(empresa)
# app.register_blueprint(product)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    

        

    return render_template('admin.html')

# LOGIN ROUTE
@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        cedula = request.form['cedula']
        contrasena = request.form['contrasena']

        cursor.execute('SELECT * FROM usuario WHERE cedula = %s AND contrasena = %s', (cedula, contrasena))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['cedula'] = account['cedula']
            session['cargo'] = account['cargo']
            session['nombres'] = account['nombres']
            session['apellidos'] = account['apellidos']
            session['telefono'] = account['telefono']
            session['email'] = account['email']

            if session['cargo'] == "Administrador":
                
                return render_template('admin.html')
            
        else:
            flash('BIENVENIDO SEÑOR')

    return render_template('nuevo_cliente.html')









# CERRAR SESIÓN
# @app.route('/logout')
# def logout():
#     # Remove session data, this will log the user out
#     session.pop('loggedin', None)
#     session.pop('cedula', None)
#     session.pop('tipo_usuario', None)
#     session.clear()
#     # Redirect to login page
#     return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)


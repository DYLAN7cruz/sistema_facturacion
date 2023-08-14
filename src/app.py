from flask import Flask, render_template, url_for, request, redirect, flash, session
# from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
import re
from database.db import get_conection

from controllers.user import users
from controllers.cliente import clientes

conn = get_conection()
# <!-- ============================================================== -->
app = Flask(__name__)
app.secret_key = "rokugan"
# <!-- ============================================================== -->
app.register_blueprint(users)
app.register_blueprint(clientes)
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

    # Comprobar si existen solicitudes POST de "cedula" y "contrasena" (formulario enviado por el usuario)
    if request.method == 'POST' and 'cedula' in request.form and 'contrasena' in request.form:
        cedula = request.form['cedula']
        contrasena = request.form['contrasena']

        # Verificar si la cuenta existe usando SQL
        cursor.execute('SELECT * FROM usuario WHERE cedula = %s', (cedula,))
        # Obtener un registro y devolver el resultado
        account = cursor.fetchone()

        if account and account['contrasena'] == contrasena:
            # Crear datos de sesión, podemos acceder a estos datos en otras rutas
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
            # La cuenta no existe o la cédula/contraseña son incorrectas
            flash('Cédula/contraseña incorrectas')

    return render_template('index.html')








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


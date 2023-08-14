from flask import Flask, render_template,session,flash,redirect,request,url_for
import flask
from werkzeug.security import generate_password_hash
import psycopg2
import psycopg2.extras
import re
from database.db import get_conection
conn = get_conection()

# Blueprint - Usuario
users = flask.Blueprint('users', __name__, url_prefix='/')
# Rutas de usuario
@users.route('/NewUser')
def user():
    return render_template('user_register.html')
# Send data to the DB 
@users.route('/addNewUser', methods=['GET', 'POST'])
def addNewUser():
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # Comprueba si existen las peticiones POST "primer_nombre", "contraseña" y "email" (formulario enviado por el usuario)
        if request.method == 'POST' and 'cedula' in request.form and 'password' in request.form:
            # Create variables for easy access
            cedula           = request.form['cedula']
            nombres          = request.form['names']
            apellidos        = request.form['fullNames']
            telefono         = request.form['phone']
            email            = request.form['email']
            contrasena       = request.form['password']
            tipo_usuario     = request.form['role']
            fecha_usuario    = request.form['regDate']
            _hashed_password = generate_password_hash(contrasena)

            # Comprueba si la cuenta existe usando SQL 
            cursor.execute(
                'SELECT * FROM usuario WHERE id = %s', (cedula,))
            account = cursor.fetchone()
            print(account)
            # Si la cuenta existe mostrar error y comprobaciones de validación
            if account:
                flash('La cuenta que usted ingreso ya existe !')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('¡Dirección de correo electrónico no válida!')
            elif not re.match(r'[A-Za-z0-9]+', nombres):
                flash('¡El nombre de usuario debe contener solo caracteres y números!')
            elif not nombres or not email or not contrasena:
                flash('¡Por favor rellena el formulario!')
            else:
                # La cuenta no existe y los datos del formulario son válidos, ahora inserta una nueva cuenta en la tabla de usuarios
                cursor.execute("INSERT INTO usuario (id, nombres, apellidos, telefono, email, contrasena, cargo, fecha_reg) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                               (cedula, nombres, apellidos, telefono, email, _hashed_password, tipo_usuario,
                                fecha_usuario))
                conn.commit()
                flash('¡Usuario registrado correctamente!')
                return render_template('user_register.html')
        elif request.method == 'POST':
            # El formulario está vacío... (sin datos POST)
            flash('¡Por favor rellena el formulario!')
            # Mostrar formulario de registro con mensaje (si corresponde)
            return render_template('user_register.html')
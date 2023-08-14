from flask import Flask, render_template,session,flash,redirect,request,url_for
import flask
from werkzeug.security import generate_password_hash
import psycopg2
import psycopg2.extras
import re
from database.db import get_conection
conn = get_conection()

# Blueprint - Usuario
clientes = flask.Blueprint('clientes', __name__, url_prefix='/')
# Rutas de usuario
# @clientes.route('/cliente')
# def cliente():
#     return render_template('cliente.html')

@clientes.route('/nuevo_cliente')
def nuevo_cliente():
    return render_template('nuevo_cliente.html')
# nuevo cliente
@clientes.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Comprueba si existen las peticiones POST "primer_nombre", "contraseña" y "email" (formulario enviado por el usuario)
        if request.method == 'POST' and 'cedula' in request.form and 'correo' in request.form:
            # Create variables for easy access
            cedula = request.form['cedula']
            nombres = request.form['nombres']
            apellidos = request.form['apellidos']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            email = request.form['correo']

            # Comprueba si la cuenta existe usando SQL
            cursor.execute(
                'SELECT * FROM cliente WHERE id = %s', (cedula,))
            account = cursor.fetchone()
            print(account)
        # Si la cuenta existe mostrar error y comprobaciones de validación
            if account:
                flash('La cuenta que usted ingreso ya existe !')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('¡Dirección de correo electrónico no válida!')
            elif not re.match(r'[A-Za-z0-9]+', nombres):
                flash('¡El nombre de usuario debe contener solo caracteres y números!')

            else:
                # La cuenta no existe y los datos del formulario son válidos, ahora inserta una nueva cuenta en la tabla de usuarios
                cursor.execute("INSERT INTO cliente (id, nombres, apellidos, direccion, telefono, email) VALUES (%s,%s,%s,%s,%s,%s)",
                               (cedula, nombres, apellidos, direccion, telefono, email))
                conn.commit()
                flash('¡Cliente registrado correctamente!')
                return redirect(url_for('clientes.nuevo_cliente'))
        elif request.method == 'POST':
            # El formulario está vacío... (sin datos POST)
            flash('¡Por favor rellena el formulario!')
# En esta pagina se muestra los usuarios de la empresa


@clientes.route('/cliente', methods=['POST', 'GET'])
def cliente():
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Comprobar si el usuario ha iniciado sesión
  
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if request.method == "POST" and 'buscar' in request.form:
            s = "SELECT * FROM cliente where id like '%" + \
                request.form['buscar'] + "%'"
        else:
            s = "SELECT * FROM cliente"
        cur.execute(s)  # Ejecutar la instrucción SQL
        list_users = cur.fetchall()
        return render_template('cliente.html', list_users=list_users)
    # seleccionar cliente
    
@clientes.route('/edit_cliente/<id>', methods=['POST', 'GET'])
def get_cliente(id):

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute('SELECT * FROM cliente WHERE id = %s', (id,))
        data = cur.fetchall()
        cur.close()
        print(data[0])
        return render_template('editar_cliente.html', cliente=data[0])

    # Editar cliente
@clientes.route('/update_cliente/<cedula>', methods=['POST'])
def update_cliente(cedula):

        if request.method == 'POST':
            cedula = request.form['cedula']
            nombres = request.form['nombres']
            apellidos = request.form['apellidos']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            email = request.form['correo']

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
              UPDATE cliente
              SET id           = %s,
                  nombres    = %s,
                  apellidos  = %s,
                  direccion        = %s,
                  telefono         = %s,
                  email            = %s
              WHERE id             = %s
          """, (cedula, nombres, apellidos, direccion, telefono, email, cedula,))
            flash('Cambios guardados con éxito')
            conn.commit()
            return redirect(url_for('clientes.cliente'))


# Eliminar cliente
@clientes.route('/delete_cliente/<string:cedula>', methods=['POST', 'GET'])
def delete_cliente(cedula):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
                DELETE FROM cliente WHERE id = %s
                """, (cedula,))
    conn.commit()
    flash('Cliente Eliminado Correctamente')
    return redirect(url_for('clientes.cliente'))



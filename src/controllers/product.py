from flask import Flask, render_template,session,flash,redirect,request,url_for
import flask
from werkzeug.security import generate_password_hash
import psycopg2
import psycopg2.extras
import re
from database.db import get_conection
conn = get_conection()

# Blueprint - Usuario
product = flask.Blueprint('product', __name__, url_prefix='/')
# Rutas de usuario
@product.route('/NewProduct')
def product():
    return render_template('product_register.html')
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os



app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:thanh2210@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
app.secret_key = "andsfrkasuyrvdsavdcssf"

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Alumnos(db.Model):
    _tablename_='alumnos'
    id = db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    apellidos=db.Column(db.String(50))
    email=db.Column(db.String(50))
    telefono=db.Column(db.String(50))
    created_date=db.Column(db.DateTime,default=datetime.datetime.now)

class Maestros(db.Model):
    _tablename_='maestros'
    matricula = db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    apellidos=db.Column(db.String(50))
    especialidad=db.Column(db.String(50))
    email=db.Column(db.String(50))

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50))
    apaterno = db.Column(db.String(50))
    email = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    cursos = db.relationship(
        'Curso',
        secondary='inscripciones',
        back_populates='alumnos'
    )

class Maestros(db.Model):
    __tablename__ = 'maestros'
    matricula = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    especialidad = db.Column(db.String(50))
    email = db.Column(db.String(50))
    cursos = db.relationship('Curso', back_populates='maestro')

class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(200))
    maestro_matricula = db.Column(db.Integer, db.ForeignKey('maestros.matricula'))
    maestro = db.relationship('Maestros', back_populates='cursos')
    alumnos = db.relationship(
        'Alumnos',
        secondary='inscripciones',
        back_populates='cursos'
    )

class Inscripcion(db.Model):
    __tablename__ = 'inscripciones'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'))
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.datetime.now)
    __table_args__ = (db.UniqueConstraint('alumno_id', 'curso_id', name='unique_inscripcion'),)
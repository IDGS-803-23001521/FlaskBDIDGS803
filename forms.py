from wtforms import Form
from wtforms import StringField, IntegerField, TextAreaField
from wtforms import EmailField, SelectField
from wtforms import validators
from flask_wtf import FlaskForm

class UserForm(FlaskForm): 
    id = IntegerField('ID')
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message='Ingrese nombre valido')
    ])
    apaterno = StringField('Apellido Paterno', [
        validators.DataRequired(message='El campo es requerido'),
    ])
    email = EmailField('Correo', [
        validators.Email(message='Ingrese un correo valido'),
    ])

class UserFormM(FlaskForm): 
    matricula = IntegerField('Matricula')
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=50, message='Ingrese nombre valido')
    ])
    apellidos = StringField('Apellidos', [
        validators.DataRequired(message='El campo es requerido'),
    ])
    especialidad = StringField('Especialidad', [
        validators.DataRequired(message='Ingrese una especialidad valida'),
    ])
    email = EmailField('Correo', [
        validators.Email(message='Ingrese un correo valido'),
    ])

class CursoForm(FlaskForm):
    id = IntegerField('ID')
    nombre = StringField('Nombre del Curso', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=100, message='Ingrese nombre valido')
    ])
    descripcion = TextAreaField('Descripción', [
        validators.DataRequired(message='El campo es requerido'),
    ])
    maestro_matricula = SelectField('Maestro', coerce=int, choices=[])

class InscripcionForm(FlaskForm):
    alumno_id = SelectField('Alumno', coerce=int, choices=[])
    curso_id = SelectField('Curso', coerce=int, choices=[])

class ConsultaForm(FlaskForm):
    id = SelectField('Seleccionar', coerce=int, choices=[])
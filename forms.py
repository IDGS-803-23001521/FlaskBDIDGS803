from wtforms import Form
from wtforms import StringField, IntegerField, PasswordField
from wtforms import EmailField
from wtforms import validators


class UserForm(Form): 
    id=IntegerField('id')
    nombre=StringField('Nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=10,message='Ingrese nombre valido' )
    ])
    apellidos=StringField('Apellidos',[
        validators.DataRequired(message='El campo es requerido'),
    ])
    email=EmailField('Correo',[
        validators.Email(message='Ingrese un correo valido'),
    ])
    telefono=EmailField('Telefono',[
        validators.DataRequired(message='Ingrese un telefono valido'),
    ])

class UserFormM(Form): 
    matricula=IntegerField('Matricula')
    nombre=StringField('Nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=10,message='Ingrese nombre valido' )
    ])
    apellidos=StringField('Apellidos',[
        validators.DataRequired(message='El campo es requerido'),
    ])
    especialidad=EmailField('Especialidad',[
        validators.DataRequired(message='Ingrese un telefono valido'),
    ])
    email=EmailField('Correo',[
        validators.Email(message='Ingrese un correo valido'),
    ])
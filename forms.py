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
    apaterno=StringField('aPaterno',[
        validators.DataRequired(message='El campo es requerido'),
    ])
    email=EmailField('Correo',[
        validators.Email(message='Ingrese un correo valido'),
    ])
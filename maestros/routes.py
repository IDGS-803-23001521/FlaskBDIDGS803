from . import maestros


@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"

#----------------------------------------

from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
from flask import g

import forms

from models import db
from models import Alumnos, Maestros

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
migrate = Migrate(app,db)
csrf=CSRFProtect()

@maestros.route("/grid", methods=['GET', 'POST'])
@maestros.route("/indexM")
def indexM():
	create_form=forms.UserFormM(request.form)
	maestro=Maestros.query.all()
	return render_template("maestros/indexM.html", form=create_form, maestro=maestro)

@maestros.route("/maestros",methods=['POST','GET'])
def maestrosC():
	create_form = forms.UserFormM(request.form)
	if request.method == 'POST':
		maestro = Maestros(
			nombre=create_form.nombre.data,
			apellidos=create_form.apellidos.data,
			especialidad=create_form.especialidad.data,
			email=create_form.email.data,
		)
		db.session.add(maestro)
		db.session.commit()
		return redirect(url_for('maestros.indexM'))
	return render_template("maestros/maestros.html", form=create_form)

@maestros.route("/detallesM",methods=['POST','GET'])
def detallesM():
	create_form = forms.UserFormM(request.form)
	if request.method == 'GET':
		matricula=request.args.get('matricula')
		maes1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		nombre=maes1.nombre
		apellidos=maes1.apellidos
		especialidad=maes1.especialidad
		email=maes1.email
	return render_template("maestros/detallesM.html", nombre=nombre, apellidos=apellidos, especialidad=especialidad, email=email)

@maestros.route("/modificarM", methods=['GET', 'POST'])
def modificarM():
    create_form = forms.UserFormM(request.form)

    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maes1 = Maestros.query.get(matricula)
        create_form.matricula.data = maes1.matricula
        create_form.nombre.data = maes1.nombre
        create_form.apellidos.data = maes1.apellidos
        create_form.especialidad.data = maes1.especialidad
        create_form.email.data = maes1.email
    if request.method == 'POST':
        matricula = request.form.get('matricula')  
        maes1 = Maestros.query.get(matricula)
        maes1.nombre = create_form.nombre.data
        maes1.apellidos = create_form.apellidos.data
        maes1.especialidad = create_form.especialidad.data
        maes1.email = create_form.email.data
        db.session.commit()
        return redirect(url_for('maestros.indexM'))
    return render_template("/maestros/modificarM.html", form=create_form) 

@maestros.route("/eliminarM", methods=['GET', 'POST'])
def eliminarM():
	create_form=forms.UserFormM(request.form)
	if request.method=='GET':
		matricula=request.args.get('matricula')
		maes1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		create_form.matricula.data=request.args.get('matricula')
		create_form.nombre.data=maes1.nombre
		create_form.apellidos.data=maes1.apellidos
		create_form.especialidad.data=maes1.especialidad
		create_form.email.data=maes1.email
	if request.method=='POST':
		matricula=request.args.get('matricula')
		maes1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		create_form.matricula.data=request.args.get('matricula')
		create_form.nombre.data=maes1.nombre
		create_form.apellidos.data=maes1.apellidos
		create_form.especialidad.data=maes1.especialidad
		create_form.email.data=maes1.email
		db.session.delete(maes1)
		db.session.commit()
		return redirect(url_for('maestros.indexM'))
	return render_template("maestros/eliminarM.html", form=create_form)

@maestros.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404

if __name__ == '__main__':
	csrf.init_app(app)
	
	with app.app_context():
		db.create_all()
	app.run(debug=True)


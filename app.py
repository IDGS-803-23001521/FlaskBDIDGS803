from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g

import forms

from models import db
from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@app.route("/", methods=['GET', 'POST'])
@app.route("/index")
def index():
	create_form=forms.UserForm(request.form)
	alumno=Alumnos.query.all()
	return render_template("index.html", form=create_form, alumno=alumno)

@app.route("/alumnos",methods=['POST','GET'])
def alumnos():
	create_form = forms.UserForm(request.form)
	if request.method == 'POST':
		alumno = Alumnos(
			nombre=create_form.nombre.data,
			apaterno=create_form.apaterno.data,
			email=create_form.email.data,
		)
		db.session.add(alumno)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template("alumnos.html", form=create_form)

@app.route("/detalles",methods=['POST','GET'])
def detalles():
	create_form = forms.UserForm(request.form)
	if request.method == 'GET':
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		nombre=alum1.nombre
		apaterno=alum1.apaterno
		email=alum1.email
	return render_template("detalles.html", nombre=nombre, apaterno=apaterno, email=email)

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404

if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)
	with app.app_context():
		db.create_all()
	app.run(debug=True)


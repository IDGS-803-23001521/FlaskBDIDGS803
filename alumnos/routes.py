from . import alumnos
from flask import render_template, request, redirect, url_for, flash
from models import db, Alumnos, Curso, Inscripcion
import forms

@alumnos.route("/")
def indexA():
    create_form = forms.UserForm()
    alumno = Alumnos.query.all()
    return render_template("alumnos/indexA.html", form=create_form, alumno=alumno)

@alumnos.route("/alumnos", methods=['POST', 'GET'])
def alumnosC():
    create_form = forms.UserForm()
    if request.method == 'POST' and create_form.validate():
        alumno = Alumnos(
            nombre=create_form.nombre.data,
            apaterno=create_form.apaterno.data,
            email=create_form.email.data,
        )
        db.session.add(alumno)
        db.session.commit()
        flash('Alumno agregado correctamente')
        return redirect(url_for('alumnos.indexA'))
    return render_template("alumnos/alumnos.html", form=create_form)

@alumnos.route("/detallesA", methods=['GET'])
def detallesA():
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        cursos = alum1.cursos if alum1 else []
        return render_template("alumnos/detallesA.html", 
                               nombre=alum1.nombre, 
                               apaterno=alum1.apaterno, 
                               email=alum1.email,
                               cursos=cursos)

@alumnos.route("/modificarA", methods=['GET', 'POST'])
def modificarA():
    create_form = forms.UserForm()
    
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = Alumnos.query.get(id)
        if alum1:
            create_form.id.data = alum1.id
            create_form.nombre.data = alum1.nombre
            create_form.apaterno.data = alum1.apaterno
            create_form.email.data = alum1.email
    
    if request.method == 'POST' and create_form.validate():
        id = request.form.get('id')
        alum1 = Alumnos.query.get(id)
        if alum1:
            alum1.nombre = create_form.nombre.data
            alum1.apaterno = create_form.apaterno.data
            alum1.email = create_form.email.data
            db.session.commit()
            flash('Alumno modificado correctamente')
            return redirect(url_for('alumnos.indexA'))
    
    return render_template("alumnos/modificarA.html", form=create_form)

@alumnos.route("/eliminarA", methods=['GET', 'POST'])
def eliminarA():
    create_form = forms.UserForm()
    
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alum1:
            create_form.id.data = alum1.id
            create_form.nombre.data = alum1.nombre
            create_form.apaterno.data = alum1.apaterno
            create_form.email.data = alum1.email
    
    if request.method == 'POST':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alum1:
            Inscripcion.query.filter_by(alumno_id=id).delete()
            db.session.delete(alum1)
            db.session.commit()
            flash('Alumno eliminado correctamente')
        return redirect(url_for('alumnos.indexA'))
    
    return render_template("alumnos/eliminarA.html", form=create_form)
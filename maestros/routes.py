from . import maestros
from flask import render_template, request, redirect, url_for, flash
from models import db, Maestros, Curso
import forms

@maestros.route("/")
def indexM():
    create_form = forms.UserFormM()
    maestro = Maestros.query.all()
    return render_template("maestros/indexM.html", form=create_form, maestro=maestro)

@maestros.route("/maestros", methods=['POST', 'GET'])
def maestrosC():
    create_form = forms.UserFormM()
    if request.method == 'POST' and create_form.validate():
        maestro = Maestros(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            especialidad=create_form.especialidad.data,
            email=create_form.email.data,
        )
        db.session.add(maestro)
        db.session.commit()
        flash('Maestro agregado correctamente')
        return redirect(url_for('maestros.indexM'))
    return render_template("maestros/maestros.html", form=create_form)

@maestros.route("/detallesM", methods=['GET'])
def detallesM():
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        cursos = Curso.query.filter_by(maestro_matricula=matricula).all() if maes1 else []
        return render_template("maestros/detallesM.html", 
                               nombre=maes1.nombre, 
                               apellidos=maes1.apellidos, 
                               especialidad=maes1.especialidad, 
                               email=maes1.email,
                               cursos=cursos)

@maestros.route("/modificarM", methods=['GET', 'POST'])
def modificarM():
    create_form = forms.UserFormM()
    
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maes1 = Maestros.query.get(matricula)
        if maes1:
            create_form.matricula.data = maes1.matricula
            create_form.nombre.data = maes1.nombre
            create_form.apellidos.data = maes1.apellidos
            create_form.especialidad.data = maes1.especialidad
            create_form.email.data = maes1.email
    
    if request.method == 'POST' and create_form.validate():
        matricula = request.form.get('matricula')
        maes1 = Maestros.query.get(matricula)
        if maes1:
            maes1.nombre = create_form.nombre.data
            maes1.apellidos = create_form.apellidos.data
            maes1.especialidad = create_form.especialidad.data
            maes1.email = create_form.email.data
            db.session.commit()
            flash('Maestro modificado correctamente')
            return redirect(url_for('maestros.indexM'))
    
    return render_template("maestros/modificarM.html", form=create_form)

@maestros.route("/eliminarM", methods=['GET', 'POST'])
def eliminarM():
    create_form = forms.UserFormM()
    
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if maes1:
            create_form.matricula.data = maes1.matricula
            create_form.nombre.data = maes1.nombre
            create_form.apellidos.data = maes1.apellidos
            create_form.especialidad.data = maes1.especialidad
            create_form.email.data = maes1.email
    
    if request.method == 'POST':
        matricula = request.args.get('matricula')
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if maes1:
            cursos = Curso.query.filter_by(maestro_matricula=matricula).all()
            for curso in cursos:
                curso.maestro_matricula = None
            db.session.delete(maes1)
            db.session.commit()
            flash('Maestro eliminado correctamente')
        return redirect(url_for('maestros.indexM'))
    
    return render_template("maestros/eliminarM.html", form=create_form)

@maestros.route("/cursos_por_maestro", methods=['GET', 'POST'])
def cursos_por_maestro():
    create_form = forms.ConsultaForm()
    maestros = Maestros.query.all()
    create_form.id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros]
    
    cursos_lista = []
    maestro_seleccionado = None
    
    if request.method == 'POST' and create_form.validate():
        matricula = create_form.id.data
        maestro_seleccionado = Maestros.query.get(matricula)
        if maestro_seleccionado:
            cursos_lista = Curso.query.filter_by(maestro_matricula=matricula).all()
    
    return render_template("maestros/cursos_por_maestro.html", 
                          form=create_form,
                          maestros=maestros,
                          cursos=cursos_lista,
                          maestro=maestro_seleccionado)

@maestros.route("/alumnos_por_maestro", methods=['GET', 'POST'])
def alumnos_por_maestro():
    create_form = forms.ConsultaForm()
    maestros = Maestros.query.all()
    create_form.id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros]
    
    alumnos_lista = []
    maestro_seleccionado = None
    
    if request.method == 'POST' and create_form.validate():
        matricula = create_form.id.data
        maestro_seleccionado = Maestros.query.get(matricula)
        if maestro_seleccionado:
            cursos = Curso.query.filter_by(maestro_matricula=matricula).all()
            alumnos_set = set()
            for curso in cursos:
                for alumno in curso.alumnos:
                    alumnos_set.add(alumno)
            alumnos_lista = list(alumnos_set)
    
    return render_template("maestros/alumnos_por_maestro.html", 
                          form=create_form,
                          maestros=maestros,
                          alumnos=alumnos_lista,
                          maestro=maestro_seleccionado)
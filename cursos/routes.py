from . import cursos
from flask import render_template, request, redirect, url_for, flash
from models import db, Curso, Maestros, Alumnos, Inscripcion
import forms

@cursos.route("/")
def indexC():
    create_form = forms.CursoForm()
    cursos = Curso.query.all()
    return render_template("cursos/indexC.html", form=create_form, cursos=cursos)

@cursos.route("/cursos", methods=['POST', 'GET'])
def cursosC():
    create_form = forms.CursoForm()
    
    maestros = Maestros.query.all()
    create_form.maestro_matricula.choices = [(0, '-- Seleccione un maestro --')] + [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros]
    
    if request.method == 'POST' and create_form.validate():
        curso = Curso(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_matricula=create_form.maestro_matricula.data if create_form.maestro_matricula.data != 0 else None,
        )
        db.session.add(curso)
        db.session.commit()
        flash('Curso agregado correctamente')
        return redirect(url_for('cursos.indexC'))
    
    return render_template("cursos/cursos.html", form=create_form)

@cursos.route("/detallesC", methods=['GET'])
def detallesC():
    if request.method == 'GET':
        id = request.args.get('id')
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        maestro = Maestros.query.get(curso.maestro_matricula) if curso and curso.maestro_matricula else None
        nombre_maestro = f"{maestro.nombre} {maestro.apellidos}" if maestro else "Sin asignar"
        
        alumnos = curso.alumnos if curso else []
        
        return render_template("cursos/detallesC.html", 
                               nombre=curso.nombre,
                               descripcion=curso.descripcion,
                               maestro=nombre_maestro,
                               alumnos=alumnos)

@cursos.route("/modificarC", methods=['GET', 'POST'])
def modificarC():
    create_form = forms.CursoForm()
    
    maestros = Maestros.query.all()
    create_form.maestro_matricula.choices = [(0, '-- Seleccione un maestro --')] + [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros]
    
    if request.method == 'GET':
        id = request.args.get('id')
        curso = Curso.query.get(id)
        if curso:
            create_form.id.data = curso.id
            create_form.nombre.data = curso.nombre
            create_form.descripcion.data = curso.descripcion
            create_form.maestro_matricula.data = curso.maestro_matricula if curso.maestro_matricula else 0
    
    if request.method == 'POST' and create_form.validate():
        id = request.form.get('id')
        curso = Curso.query.get(id)
        if curso:
            curso.nombre = create_form.nombre.data
            curso.descripcion = create_form.descripcion.data
            curso.maestro_matricula = create_form.maestro_matricula.data if create_form.maestro_matricula.data != 0 else None
            db.session.commit()
            flash('Curso modificado correctamente')
            return redirect(url_for('cursos.indexC'))
    
    return render_template("cursos/modificarC.html", form=create_form)

@cursos.route("/eliminarC", methods=['GET', 'POST'])
def eliminarC():
    create_form = forms.CursoForm()
    
    if request.method == 'GET':
        id = request.args.get('id')
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        if curso:
            create_form.id.data = curso.id
            create_form.nombre.data = curso.nombre
            create_form.descripcion.data = curso.descripcion
    
    if request.method == 'POST':
        id = request.args.get('id')
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        if curso:
            Inscripcion.query.filter_by(curso_id=id).delete()
            db.session.delete(curso)
            db.session.commit()
            flash('Curso eliminado correctamente')
        return redirect(url_for('cursos.indexC'))
    
    return render_template("cursos/eliminarC.html", form=create_form)

@cursos.route("/inscripcion", methods=['GET', 'POST'])
def inscripcion():
    create_form = forms.InscripcionForm()
    
    alumnos = Alumnos.query.all()
    create_form.alumno_id.choices = [(0, '-- Seleccione un alumno --')] + [(a.id, f"{a.nombre} {a.apaterno}") for a in alumnos]
    
    cursos_disponibles = Curso.query.all()
    create_form.curso_id.choices = [(0, '-- Seleccione un curso --')] + [(c.id, c.nombre) for c in cursos_disponibles]
    
    if request.method == 'POST' and create_form.validate():
        alumno_id = create_form.alumno_id.data
        curso_id = create_form.curso_id.data
        
        if alumno_id == 0 or curso_id == 0:
            flash('Debe seleccionar un alumno y un curso')
            return redirect(url_for('cursos.inscripcion'))
        
        existe = Inscripcion.query.filter_by(
            alumno_id=alumno_id,
            curso_id=curso_id
        ).first()
        
        if existe:
            flash('El alumno ya está inscrito en este curso')
        else:
            inscripcion = Inscripcion(
                alumno_id=alumno_id,
                curso_id=curso_id
            )
            db.session.add(inscripcion)
            db.session.commit()
            flash('Inscripción realizada correctamente')
        
        return redirect(url_for('cursos.inscripcion'))
    
    return render_template("cursos/inscripcion.html", form=create_form)

@cursos.route("/alumnos_por_curso", methods=['GET', 'POST'])
def alumnos_por_curso():
    create_form = forms.ConsultaForm()
    cursos = Curso.query.all()
    create_form.id.choices = [(0, '-- Seleccione un curso --')] + [(c.id, c.nombre) for c in cursos]
    
    alumnos_lista = []
    curso_seleccionado = None
    
    if request.method == 'POST' and create_form.validate():
        curso_id = create_form.id.data
        if curso_id != 0:
            curso_seleccionado = Curso.query.get(curso_id)
            if curso_seleccionado:
                alumnos_lista = curso_seleccionado.alumnos
    
    return render_template("cursos/alumnos_por_curso.html", 
                          form=create_form,
                          cursos=cursos,
                          alumnos=alumnos_lista,
                          curso=curso_seleccionado)

@cursos.route("/cursos_por_alumno", methods=['GET', 'POST'])
def cursos_por_alumno():
    create_form = forms.ConsultaForm()
    alumnos = Alumnos.query.all()
    create_form.id.choices = [(0, '-- Seleccione un alumno --')] + [(a.id, f"{a.nombre} {a.apaterno}") for a in alumnos]
    
    cursos_lista = []
    alumno_seleccionado = None
    
    if request.method == 'POST' and create_form.validate():
        alumno_id = create_form.id.data
        if alumno_id != 0:
            alumno_seleccionado = Alumnos.query.get(alumno_id)
            if alumno_seleccionado:
                cursos_lista = alumno_seleccionado.cursos
    
    return render_template("cursos/cursos_por_alumno.html", 
                          form=create_form,
                          alumnos=alumnos,
                          cursos=cursos_lista,
                          alumno=alumno_seleccionado)
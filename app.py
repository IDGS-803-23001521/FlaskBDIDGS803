from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate

from maestros.routes import maestros
from alumnos.routes import alumnos
from cursos.routes import cursos

from models import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(maestros, url_prefix='/maestros')
app.register_blueprint(alumnos, url_prefix='/alumnos')
app.register_blueprint(cursos, url_prefix='/cursos')

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect()

@app.route("/")
def inicio():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
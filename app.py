import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ===============================
# MODELO PERFUME
# ===============================
class Perfume(db.Model):
    __tablename__ = 'perfumes'

    id_perfume = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50))
    genero = db.Column(db.String(20))
    volumen_ml = db.Column(db.Integer)
    precio = db.Column(db.Numeric(10,2), nullable=False)

    def to_dict(self):
        return {
            'id_perfume': self.id_perfume,
            'nombre': self.nombre,
            'marca': self.marca,
            'tipo': self.tipo,
            'genero': self.genero,
            'volumen_ml': self.volumen_ml,
            'precio': float(self.precio)
        }

# ===============================
# RUTA PRINCIPAL (LISTAR)
# ===============================
@app.route('/')
def index():
    perfumes = Perfume.query.all()
    return render_template('index.html', perfumes=perfumes)

# ===============================
# CREAR PERFUME
# ===============================
@app.route('/perfumes/new', methods=['GET','POST'])
def create_perfume():
    if request.method == 'POST':
        nuevo_perfume = Perfume(
            nombre=request.form['nombre'],
            marca=request.form['marca'],
            tipo=request.form['tipo'],
            genero=request.form['genero'],
            volumen_ml=request.form['volumen_ml'],
            precio=request.form['precio']
        )

        db.session.add(nuevo_perfume)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create_perfume.html')

# ===============================
# ELIMINAR PERFUME
# ===============================
@app.route('/perfumes/delete/<int:id_perfume>')
def delete_perfume(id_perfume):
    perfume = Perfume.query.get(id_perfume)
    if perfume:
        db.session.delete(perfume)
        db.session.commit()
    return redirect(url_for('index'))

# ===============================
# ACTUALIZAR PERFUME
# ===============================
@app.route('/perfumes/update/<int:id_perfume>', methods=['GET','POST'])
def update_perfume(id_perfume):
    perfume = Perfume.query.get(id_perfume)

    if request.method == 'POST':
        perfume.nombre = request.form['nombre']
        perfume.marca = request.form['marca']
        perfume.tipo = request.form['tipo']
        perfume.genero = request.form['genero']
        perfume.volumen_ml = request.form['volumen_ml']
        perfume.precio = request.form['precio']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_perfume.html', perfume=perfume)

# ===============================
# RUN
# ===============================
if __name__ == '__main__':
    app.run(debug=True)
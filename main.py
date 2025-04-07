from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(100), nullable=False)
    vacina = db.Column(db.String(100), nullable=False)
    data_vacinacao = db.Column(db.Date, nullable=False)
    proxima_dose = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    hoje = datetime.now().date()
    filtro = request.args.get('filtro')
    pets = Pet.query.all()

    for pet in pets:
        pet.atrasado = pet.proxima_dose <= hoje

    if filtro:
        pets = [p for p in pets if p.atrasado]

    return render_template('index.html', pets=pets)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    especie = request.form['especie']
    vacina = request.form['vacina']
    data_vacinacao = datetime.strptime(request.form['data_vacinacao'], '%Y-%m-%d').date()
    proxima_dose = datetime.strptime(request.form['proxima_dose'], '%Y-%m-%d').date()
    novo_pet = Pet(
        nome=nome,
        especie=especie,
        vacina=vacina,
        data_vacinacao=data_vacinacao,
        proxima_dose=proxima_dose
    )
    db.session.add(novo_pet)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    pet = Pet.query.get_or_404(id)
    db.session.delete(pet)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

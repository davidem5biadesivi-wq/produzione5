
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    macchina = db.Column(db.String(50), nullable=True)

class Lavorazione(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    macchina = db.Column(db.String(50))
    descrizione = db.Column(db.String(200))
    data_richiesta = db.Column(db.String(50))
    operatore_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cliente = db.Column(db.String(100))
    ordine = db.Column(db.String(100))
    codice_articolo = db.Column(db.String(100))
    data_consegna = db.Column(db.String(50))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        user = User.query.filter_by(username=username, password=password, role=role).first()
        if user:
            session['user_id'] = user.id
            session['role'] = user.role
            if role == 'operatore':
                return redirect(url_for('dashboard_operatore'))
            else:
                return redirect(url_for('dashboard_ufficio'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        macchina = request.form['macchina']
        user = User(username=username, password=password, role='operatore', macchina=macchina)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard_operatore')
def dashboard_operatore():
    user_id = session.get('user_id')
    lavorazioni = Lavorazione.query.filter_by(operatore_id=user_id).all()
    return render_template('dashboard_operatore.html', lavorazioni=lavorazioni)

@app.route('/dashboard_ufficio')
def dashboard_ufficio():
    macchina = request.args.get('macchina')
    if macchina:
        lavorazioni = Lavorazione.query.filter_by(macchina=macchina).all()
    else:
        lavorazioni = Lavorazione.query.all()
    return render_template('dashboard_ufficio.html', lavorazioni=lavorazioni)

@app.route('/richiedi_data/<int:id>', methods=['POST'])
def richiedi_data(id):
    lavorazione = Lavorazione.query.get(id)
    lavorazione.data_richiesta = request.form['data_richiesta']
    db.session.commit()
    return redirect(url_for('dashboard_ufficio'))

@app.route('/modifica_lavorazione/<int:id>', methods=['POST'])
def modifica_lavorazione(id):
    lavorazione = Lavorazione.query.get(id)
    lavorazione.cliente = request.form['cliente']
    lavorazione.ordine = request.form['ordine']
    lavorazione.codice_articolo = request.form['codice_articolo']
    lavorazione.data_consegna = request.form['data_consegna']
    db.session.commit()
    return redirect(url_for('dashboard_operatore'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

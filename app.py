from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

class Kunder(db.Model):
    __tablename__ = 'kunder'
    kunde_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fornavn = db.Column(db.String(50), nullable=False)
    efternavn = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Kunder {self.fornavn} {self.efternavn}>'

class Abonnementer(db.Model):
    _tablename_='abonnementer'
    abonnementer_id = db.Column(db.integer, primary_key=True, autoincrement=True)
    kunde_id = db.Column(db.Integer,db.ForeignKey('kunder.kunde_id'),nullable=False)
    bil_id = db.Column(db.integer,db.ForeignKey('biler.bil_id'),nullable=False)
    startDato = db.column(db.date, nullable=False)
    slutDate = db.column(db.date, nullable=False)
    prisPrMaaned = db.column(db.float, nullable =False)

    def __repr__(self):
        return f'<Leases KundeID: {self.kunde_id}, BilID: {self.bil_id}>'
    
class Biler(db.Model):
    _tablename_='biler'
    bil_id = db.Column(db.integer,primary_key=True,nullable=False)
    maerke = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    braendstoftype = db.Column(db.String(50), nullable=False)
    hestekraefter = db.Column(db.Integer, nullable=False)
    stelnummer = db.Column(db.String(50), nullable=False)
    vognnummer = db.Column(db.String(50), nullable=False)
    odometer = db.Column(db.Integer, nullable=False)
    produktionsaar = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Bil: model: {self.model}, brændstof: {self.braendstoftype}, mærke: {self.maerke}, BilID: {self.bil_id}>'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/greet', methods=['POST'])
def greet():
    fornavn = request.form['fornavn']
    efternavn = request.form['efternavn']
    adresse = request.form['adresse']
    email = request.form['email']
    telefon = request.form['telefon']
    
    new_user = Kunder(fornavn=fornavn, efternavn=efternavn, adresse=adresse, email=email, telefon=telefon)
    db.session.add(new_user)
    db.session.commit()
    
    return render_template('greet.html', fornavn=fornavn, efternavn=efternavn)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
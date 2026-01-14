from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Groupe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    etudiants = db.relationship('Etudiant', backref='groupe', lazy=True)

class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200), nullable=True)
    pin = db.Column(db.String(50), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groupe.id'))
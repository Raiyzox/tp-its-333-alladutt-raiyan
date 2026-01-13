from flask_sqlalchemy import SQLAlchemy

# On prépare la base de données
db = SQLAlchemy()

class Groupe(db.Model):
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    
    # Relation : Un groupe contient plusieurs étudiants
    etudiants = db.relationship('Etudiant', backref='groupe', lazy=True)

    def __repr__(self):
        return f"<Groupe {self.nom}>"

class Etudiant(db.Model):
    __tablename__ = "etudiant"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String(200), nullable=True)  # Ajouté pour ton TP
    pin = db.Column(db.String(50), nullable=True)      # Ajouté pour ton TP
    
    # Clé étrangère qui relie l'étudiant à un groupe
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    def __repr__(self):
        return f"<Etudiant {self.nom}>"
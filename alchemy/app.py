from flask import Flask, render_template, request, redirect
from models import db, Groupe, Etudiant
import os

app = Flask(__name__)

# Configuration de la base de données (fichier alchimie.db)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'alchimie.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Lier la BDD à l'app
db.init_app(app)

# --- INITIALISATION AU DÉMARRAGE ---
with app.app_context():
    db.create_all() # Crée les tables vides

    # Exercice Slide 17 : Créer le groupe ITS2 s'il n'existe pas
    if not Groupe.query.filter_by(nom="ITS2").first():
        its2 = Groupe(nom="ITS2")
        db.session.add(its2)
        db.session.commit()
        print("✅ Groupe ITS2 créé !")

        # Ajout de quelques étudiants de test
        e1 = Etudiant(nom="Alice", adresse="Paris", pin="111", groupe=its2)
        e2 = Etudiant(nom="Bob", adresse="Lyon", pin="222", groupe=its2)
        db.session.add_all([e1, e2])
        db.session.commit()
        print("✅ Étudiants de démo ajoutés !")

# --- ROUTES ---

@app.route('/')
def home():
    # ORM : On récupère tous les étudiants (SELECT * FROM etudiant)
    liste = Etudiant.query.all()
    return render_template("base.html", etudiants=liste)

@app.route('/new', methods=['GET', 'POST'])
def new_student():
    if request.method == 'GET':
        return render_template("index.html")
    
    if request.method == 'POST':
        # 1. Récupération du formulaire
        nom_recu = request.form['name']
        addr_recu = request.form['addr']
        pin_recu = request.form['pincode']
        
        # 2. On récupère le groupe "ITS2" pour y mettre l'étudiant
        groupe_defaut = Groupe.query.filter_by(nom="ITS2").first()

        # 3. Création de l'objet (ORM)
        nouveau = Etudiant(nom=nom_recu, adresse=addr_recu, pin=pin_recu, groupe=groupe_defaut)

        # 4. Sauvegarde
        db.session.add(nouveau)
        db.session.commit()
        
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
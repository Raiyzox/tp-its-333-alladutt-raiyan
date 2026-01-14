from flask import Blueprint, request, jsonify
from .models import db, Groupe, Etudiant
import jwt
import datetime
from functools import wraps

# On crée un "Blueprint" (un morceau d'application)
views = Blueprint('views', __name__)

SECRET_KEY = "raiyan_secret_boss_2026"

# --- DÉCORATEUR POUR SÉCURISER LES ROUTES ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token manquant !'}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token invalide !'}), 401
        return f(*args, **kwargs)
    return decorated

# --- ROUTE LOGIN ---
@views.route('/login', methods=['POST'])
def login():
    data = request.json
    # Tes identifiants : raiyan / boss
    if data and data.get('username') == "raiyan" and data.get('password') == "boss":
        token = jwt.encode({
            'user': data['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({'message': 'Login raté'}), 401

# --- ROUTES ETUDIANTS ---
@views.route('/etudiants', methods=['GET'])
def get_etudiants():
    groupe = Groupe.query.filter_by(nom="Groupe_Raiyan").first()
    if not groupe:
        return jsonify({"message": "Groupe introuvable"}), 404
        
    liste = [{
        "id": e.id, 
        "nom": e.nom, 
        "adresse": e.adresse,
        "pin": e.pin
    } for e in groupe.etudiants]
    
    return jsonify({"groupe": groupe.nom, "etudiants": liste})

@views.route('/new', methods=['POST'])
@token_required # Sécurisé !
def add_etudiant():
    data = request.json
    groupe = Groupe.query.filter_by(nom="Groupe_Raiyan").first()
    
    nouveau = Etudiant(
        nom=data.get('nom'),
        adresse=data.get('adresse'),
        pin=data.get('pin'),
        groupe=groupe
    )
    db.session.add(nouveau)
    db.session.commit()
    return jsonify({"message": f"Étudiant {nouveau.nom} ajouté !"})
from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
# 1. Imports pour le JWT
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# 2. Configuration du JWT
app.config["JWT_SECRET_KEY"] = "super-secret-key-change-me"  # Clé de cryptage
jwt = JWTManager(app)

# ... (Tes routes home, new, list, edit restent ici, inchangées) ...

# --- 3. NOUVELLE ROUTE : Authentification (Login) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Affichage du formulaire de connexion
    if request.method == 'GET':
        return render_template('login.html')

    # Traitement de la connexion
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        
        # On vérifie si l'admin existe dans la BDD
        cur.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, password))
        admin = cur.fetchone()
        con.close()
        
        if admin:
            # Si c'est bon, on crée le jeton (Token)
            access_token = create_access_token(identity=username)
            # On l'affiche en JSON (C'est le standard pour les API)
            return jsonify(access_token=access_token), 200
        else:
            return "Mauvais login ou mot de passe", 401

# Exemple de route protégée (Seul l'admin avec un token peut supprimer)
@app.route('/protected-delete/<int:id>', methods=['DELETE'])
@jwt_required() # <--- Cette ligne protège la route !
def protected_delete(id):
    # Ici, le code de suppression ne s'exécutera que si le token est valide
    current_user = get_jwt_identity()
    return jsonify(msg=f"Utilisateur supprimé par l'admin {current_user}"), 200

if __name__ == '__main__':
    app.run(debug=True)
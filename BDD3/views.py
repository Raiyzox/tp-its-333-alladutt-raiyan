from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
import jwt # C'est la librairie manuelle

app = Flask(__name__)

# Une clé secrète pour signer le token (comme une signature numérique)
SECRET_KEY = "ITS_SECRET_2026"

@app.route('/')
def home():
    # On redirige vers le login direct
    return redirect('/login')

# ---------- LOGIN (Génère le Token) ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    # Récupération du form
    user = request.form['username']
    pwd = request.form['password']

    # Vérification simple (admin / admin)
    if user == "admin" and pwd == "admin":
        # CRÉATION MANUELLE DU TOKEN
        token = jwt.encode({
            "user": user,
            # Le token expire dans 30 minutes
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, SECRET_KEY, algorithm="HS256")

        # On affiche le token à l'utilisateur
        return render_template("token.html", token=token)

    return "Accès refusé : Mauvais mot de passe"


# ---------- AJOUT ETUDIANT (Pas protégé pour l'exercice) ----------
@app.route('/new', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
         return render_template("new.html")
         
    nom = request.form['nom']
    adresse = request.form['addr'] # Attention: dans ton html c'est 'addr' pas 'adresse'
    pin = request.form['pin']

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO etudiants (nom, addr, pin) VALUES (?,?,?)", (nom, adresse, pin))
    conn.commit()
    conn.close()
    
    # Une fois ajouté, on retourne voir la liste (mais il faudra le token !)
    return "Étudiant ajouté ! <a href='/login'>Retour au login pour avoir un token</a>"

# ---------- LISTE PROTÉGÉE (Vérifie le Token) ----------
@app.route('/list')
def list_students():
    # 1. On cherche le token dans l'URL (ex: /list?token=MON_TOKEN)
    token = request.args.get("token")

    # 2. Si pas de token, on bloque
    if not token:
        return "⛔ ERREUR : Token requis ! Connectez-vous d'abord."

    try:
        # 3. On essaie de décoder le token avec la clé secrète
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # Si ça marche, le code continue...
    except:
        # Si le token est faux ou expiré, ça plante ici
        return "⛔ ERREUR : Token invalide ou expiré."

    # 4. Si on arrive là, c'est que le token est bon ! On affiche la liste.
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT rowid, * FROM etudiants")
    rows = cur.fetchall()
    conn.close()

    # On renvoie le token à la page pour qu'elle puisse construire des liens valides
    return render_template("list.html", rows=rows, token=token)

if __name__ == '__main__':
    app.run(debug=True)
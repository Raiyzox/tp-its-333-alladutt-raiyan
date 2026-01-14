from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('new.html')

@app.route('/new', methods=['POST'])
def add_student():
    # ... (Garde ton code existant ici pour l'ajout) ...
    # Je te remets le code court pour rappel :
    if request.method == 'POST':
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO etudiants (nom,addr,pin) VALUES (?,?,?)", 
                           (request.form['nom'], request.form['addr'], request.form['pin']))
                con.commit()
        except:
            con.rollback()
    return redirect(url_for('list_students')) # Une fois ajouté, on va direct à la liste

# --- NOUVELLE PARTIE POUR AFFICHER (READ) ---
@app.route('/list')
def list_students():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row # Important pour utiliser les noms des colonnes
    cur = con.cursor()
    
    # On récupère aussi le 'rowid' pour pouvoir identifier chaque étudiant
    cur.execute("SELECT rowid, * FROM etudiants")
    rows = cur.fetchall()
    con.close()
    return render_template("list.html", rows=rows)

# --- NOUVELLE PARTIE POUR MODIFIER (UPDATE) ---
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    if request.method == 'POST':
        # Si on a cliqué sur "Sauvegarder", on fait la mise à jour SQL
        nom = request.form['nom']
        addr = request.form['addr']
        pin = request.form['pin']
        
        # Commande SQL UPDATE (Slide 9 implique modification)
        cur.execute("UPDATE etudiants SET nom=?, addr=?, pin=? WHERE rowid=?", (nom, addr, pin, id))
        con.commit()
        con.close()
        return redirect(url_for('list_students')) # Retour à la liste
    
    else:
        # Si on arrive juste sur la page, on récupère les infos actuelles de l'étudiant
        cur.execute("SELECT rowid, * FROM etudiants WHERE rowid=?", (id,))
        row = cur.fetchone()
        con.close()
        return render_template("edit.html", row=row)
# --- NOUVELLE PARTIE POUR SUPPRIMER (DELETE) ---
@app.route('/delete/<int:id>')
def delete_student(id):
    try:
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        
        # Commande SQL pour supprimer la ligne correspondant à l'ID (rowid)
        cur.execute("DELETE FROM etudiants WHERE rowid = ?", (id,))
        
        con.commit()
        msg = "Supprimé avec succès"
    except:
        con.rollback()
        msg = "Erreur lors de la suppression"
    finally:
        con.close()
        # On retourne sur la page de la liste pour voir le résultat
        return redirect(url_for('list_students'))
if __name__ == '__main__':
    app.run(debug=True)
from app import app
from flask import render_template, request, jsonify

### EXO1 - simple API
@app.route('/api/hello', methods=['GET'])
def hello_api():
    return jsonify({"message": "Hello from MVC API!"})

### EXO2 - API with simple display
@app.route('/simple-html')
def simple_display():
    return "<h1>Ceci est une vue HTML simple</h1><p>Générée depuis Flask views.py par RAIYANDOOOO</p>"
    # return render_template("index.html")


### EXO3 - API with parameters display 
@app.route('/bonjour/<name>')
def bonjour_perso(name):
    return f"<h1>Bonjour {name} !</h1><p>Ce paramètre vient de la route URL.</p>"
### EXO4 - API with parameters retrieved from URL 
@app.route('/recherche')
def recherche_url():
    # 1. On récupère la valeur du paramètre 'term' dans l'URL
    # Si l'utilisateur n'en met pas, on utilise 'Inconnu'
    terme_recupere = request.args.get('term', 'Inconnu')
    
    # 2. On renvoie le template HTML en lui passant la variable
    # Dans le HTML, on l'appellera "le_terme"
    return render_template('search.html', le_terme=terme_recupere)
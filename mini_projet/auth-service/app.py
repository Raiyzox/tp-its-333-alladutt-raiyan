from flask import Flask, request, jsonify
import jwt
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Pour que le HTML puisse l'appeler

# Clé secrète pour signer les badges (Tokens)
SECRET_KEY = "super_secret_key_microservices"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    
    # Vérification simple (admin / admin)
    if data and data.get('username') == "admin" and data.get('password') == "admin":
        
        # Création du token
        token = jwt.encode({
            'user': 'admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, SECRET_KEY, algorithm="HS256")
        
        return jsonify({'token': token})
    
    return jsonify({'message': 'Mauvais login/mot de passe !'}), 401

if __name__ == '__main__':
    # Port 5003 pour ce service
    app.run(host='0.0.0.0', port=5003, debug=True)
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from .models import db, Groupe, Etudiant
from .views import views

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///raiyan_school.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Configuration Swagger
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Enregistrement des routes (views)
    app.register_blueprint(views, url_prefix='/')

    # CRÉATION DE LA BDD ET DES DONNÉES
    with app.app_context():
        db.create_all()
        
        # On crée tes données si elles n'existent pas
        if not Groupe.query.filter_by(nom="Groupe_Raiyan").first():
            mon_groupe = Groupe(nom="Groupe_Raiyan")
            db.session.add(mon_groupe)
            
            # Tes étudiants persos
            e1 = Etudiant(nom="Raiyan ALLADUTT", adresse="Creteil", pin="94000", groupe=mon_groupe)
            e2 = Etudiant(nom="Thibault Bernard", adresse="Saint Maur", pin="94100", groupe=mon_groupe)
            
            db.session.add_all([e1, e2])
            db.session.commit()
            print("✅ Base de données initialisée pour Raiyan !")

    return app
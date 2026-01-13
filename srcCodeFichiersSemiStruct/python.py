import json


chemin = "BDD101/data.json"

try:
    # --- ÉTAPE 1 : LIRE LES VALEURS ---
    with open(chemin, 'r') as f:
        data = json.load(f)
    
    print("Lecture réussie !")
    print("Anciennes coordonnées :", data['features'][0]['geometry']['coordinates'])

    # --- ÉTAPE 2 : MISE À JOUR DE COORDINATES ---
    # La structure 
    nouvelles_coords = [55.18, 32.35] # Exemple (Paris)
    data['features'][0]['geometry']['coordinates'] = nouvelles_coords
    print("Nouvelles coordonnées appliquées.")

    # --- ÉTAPE 3 : AJOUT DU COUPLE CLÉ-VALEUR DANS PROPERTIES ---
    data['features'][0]['properties']['prop45'] = True
    
    
    
    print("Propriété 'prop45' ajoutée.")



    with open(chemin, 'w') as f:
        json.dump(data, f, indent=4)
    
    print("\nTout est sauvegardé dans data.json !")

except FileNotFoundError:
    print(f"Erreur : Le fichier est introuvable au chemin '{chemin}'. Vérifie l'emplacement.")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")
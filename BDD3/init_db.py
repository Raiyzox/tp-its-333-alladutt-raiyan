import sqlite3

# Connexion au fichier (Slide 5)
conn = sqlite3.connect('database.db')
print("Base de données ouverte avec succès")

# Création de la table avec les 3 colonnes demandées (Slide 5)
conn.execute('CREATE TABLE etudiants (nom TEXT, addr TEXT, pin TEXT)')
print("Table créée avec succès")

conn.close()
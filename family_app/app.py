from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

# Le fichier où on stockera les données (notre "base de données" simple)
DATA_FILE = 'data.json'

# Fonction pour charger les données
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"recos": [], "agenda": []} # Si le fichier n'existe pas, on crée une structure vide
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Fonction pour sauvegarder
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- PAGE D'ACCUEIL ---
@app.route('/')
def index():
    data = load_data()
    # On envoie les données à la page HTML
    return render_template('index.html', recos=data['recos'], agenda=data['agenda'])

# --- ACTION : AJOUTER UNE RECO ---
@app.route('/add_reco', methods=['POST'])
def add_reco():
    titre = request.form.get('titre')
    type_reco = request.form.get('type') # Film, Expo, etc.
    auteur = request.form.get('auteur')
    
    if titre and auteur:
        data = load_data()
        nouvelle_reco = {
            "titre": titre,
            "type": type_reco,
            "auteur": auteur,
            "date": datetime.now().strftime("%d/%m %H:%M")
        }
        data['recos'].insert(0, nouvelle_reco) # On ajoute au début de la liste
        save_data(data)
    
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

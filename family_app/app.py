from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        try:
            data = json.load(f)
            # Vérification de sécurité si le fichier est vide ou corrompu
            if not isinstance(data, list): return []
            return data
        except:
            return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_users():
    if not os.path.exists('users.json'):
        return []
    with open('users.json', 'r') as f:
        return json.load(f)


# Fonction pour nettoyer les pépites vieilles de plus de 3 mois (90 jours)
def clean_old_entries(data):
    now = datetime.now()
    cutoff = now - timedelta(days=90)
    # On garde seulement les éléments dont la date est plus récente que le cutoff
    # On doit convertir la string 'date' en objet datetime pour comparer
    cleaned_data = []
    for item in data:
        try:
            item_date = datetime.strptime(item['date_obj'], "%Y-%m-%d %H:%M:%S")
            if item_date > cutoff:
                cleaned_data.append(item)
        except KeyError:
            # Si format date incompatible, on garde par sécurité (ou on supprime)
            pass
    return cleaned_data

@app.route('/')
def index():
    data = load_data()
    users = load_users()
    # On nettoie les vieux posts à chaque chargement de page
    data = clean_old_entries(data)
    save_data(data) # On sauvegarde le nettoyage
    return render_template('index.html', recos=data, users = users)

@app.route('/add_reco', methods=['POST'])
def add_reco():
    titre = request.form.get('titre')
    type_reco = request.form.get('type')
    auteur = request.form.get('auteur')
    lien = request.form.get('lien')
    desc = request.form.get('desc')
    tags = request.form.getlist('tags')    

    if titre and auteur:
        data = load_data()
        now = datetime.now()
        nouvelle_reco = {
            "titre": titre,
            "type": type_reco,
            "auteur": auteur,
            "lien": lien,
            "desc": desc,
	    "tags": tags,
            "date_display": now.strftime("%d/%m/%Y"), # Pour l'affichage
            "date_obj": now.strftime("%Y-%m-%d %H:%M:%S") # Pour le tri technique
        }
        data.insert(0, nouvelle_reco)
        save_data(data)
    
    return redirect('/')

if __name__ == '__main__':
    # Le host 0.0.0.0 permet d'être accessible depuis le réseau local
    app.run(host='0.0.0.0', port=5000)

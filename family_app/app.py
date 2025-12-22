import uuid
from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATA_FILE = 'data.json'

# --- GESTION DES DONNEES ---
def load_data():
    # Si le fichier n'existe pas, on retourne un DICTIONNAIRE vide
    if not os.path.exists(DATA_FILE):
        return {} 
    with open(DATA_FILE, 'r') as f:
        try:
            data = json.load(f)
            # On vérifie que c'est bien un dictionnaire
            if not isinstance(data, dict): return {}
            return data
        except:
            return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_users():
    if not os.path.exists('users.json'):
        return []
    with open('users.json', 'r') as f:
        return json.load(f)

def clean_old_entries(data_list):
    # Cette fonction nettoie une LISTE spécifique (recos ou agenda)
    if not isinstance(data_list, list): return []
    
    now = datetime.now()
    cutoff = now - timedelta(days=90)
    cleaned_data = []
    
    for item in data_list:
        try:
            # On vérifie si la clé existe
            if 'date_obj' in item:
                item_date = datetime.strptime(item['date_obj'], "%Y-%m-%d %H:%M:%S")
                if item_date > cutoff:
                    cleaned_data.append(item)
            else:
                cleaned_data.append(item)
        except Exception:
            pass
    return cleaned_data

# --- ROUTE ACCUEIL ---
@app.route('/')
def index():
    data = load_data()
    users = load_users()
    
    # On récupère les listes, ou des listes vides si elles n'existent pas encore
    recos = data.get('recos', [])
    agenda = data.get('agenda', [])

    # Nettoyage des vieilles pépites
    recos = clean_old_entries(recos)

    # Mise à jour et sauvegarde
    data['recos'] = recos
    data['agenda'] = agenda
    save_data(data)
    
    # IMPORTANT : On envoie bien 'recos' (la liste) et pas 'data' (le gros dico)
    return render_template('index.html', recos=recos, agenda=agenda, users=users)

# --- AJOUTER PEPITE ---
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
            "id": str(uuid.uuid4()),
            "titre": titre,
            "type": type_reco,
            "auteur": auteur,
            "lien": lien,
            "desc": desc,
            "tags": tags,
            "date_display": now.strftime("%d/%m/%Y"),
            "date_obj": now.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Si la clé n'existe pas, on crée la liste
        if 'recos' not in data: data['recos'] = []
        
        # On insère DANS la liste 'recos', pas dans data
        data['recos'].insert(0, nouvelle_reco)
        save_data(data)
    
    return redirect('/')

# --- AJOUTER AGENDA ---
@app.route('/add_event', methods=['POST'])
def add_event():
    titre = request.form.get('titre')
    date_event = request.form.get('date') 
    heure_event = request.form.get('heure') 
    desc = request.form.get('desc')
    tags = request.form.getlist('tags')
    
    if titre and date_event:
        data = load_data()
        nouvel_event = {
            "id": str(uuid.uuid4()),
            "titre": titre,
            "date": date_event,
            "heure": heure_event,
            "desc": desc,
            "tags": tags,
            "timestamp": f"{date_event} {heure_event}" 
        }
        
        if 'agenda' not in data: data['agenda'] = []
        data['agenda'].append(nouvel_event)
        
        # Tri chronologique
        data['agenda'].sort(key=lambda x: x['timestamp'])
        
        save_data(data)
    
    return redirect('/')

# --- SUPPRESSION ---
@app.route('/delete/<item_type>/<item_id>')
def delete_item(item_type, item_id):
    data = load_data()
    # item_type est soit 'recos' soit 'agenda'
    if item_type in data and isinstance(data[item_type], list):
        # On filtre la liste pour garder tout sauf l'ID ciblé
        data[item_type] = [item for item in data[item_type] if item.get('id') != item_id]
        save_data(data)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

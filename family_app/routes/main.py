from flask import Blueprint, render_template, request, redirect, session, url_for
from datetime import datetime
import uuid
from utils import load_data, save_data, get_user_list, clean_old_entries

main_bp = Blueprint('main', __name__)

# Fonction de sécurité : à utiliser avant chaque action
def check_auth():
    if 'user' not in session:
        return False
    return True

@main_bp.route('/')
def index():
    # Si pas connecté -> direction Login
    if not check_auth():
        return redirect(url_for('auth.login'))
        
    data = load_data()
    users = get_user_list()
    
    # Récupération et nettoyage
    recos = clean_old_entries(data.get('recos', []))
    agenda = data.get('agenda', []) # Pas de nettoyage auto pour l'agenda pour l'instant
    
    # Sauvegarde du nettoyage
    data['recos'] = recos
    save_data(data)
    
    # On passe le 'current_user' au HTML pour afficher "Bonjour Gabriel"
    return render_template('index.html', recos=recos, agenda=agenda, users=users, current_user=session['user'])

# --- ROUTES D'AJOUT ET SUPPRESSION (Identiques à avant, juste indentées) ---

@main_bp.route('/add_reco', methods=['POST'])
def add_reco():
    if not check_auth(): return redirect(url_for('auth.login'))
    
    # ... (Copie ici ton ancienne logique add_reco, ou je peux te la redonner si besoin)
    # Pour faire court, je mets l'essentiel :
    titre = request.form.get('titre')
    type_reco = request.form.get('type')
    # On force l'auteur à être celui qui est connecté !! Plus de triche !
    auteur = session['user'] 
    
    # ... suite du code standard ...
    # Note : Si tu veux garder le choix de l'auteur manuel, remets request.form.get('auteur')
    # Mais pour la sécurité, c'est mieux d'utiliser session['user']
    
    # JE TE LAISSE LE CODE COMPLET POUR EVITER LES ERREURS :
    lien = request.form.get('lien')
    desc = request.form.get('desc')
    tags = request.form.getlist('tags')
    
    if titre:
        data = load_data()
        now = datetime.now()
        nouvelle_reco = {
            "id": str(uuid.uuid4()),
            "titre": titre,
            "type": type_reco,
            "auteur": auteur, # <-- Ici on peut utiliser la session
            "lien": lien,
            "desc": desc,
            "tags": tags,
            "date_display": now.strftime("%d/%m/%Y"),
            "date_obj": now.strftime("%Y-%m-%d %H:%M:%S")
        }
        if 'recos' not in data: data['recos'] = []
        data['recos'].insert(0, nouvelle_reco)
        save_data(data)
    return redirect(url_for('main.index'))

@main_bp.route('/add_event', methods=['POST'])
def add_event():
    if not check_auth(): return redirect(url_for('auth.login'))
    
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
        data['agenda'].sort(key=lambda x: x['timestamp'])
        save_data(data)
    return redirect(url_for('main.index'))

@main_bp.route('/delete/<item_type>/<item_id>')
def delete_item(item_type, item_id):
    if not check_auth(): return redirect(url_for('auth.login'))
    
    data = load_data()
    if item_type in data and isinstance(data[item_type], list):
        data[item_type] = [item for item in data[item_type] if item.get('id') != item_id]
        save_data(data)
    return redirect(url_for('main.index'))

from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash

from utils import load_users_dict, save_users_dict

# On définit un "Blueprint" (un morceau d'application)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        users = load_users_dict()
        
        # Vérification si l'utilisateur existe et si le mot de passe correspond au hash
        if username in users and check_password_hash(users[username], password):
            session['user'] = username # On enregistre l'utilisateur dans la session
            return redirect(url_for('main.index')) # On renvoie vers l'accueil
        else:
            flash('Mauvais identifiant ou mot de passe !') # Message d'erreur
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None) # On supprime l'utilisateur de la session
    return redirect(url_for('auth.login'))



@auth_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        old_pass = request.form.get('old_password')
        new_pass = request.form.get('new_password')
        confirm_pass = request.form.get('confirm_password')
        
        user = session['user']
        users = load_users_dict()
        
        # 1. Vérifier l'ancien mot de passe
        if not check_password_hash(users[user], old_pass):
            flash("L'ancien mot de passe est incorrect.")
        # 2. Vérifier que les deux nouveaux correspondent
        elif new_pass != confirm_pass:
            flash("Les nouveaux mots de passe ne correspondent pas.")
        # 3. Vérifier que le nouveau n'est pas vide
        elif not new_pass:
            flash("Le mot de passe ne peut pas être vide.")
        else:
            # Tout est bon, on change !
            users[user] = generate_password_hash(new_pass, method='scrypt')
            save_users_dict(users)
            flash("Mot de passe modifié avec succès !")
            return redirect(url_for('main.index'))
            
    return render_template('change_password.html')

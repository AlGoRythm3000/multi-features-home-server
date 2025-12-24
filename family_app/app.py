from flask import Flask
from routes.auth import auth_bp
from routes.main import main_bp

app = Flask(__name__)

# CLE SECRETE OBLIGATOIRE POUR LA SESSION
# En prod, on mettrait ça dans une variable d'environnement, mais là ça ira
app.secret_key = 'une_cle_secrete_tres_difficile_a_deviner_pour_la_famille'

# On enregistre les "Blueprints" (nos morceaux de site)
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

import json
import os
from datetime import datetime, timedelta

DATA_FILE = 'data.json'
USERS_FILE = 'users.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        try:
            data = json.load(f)
            if not isinstance(data, dict): return {}
            return data
        except:
            return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_users_dict():
    # Charge le dictionnaire complet {user: hash}
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def get_user_list():
    # Renvoie juste la liste des prénoms pour l'affichage
    users = load_users_dict()
    return list(users.keys())

def clean_old_entries(data_list):
    if not isinstance(data_list, list): return []
    now = datetime.now()
    cutoff = now - timedelta(days=90)
    cleaned_data = []
    for item in data_list:
        try:
            if 'date_obj' in item:
                item_date = datetime.strptime(item['date_obj'], "%Y-%m-%d %H:%M:%S")
                if item_date > cutoff:
                    cleaned_data.append(item)
            else:
                cleaned_data.append(item)
        except Exception:
            pass
    return cleaned_data


def save_users_dict(users_data):
    with open(USERS_FILE, 'w') as f:
        json.dump(users_data, f, indent=4)

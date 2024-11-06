# -*- coding: utf-8 -*-

try:
    from bs4 import BeautifulSoup
    import requests
except Exception as e:
    print(f"Error: {e}")

# Titre et Bannières
def Title(name):
    print(f"\n{'-'*10} {name} {'-'*10}\n")

Title("OsintMx - Email Tracker")

# Variables de couleur personnalisées
VIOLET = "\033[38;5;93m"       # Violet
LIGHT_BLUE = "\033[38;5;117m"   # Bleu clair
WHITE = "\033[38;5;15m"         # Blanc
RESET = "\033[0m"

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

# Fonction pour vérifier la présence d'un email sur différents sites
def Instagram(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://www.instagram.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.instagram.com/'
        }
        data = {"email": email}
        response = session.get("https://www.instagram.com/accounts/emailsignup/", headers=headers)
        if response.status_code == 200 and 'csrftoken' in session.cookies:
            token = session.cookies['csrftoken']
        else:
            return "Error: Token Not Found."
        
        headers["x-csrftoken"] = token
        response = session.post("https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/", headers=headers, data=data)
        return "Found" if "Another account is using the same email." in response.text or "email_is_taken" in response.text else "Not Found"
    except Exception as e:
        return f"Error: {e}"

def Twitter(email):
    try:
        session = requests.Session()
        response = session.get("https://api.twitter.com/i/users/email_available.json", params={"email": email})
        return "Found" if response.status_code == 200 and response.json().get("taken") else "Not Found"
    except Exception as e:
        return f"Error: {e}"

def Pinterest(email):
    try:
        session = requests.Session()
        response = session.get("https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/", params={
            "source_url": "/",
            "data": '{"options": {"email": "' + email + '"}, "context": {}}'
        })
        return "Found" if response.status_code == 200 and response.json()["resource_response"]["data"] else "Not Found"
    except Exception as e:
        return f"Error: {e}"

def Imgur(email):
    try:
        session = requests.Session()
        headers = {'User-Agent': user_agent, 'X-Requested-With': 'XMLHttpRequest'}
        response = session.post("https://imgur.com/signin/ajax_email_available", headers=headers, data={'email': email})
        return "Found" if response.status_code == 200 and not response.json()['data'].get("available") else "Not Found"
    except Exception as e:
        return f"Error: {e}"

def Patreon(email):
    try:
        session = requests.Session()
        headers = {'User-Agent': user_agent, 'X-Requested-With': 'XMLHttpRequest'}
        response = session.post("https://www.plurk.com/Users/isEmailFound", headers=headers, data={'email': email})
        return "Found" if response.status_code == 200 and "True" in response.text else "Not Found"
    except Exception as e:
        return f"Error: {e}"

def Spotify(email):
    try:
        session = requests.Session()
        headers = {'User-Agent': user_agent}
        response = session.get('https://spclient.wg.spotify.com/signup/public/v1/account', headers=headers, params={'validate': '1', 'email': email})
        return "Found" if response.status_code == 200 and response.json()["status"] == 20 else "Not Found"
    except Exception as e:
        return f"Error: {e}"

def FireFox(email):
    try:
        session = requests.Session()
        response = session.post("https://api.accounts.firefox.com/v1/account/status", data={"email": email})
        return "Found" if response.status_code == 200 and "true" in response.text else "Not Found"
    except Exception as e:
        return f"Error: {e}"

def LastPass(email):
    try:
        session = requests.Session()
        headers = {'User-Agent': user_agent}
        response = session.get("https://lastpass.com/create_account.php", headers=headers, params={'check': 'avail', 'username': email})
        return "Found" if response.status_code == 200 and "no" in response.text else "Not Found"
    except Exception as e:
        return f"Error: {e}"

def Archive(email):
    try:
        session = requests.Session()
        headers = {'User-Agent': user_agent}
        response = session.post('https://archive.org/account/signup', headers=headers, data={'input_name': 'username', 'input_value': email})
        return "Found" if response.status_code == 200 and "is already taken." in response.text else "Not Found"
    except Exception as e:
        return f"Error: {e}"

# Interface utilisateur
email = input(f"{VIOLET}Entrez l'email à scanner : {RESET}")
print(f"{LIGHT_BLUE}Scanning...{RESET}")

sites = [Instagram, Twitter, Pinterest, Imgur, Patreon, Spotify, FireFox, LastPass, Archive]
found, not_found, errors = 0, 0, 0

for site in sites:
    result = site(email)
    if result == "Found":
        print(f"{LIGHT_BLUE}✔ {site.__name__}: {WHITE}Email trouvé!{RESET}")
        found += 1
    elif result == "Not Found":
        print(f"{VIOLET}✘ {site.__name__}: {WHITE}Email non trouvé.{RESET}")
        not_found += 1
    else:
        print(f"{VIOLET}⚠ {site.__name__}: {WHITE}{result}{RESET}")
        errors += 1

# Résumé des résultats
print(f"\n{WHITE}Résultat: {LIGHT_BLUE}Trouvé: {found} {VIOLET}Non Trouvé: {not_found} {VIOLET}Erreurs: {errors}{RESET}")

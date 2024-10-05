import os
import subprocess
import requests
from bs4 import BeautifulSoup

output_directory = '/Users/nunus/Desktop/1234'

os.makedirs(output_directory, exist_ok=True)

commands = {
    "network_info.txt": "ifconfig",
    "active_connections.txt": "netstat -an",
    "wifi_info.txt": "system_profiler SPNetworkDataType",
    "routing_table.txt": "netstat -rn",
    "visible_wifi_networks.txt": "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s"
}

for filename, command in commands.items():
    output_path = os.path.join(output_directory, filename)
    full_command = f"{command} > {output_path}"
    subprocess.run(full_command, shell=True)
    print(f"Commande exécutée et résultat stocké dans : {output_path}")

modem_ip = '192.168.1.1'
username = 'admin'
password = 'admin'

login_url = f'http://{modem_ip}/login'

session = requests.Session()

login_data = {
    'username': username,
    'password': password
}

response = session.post(login_url, data=login_data)

if response.status_code == 200:
    print("Connexion réussie !")
    
    wifi_settings_url = f'http://{modem_ip}/wifi_settings'

    response = session.get(wifi_settings_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        wifi_password = soup.find('input', {'id': 'wifi_password'})['value']
        print(f"Le mot de passe Wi-Fi est : {wifi_password}")
    else:
        print("Impossible d'accéder aux paramètres Wi-Fi.")
else:
    print("Échec de la connexion au modem.")

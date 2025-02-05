import requests
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime
import pytz

# Specify the absolute path to the ping sound file
PING_SOUND_FILE = "ping-82822.mp3"

# Specify your Pushover API key and user token
PUSHOVER_API_KEY = "afvtxe7wgp9vt14qiygh67g8bs345b"
PUSHOVER_USER_TOKEN = "ue9wptsmmpky9yqx8sfup53gs36uaz"

def play_ping_sound():
    try:
        os.system(f"start afplay {PING_SOUND_FILE}")  # For macOS
    except Exception as e:
        print(f"Error playing the sound: {e}")

def send_pushover_notification(message):
    try:
        url = "https://api.pushover.net/1/messages.json"
        data = {
            "token": PUSHOVER_API_KEY,
            "user": PUSHOVER_USER_TOKEN,
            "message": message,
        }
        response = requests.post(url, data=data)
        print(f"Pushover notification sent: {response.json()}")
    except Exception as e:
        print(f"Error sending Pushover notification: {e}")

def check_laadpaal_beschikbaarheid(url):
    # Set the timezone
    tz = pytz.timezone('Europe/Brussels')  # Adjust this to your timezone

    # Get the current time in the specified timezone
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Fetch the HTML from the website
        response = requests.get(url)
        response.raise_for_status()

        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the specific <div> element with the class 'label-availability__available'
        beschikbaarheid_div = soup.find('div', {'class': 'modal-stock-web pointer stock stock-9', 'data-stock-web': '9'})

        if beschikbaarheid_div and beschikbaarheid_div.text.strip() != "Rupture":
            print(f"{timestamp} - Asus beschikbaar: Beschikbaar")
            play_ping_sound()  # Call the function to play the ping sound
            send_pushover_notification(f"{timestamp} - De Asus is nu beschikbaar!")  # Call the function to send the Pushover notification
            return True  # Signal that the loop should stop

        else:
            print(f"{timestamp} - Asus not available")

    except requests.exceptions.RequestException as e:
        print(f"{timestamp} - Error fetching the website: {e}")

    return False  # Signal that the loop should continue

def check_laadpaal_beschikbaarheid_2(url):
    # Set the timezone
    tz = pytz.timezone('Europe/Brussels')  # Adjust this to your timezone

    # Get the current time in the specified timezone
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Fetch the HTML from the website
        response = requests.get(url)
        response.raise_for_status()

        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the specific <div> element with the class 'label-availability__available'
        beschikbaarheid_div = soup.find('div', {'class': 'modal-stock-web pointer stock stock-9', 'data-stock-web': '9'})

        if beschikbaarheid_div and beschikbaarheid_div.text.strip() != "Rupture":
            print(f"{timestamp} - Msi beschikbaar: Beschikbaar")
            play_ping_sound()  # Call the function to play the ping sound
            send_pushover_notification(f"{timestamp} - De Msi is nu beschikbaar!")  # Call the function to send the Pushover notification
            return True  # Signal that the loop should stop

        else:
            print(f"{timestamp} - Msi not available")

    except requests.exceptions.RequestException as e:
        print(f"{timestamp} - Error fetching the website: {e}")

    return False  # Signal that the loop should continue

def check_coolblue_msi(url):
    # Set the timezone
    tz = pytz.timezone('Europe/Brussels')  # Adjust this to your timezone

    # Get the current time in the specified timezone
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Fetch the HTML from the website
        response = requests.get(url)
        response.raise_for_status()

        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the specific <div> element with the class 'label-availability__available'
        beschikbaarheid_div = soup.find('div', {'class': 'color--unavailable'})

        if beschikbaarheid_div and "Binnenkort leverbaar" in beschikbaarheid_div.text.strip():
            print(f"{timestamp} - Msi Coolblue beschikbaar: Beschikbaar")
            play_ping_sound()  # Call the function to play the ping sound
            send_pushover_notification(f"{timestamp} - De MSI is nu beschikbaar op Coolblue!")  # Call the function to send the Pushover notification
            return True  # Signal that the loop should stop

        else:
            print(f"{timestamp} - Msi Coolblue not available")

    except requests.exceptions.RequestException as e:
        print(f"{timestamp} - Error fetching the website: {e}")

    return False  # Signal that the loop should continue

if __name__ == "__main__":
    url = "https://www.ldlc.pro/fiche/PB00663199.html"
    url2 = "https://www.ldlc.pro/fiche/PB00661910.html"
    url3 = "https://www.coolblue.be/nl/product/959803/msi-geforce-rtx-5090-ventus-3x-oc-32gb.html"

    while True:
        if not check_laadpaal_beschikbaarheid(url):
            time.sleep(1)
        if not check_laadpaal_beschikbaarheid_2(url2):
            time.sleep(1)
        if not check_coolblue_msi(url3):
            time.sleep(1)
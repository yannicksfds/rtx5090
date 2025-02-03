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
        beschikbaarheid_div = soup.find('div', {'class': 'label-availability__available'})

        if beschikbaarheid_div:
            print(f"{timestamp} - Laadpaal beschikbaar: Beschikbaar")
            play_ping_sound()  # Call the function to play the ping sound
            send_pushover_notification(f"{timestamp} - De laadpaal is nu beschikbaar!")  # Call the function to send the Pushover notification
            return True  # Signal that the loop should stop

        else:
            print(f"{timestamp} - Laadpaal beschikbaar: Niet beschikbaar")

    except requests.exceptions.RequestException as e:
        print(f"{timestamp} - Error fetching the website: {e}")

    return False  # Signal that the loop should continue

if __name__ == "__main__":
    url = "https://nl.chargemap.com/allego-parking-kerkhof.html"

    while not check_laadpaal_beschikbaarheid(url):
        # Wait for 30 seconds before the next check
        time.sleep(1)

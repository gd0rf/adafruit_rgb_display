import requests
import time
from datetime import datetime
import json
import time
import threading
import subprocess


# Flag to track if a command is running
is_command_running = False
command_thread = None


# Replace these with your Steam API key and Steam ID
STEAM_API_KEY = "your_steam_api_key"
STEAM_ID = "your_steam_id"
XBL_API_KEY = "your_xbox_api_key"
XBOX_XUID = "your_xbox_xuid"  # Xbox User ID (XUID)

def get_current_steam_game(api_key, steam_id):
    """Fetches the current game being played on Steam."""
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = {
        "key": api_key,
        "steamids": steam_id
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "response" in data and "players" in data["response"]:
            player = data["response"]["players"][0]
            return player.get("gameextrainfo")  # None if no game is being played
    except requests.RequestException as e:
        print(f"Steam API error: {e}")
    return None

def get_current_xbox_game(api_key, xuid):
    """Fetches the current game being played on Xbox using xbl.io API."""
    url = f"https://xbl.io/api/v2/presence/"
    headers = {
        "X-Authorization": api_key
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(data)
        print("-"*50)
        if isinstance(data, list):  # Ensure response is a list
            online_titles = []
            offline_entries = []

            # Process each entry in the response
            for entry in data:
                print(entry)
                print("-"*50)
                # If state is online, collect the title
                if entry.get("state") == "Offline" and "lastSeen" in entry:
                    title_name = entry["lastSeen"].get("titleName")
                    if title_name:
                        online_titles.append(title_name)
                # Otherwise, collect offline lastSeen entries
                elif "lastSeen" in entry:
                    offline_entries.append(entry["lastSeen"])

            # If online titles exist, return the first one
            if online_titles:
                return online_titles

            # If no online titles, fallback to the most recent offline game
            if offline_entries:
                most_recent = max(offline_entries, key=lambda x: datetime.fromisoformat(x["timestamp"]))
                return most_recent.get("titleName", None)

        return None
    except requests.RequestException as e:
        print(f"xbl.io API error: {e}")
    return None

def load_json_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_json_to_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def get_image_path(game_name, data, filename):
    # If game not found, add it and set path to 'Images/default.jpg'
    if game_name not in data:
        data[game_name] = "/home/pi/rpi-rgb-led-matrix/utils/Images/default.jpg"
        save_json_to_file(filename, data)
        print(f"Game '{game_name}' not found. Added with default path '/home/pi/rpi-rgb-led-matrix/utils/Images/default.jpg'.")
        return "/home/pi/rpi-rgb-led-matrix/utils/Images/default.png"
    else:
        return data[game_name]

data = load_json_from_file('games.json')

# Function to execute the command with an updated image
def execute_command(updated_image_path):
    global is_command_running, command_process

    if not is_command_running:
        # Start the command with the updated image path
        print(f"Starting command with image: {updated_image_path}")
        is_command_running = True
        command_process = subprocess.Popen(
            ['sudo', './led-image-viewer', '--led-rows=64', '--led-cols=64', '--led-gpio-mapping=adafruit-hat', 
             '--led-slowdown-gpio=2', updated_image_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    else:
        # Cancel the current command and start a new one with updated image
        print("Command is already running. Canceling and restarting...")
        cancel_command()
        time.sleep(1)  # Wait a moment before restarting
        execute_command(updated_image_path)  # Restart the command with the new image

# Function to cancel the current running command
def cancel_command():
    global is_command_running, command_process
    if is_command_running:
        print("Stopping the command...")
        command_process.terminate()  # Terminate the running command
        command_process.wait()  # Wait for the process to terminate
        is_command_running = False

def stop_command():
    global is_command_running, command_process
    if is_command_running:
        print("Stopping the command...")
        command_process.terminate()  # Terminate the running command
        command_process.wait()  # Wait for the process to terminate
        is_command_running = False
        print("Command stopped.")
    else:
        print("No command is currently running.")

def main():
    """Continuously checks for current games on Steam and Xbox."""
    last_game = None

    while True:
        print("Checking for current game...")
        
        # Check Steam first
        current_game = get_current_steam_game(STEAM_API_KEY, STEAM_ID)
        
        #if not current_game:  # If no game on Steam, check Xbox
        #    current_game = get_current_xbox_game(XBL_API_KEY, XBOX_XUID)
        
        if current_game != last_game:
            if current_game:
                print(f"Current game: {current_game}")
                image_path = get_image_path(current_game, data, 'games.json')
                print(f"The path to the image for {current_game} is: {image_path}")
                execute_command(image_path)
            else:
                print("No game currently being played.")
                stop_command()  # Stop the command
            last_game = current_game

        time.sleep(30)  # Check every 10 seconds

if __name__ == "__main__":
    main()

# Game Status Display with Steam Integration

This Python script continuously checks the current game being played on Steam and and updates an LED display with the corresponding game image. The image associated with the current game is retrieved from a JSON file, and if no game is found, a default image is used. The script also manages the command to display the image on an LED matrix.

## Features
- Fetches the current game being played on Steam using the Steam API.
- Retrieves and updates the image for the current game from a `games.json` file.
- Displays the game image on an LED matrix using the `led-image-viewer` command.
- Stops and restarts the display command if the game changes.
- Saves the path to the game image in `games.json` if the game is not found.
- Runs continuously, checking for game status every 30 seconds.

## Prerequisites
- Python 3.x
- Required libraries: `requests`, `json`, `subprocess`
- A running instance of `led-image-viewer` for displaying images on an LED matrix.
- Steam API keys.

## Installation
1. Install the required Python libraries:
   ```bash
   pip install requests
2. Ensure that the led-image-viewer tool is installed and accessible in the environment. This tool is used to display images on an LED matrix.
3. Ensure that you have a games.json file with game names and corresponding image paths. The default image path will be used if a game is not found.
4. Replace the placeholders for the Steam API keys in the script:
   ```bash
   STEAM_API_KEY = "your_steam_api_key"
   STEAM_ID = "your_steam_id"

## How It Works
1. The script checks the current game being played on Steam using the get_current_steam_game() function.
3. The current game name is checked against the games.json file to retrieve the image path.
4. If the game is not found, a default image path is used, and the game is added to the games.json file.
5. The execute_command() function runs the led-image-viewer command to display the image on an LED matrix.
6. If a new game is detected, the previous command is stopped and restarted with the new image.

## Functions Overview
- get_current_steam_game(api_key, steam_id): Fetches the current game being played on Steam.
- get_current_xbox_game(api_key, xuid): Fetches the current game being played on Xbox (using the xbl.io API).   //not working
- load_json_from_file(filename): Loads a JSON file to store game image mappings.
- save_json_to_file(filename, data): Saves game image mappings to a JSON file.
- get_image_path(game_name, data, filename): Retrieves the image path for a given game, adding it to the JSON file if not found.
- execute_command(updated_image_path): Executes the led-image-viewer command with the updated image path.
- cancel_command(): Cancels the current running command.
- stop_command(): Stops the currently running command.
- main(): The main function that checks for the current game and updates the display.

## Usage
1. Ensure that the necessary dependencies are installed and that the Steam API keys are set.
2. Run the script:
   ```bash
   python game_status_display.py
3. The script will continuously check the game being played and update the LED display every 30 seconds.

## Troubleshooting
- If no game is detected, ensure that the Steam API keys are correct and that the Steam ID are valid.
- If the command to display the image fails, verify that led-image-viewer is installed and properly configured for your LED matrix.
- If the games.json file is missing or empty, the script will automatically create it with the default game image.

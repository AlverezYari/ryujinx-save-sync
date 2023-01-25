# Ryujinx Save Sync

A Python based mini app that will sync the 'save' directories between a PC and SteamDeck for the popular Ryujinx Switch Emulator. This app can be deployed in a container.

## Requirements

- Python 3.9 or later
- The `paramiko` library for SSH communication
- The `pytz` library for timezone conversion
- SSH access to the SteamDeck with the appropriate credentials
- The emulator should be installed on the SteamDeck.

## Usage

1. Clone the repository and navigate to the project directory.
2. Create a `config.json` file in the same directory as the script with the following structure:
{
"steamdeck": {
"host": "hostname or IP",
"port": 22,
"username": "username",
"password": "password",
"ryujinx_save_dir": "/path/to/ryujinx/save/directory"
},
"local": {
"ryujinx_save_dir": "/path/to/local/ryujinx/save/directory"
}
}

Copy code
3. Run the script with the following command:
python ryujinx_save_sync.py

Copy code

The script will connect to the SteamDeck using SSH, list the files in the Ryujinx save directory on the SteamDeck and the local machine, compare the timestamps of the files and copies the newer files from the local machine to the SteamDeck.

This script will also convert the timestamps of the files to UTC before making the comparison and also ignore any files that have different naming scheme.

## Note

- Please make sure to take a backup of your save data before running the script.
- This script only copies files from the local machine to the SteamDeck, and it will not delete any files on the SteamDeck.
- This script only works for files with the same naming scheme.
- This script assumes that the emulator is installed on the SteamDeck and the save directory is located in the same path as specified in the `config.json` file.
- If you have any issues or suggestions, please open an issue on the repository.

## Future improvements
-
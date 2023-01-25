###
# Ryujinx Steam-Deck Save Sync App
# By:
# https://github.com/AlverezYari
# 2023
###
import os
import json
import subprocess
from datetime import datetime
import pytz

# 3rd party
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

## func

def load_config():
    config_file = os.environ['CONFIG_FILE']
    with open(config_file) as f:
        config = json.load(f)
    return config

def get_files_and_timestamps(save_state):

    target_files_timestamps = {}

    for line in save_state.splitlines()[3:]:
        parts = line.split()
        print(parts)
        timestamp = parts[5] + ' ' + parts[6] + ' ' + parts[7]
        filename = parts[8]
        target_files_timestamps[filename] = datetime.strptime(timestamp, '%b %d %H:%M')

    return target_files_timestamps

def create_sync_target_obj(pc_files, deck_files):
    sync_targets = []
    for file, timestamp in pc_files.items():
        if file in deck_files:
            deck_file_timestamp = deck_files[file]
            if timestamp > deck_file_timestamp:
                sync_targets.append({"game_id":file, "sync_head" : 0})
            else:
                sync_targets.append({"game_id":file, "sync_head" : 1})
    return sync_targets

def get_pc_saves_state(config):
    result = subprocess.Popen(['ls','-la', config['steam_sync_config']["pc_save_location"] ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate()
    return stdout.decode()

def get_deck_saves_state(config, ssh):
    _stdin, _stdout,_stderr = ssh.exec_command("ls -la " + config['steam_sync_config']["deck_save_location"])
    return _stdout.read().decode()

def create_ssh_client(config):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(config['steam_sync_config']['deck_address'], username=config['steam_sync_config']['deck_uname'], password=config['steam_sync_config']['deck_passwd'])
    return ssh

def push_to_deck(title):
    print(
        'Newer copy of save dir found on PC \n ====Pushing save to SteamDeck=====' 
        )
    return

def pull_to_pc(title):
    print(
        'Newer copy of save dir found on the SteamDeck \n ====Pull remote save to local PC=====' 
        )
    return

def sync_saves(sync_targets):
    for title in sync_targets:
        print(title)
        print('Checking Title: ' + title['game_id'])
        if title['sync_head'] == 0:
            push_to_deck(title)
        elif title['sync_head'] == 1:
            pull_to_pc(title)
    return

# main loop

def main():
    config = load_config()
    ssh = create_ssh_client(config)
    deck_save_state = get_deck_saves_state(config, ssh)
    # print(deck_save_state)
    deck_files = get_files_and_timestamps(deck_save_state)
    pc_save_state = get_pc_saves_state(config)
    # print(pc_save_state)
    pc_files = get_files_and_timestamps(pc_save_state)
    sync_targets = create_sync_target_obj(pc_files, deck_files)
    sync_saves(sync_targets)
    return

# run
main()
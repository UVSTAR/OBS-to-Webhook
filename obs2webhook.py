import obspython as obs
import os
import requests
import time
import threading
import json

# Global variables for the script settings
webhook_url = ""
folder_path = ""
delete_after_upload = False
sent_files = set()
sent_files_path = os.path.join(obs.obs_data_get_string(obs.obs_data_create(), "script_path"), "sent_files.json")

# Function to load sent files from a JSON file
def load_sent_files():
    global sent_files
    if os.path.exists(sent_files_path):
        with open(sent_files_path, 'r') as file:
            sent_files = set(json.load(file))
    else:
        save_sent_files()  # Create the file if it doesn't exist

# Function to save sent files to a JSON file
def save_sent_files():
    global sent_files
    with open(sent_files_path, 'w') as file:
        json.dump(list(sent_files), file)

# Function to find the latest video file in the folder
def get_latest_video(folder):
    try:
        files = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".mp4", ".mov", ".avi",".mkv"))
        ]
        if not files:
            return None
        files.sort(key=os.path.getmtime, reverse=True)
        for file in files:
            if file not in sent_files:
                return file
        return None
    except Exception as e:
        obs.script_log(obs.LOG_ERROR, f"Error finding latest video: {e}")
        return None

# Function to send the latest video to the webhook URL
def send_video(latest_video):
    global webhook_url, delete_after_upload

    if not webhook_url:
        obs.script_log(obs.LOG_WARNING, "Webhook URL is not set.")
        return False

    try:
        with open(latest_video, 'rb') as file:
            response = requests.post(webhook_url, files={"file": file})

        if response.status_code == 200:
            obs.script_log(obs.LOG_INFO, f"Video successfully sent: {latest_video}")
            if delete_after_upload:
                os.remove(latest_video)
                obs.script_log(obs.LOG_INFO, f"Video deleted: {latest_video}")
            return True
        else:
            obs.script_log(obs.LOG_ERROR, f"Failed to send video. Status code: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        obs.script_log(obs.LOG_ERROR, f"Error sending video: {e}")
        return False

# Thread to monitor the folder for new files
def monitor_folder():
    global folder_path, sent_files

    while True:
        if not folder_path:
            time.sleep(1)  # Reduced cooldown to 1 second
            continue

        latest_video = get_latest_video(folder_path)

        if latest_video:
            obs.script_log(obs.LOG_INFO, f"New video detected: {latest_video}")
            if send_video(latest_video):
                sent_files.add(latest_video)
                save_sent_files()

        time.sleep(1)  # Reduced cooldown to 1 second

# OBS script properties
def script_description():
    return "Automatically send the latest video file from a specified folder to a webhook URL."

def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(props, "webhook_url", "Webhook URL", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_path(props, "folder_path", "Folder Path", obs.OBS_PATH_DIRECTORY, "", None)
    obs.obs_properties_add_bool(props, "delete_after_upload", "Delete video after upload")

    return props

def script_update(settings):
    global webhook_url, folder_path, delete_after_upload

    webhook_url = obs.obs_data_get_string(settings, "webhook_url")
    folder_path = obs.obs_data_get_string(settings, "folder_path")
    delete_after_upload = obs.obs_data_get_bool(settings, "delete_after_upload")

def script_load(settings):
    load_sent_files()
    threading.Thread(target=monitor_folder, daemon=True).start()
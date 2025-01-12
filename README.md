# OBS2Webhook

This script automatically sends the latest video file from a specified folder to a webhook URL using OBS Studio.

## Features

- Automatically detects new video files in a specified folder.
- Sends the latest video file to a specified webhook URL.
- Option to delete the video file after upload.
- Prevents re-uploading the same video on OBS relaunch.

## Requirements

- Python 3.10 or higher(WON'T WORK ON PYTHON VERSION NOT SUPPORTED BY OBS)
- OBS Studio

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/UVSTAR/OBS2Webhook.git
    cd OBS2Webhook
    ```

2. **Install Python 3.10:**

    Download and install Python 3.10 from the [official Python website](https://www.python.org/downloads/release/python-3100/).

3. **Install the required Python packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Add the script to OBS Studio:**

    - Open OBS Studio.
    - Go to `Tools` > `Scripts`.
    - Click the `+` button and add the `obs2webhook.py` script.

5. **Configure the script:**

    - Set the `Webhook URL` to your desired webhook endpoint.
    - Set the `Folder Path` to the directory where your video files are saved.
    - Optionally, enable the `Delete video after upload` checkbox if you want to delete the video file after it is uploaded.

## License

This project is licensed under the MIT License. See the LICENSE file for details.


## Contact

For any questions or suggestions, please open an issue on GitHub.

---

### requirements.txt

```plaintext
requests

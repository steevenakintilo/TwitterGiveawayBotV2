"""File that handle utility functions"""

import pyotp
from discord_webhook import DiscordWebhook

# Too general exception
# pylint: disable=W0718

# No exception type specified
# pylint: disable=W0702

def write_into_file(path:str, data:str) -> None:
    """A function that write data into a file"""
    with open(path, "ab") as f:
        f.write(str(data).encode("utf-8"))

def reset_file(path:str) -> None:
    """A function that reset a file"""
    f = open(path, "w",encoding="utf8")
    f.write("")
    f.close()

def print_file_content(path:str) -> str:
    """A function that print the content of a file"""
    f = open(path, 'r',encoding="utf-8")
    content = f.read()
    f.close()
    return content

def generate_totp(secret: str, time_step: int = 30):
    """A function that generate a totp code"""
    try:
        totp = pyotp.TOTP(secret, interval=time_step)
        return totp.now()
    except Exception as e:
        return f"Error generating TOTP: {e}"

def send_message_discord(msg,url_path):
    """A function that send discord message with webhook"""
    try:    
        webhook = DiscordWebhook(url=url_path, content=msg)
        webhook.execute()
    except:
        pass

def send_message_discord_with_pic(msg,url_path,path="screenshot.png"):
    """A function that send discord message + picture with webhook"""
    try:
        webhook = DiscordWebhook(url=url_path, content=msg)
        webhook.execute()
        if path:
            with open(path, "rb") as f:
                webhook.add_file(file=f.read(), filename=path)
        webhook.execute()
    except:
        pass
def convert_seconds_to_hms(seconds):
    """A function that convert second to hour,minute,seconde"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    return hours, minutes, remaining_seconds

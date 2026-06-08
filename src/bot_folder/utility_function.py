"""File that handle utility functions"""

import pyotp
from discord_webhook import DiscordWebhook

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
        response = webhook.execute()
    except:
        pass

def send_message_discord_with_pic(msg):
    """A function that send discord message + picture with webhook"""
    path = "screen.png"
    try:
        urls = "https://discord.com/api/webhooks/1297590847193219185/SFGzu7jwhGh8oWiUmrrQWvpbB7cfGXdhXbE0rgr_1SSpYmtA1zu8x5Mm3VFJq08jbQy0"
        webhook = DiscordWebhook(url=urls, content=msg)        
        if path:
            with open(path, "rb") as f:
                webhook.add_file(file=f.read(), filename=path)
        response = webhook.execute()
    except:
        pass
def convert_seconds_to_hms(seconds):
    """A function that convert second to hour,minute,seconde"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    return hours, minutes, remaining_seconds
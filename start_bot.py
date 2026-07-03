"""File that launch all the bot"""

import json
import os
import time

import platform
import traceback
import yaml

from discord_webhook import DiscordWebhook


# No exception type specified
# pylint: disable=W0702

class bot_launcher():
    """Bot launcher class"""
    def __init__(self):
        self.group_of_the_day = int(self.print_file_content("group_of_the_day.txt")[0])

        with open("configuration.yml", "r",encoding="utf-8") as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)
        
        with open("discord_data_dict.json", "r", encoding="utf-8") as file:
            self.discord_dict = json.load(file)

    def write_into_file(self,path:str, data:str) -> None:
        """A function that write data into a file"""
        with open(path, "ab") as f:
            f.write(str(data).encode("utf-8"))

    def reset_file(self,path:str) -> None:
        """A function that reset a file"""
        f = open(path, "w",encoding="utf8")
        f.write("")
        f.close()

    def print_file_content(self,path:str) -> str:
        """A function that print the content of a file"""
        f = open(path, 'r',encoding="utf-8")
        content = f.read()
        f.close()
        return content

    def send_message_discord(self,msg,url_path) -> None:
        """A function that send discord message with webhook"""
        try:
            webhook = DiscordWebhook(url=url_path, content=msg)
            webhook.execute()
        except:
            pass
    
    def convert_seconds_to_hms(self,seconds):
        """A function that convert second to hour,minute,seconde"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60

        return hours, minutes, remaining_seconds
        
    def check_for_update(self):
        """A function that will check if the code has been updated"""
        os_system = platform.system()
        os.system("git pull")
        if os_system != "Windows":
            os.system("chmod +x ./src/copy_twitter.sh")
            os.system("./src/copy_twitter.sh")
        else:
            os.system(r"cd src && .\copy_twitter.bat")

    def start(self) -> None:
        """A function that will start all the bot"""
        os.system("pip install --upgrade cloakbrowser")
        start = time.time()
        folder_to_skip = [
            "bot_folder",
            "find_giveaway",
            "__pycache__",
            "move_url.bat",
            "twitter.py",
            "txt_files_folder"
        ]

        index = 0
        # Launch Giveaway / Random Tweet to RT

        # Launch All bot
        self.send_message_discord("-"*20,self.discord_dict["list_of_account_time_statistics"])
        self.send_message_discord("Hello World",self.discord_dict["list_of_account_time_statistics"])

        search_giveaway = True
        if search_giveaway:
            os.system("cd src/find_giveaway && python find_giveaway.py")

        empty_space = "‎"
        self.send_message_discord(f"{empty_space}\n"*3,self.discord_dict["list_of_account_time_statistics"])

        self.send_message_discord(f"Starting giveaway on account of group {self.group_of_the_day}",self.discord_dict["list_of_account_time_statistics"])
        account_of_the_day = self.print_file_content(f"account_of_groupe{str(self.group_of_the_day)}_name.txt").split("\n")
        for bot in account_of_the_day:
            
            if bot not in folder_to_skip:
                index+=1
                print(bot)
                self.send_message_discord(f"{bot} {index}/{len(account_of_the_day)} accounts done",self.discord_dict["list_of_account_time_statistics"])
                os.system(f"cd src/{bot} && python main.py")

        self.send_message_discord("All accounts are done",self.discord_dict["list_of_account_time_statistics"])

        new_day = self.group_of_the_day + 1 if self.group_of_the_day + 1 <= 3 else 1

        try:
            if str(self.group_of_the_day) == "1":
                self.check_for_update()
        except:
            pass
        # End

        self.reset_file("group_of_the_day.txt")
        self.write_into_file("group_of_the_day.txt",new_day)
        end = time.time()
        print(f"Execution time: {end - start:.6f} seconds")
        elapsed_seconds = int(end - start)
        hours, minutes, remaining_seconds = self.convert_seconds_to_hms(elapsed_seconds)

        try:
            self.send_message_discord(f"List of giveaway done today {len(self.print_file_content("list_of_giveaway_done_today.txt").split("\n")) - 1}",self.discord_dict["list_of_account_time_statistics"])
            self.send_message_discord(f"List of all giveaway done {len(self.print_file_content("list_of_all_giveaway_done.txt").split("\n")) - 1}",self.discord_dict["list_of_account_time_statistics"])
        except:
            traceback.print_exc()

        self.reset_file("list_of_giveaway_done_today.txt")
        if self.data["search_for_win"]:
            os.system("cd src/check_for_win_bot && python main.py")

        print(f"It took {hours} hours, {minutes} minutes, and {remaining_seconds} seconds.")
        self.send_message_discord(f"It took {hours} hours, {minutes} minutes, and {remaining_seconds} seconds.",self.discord_dict["list_of_account_time_statistics"])

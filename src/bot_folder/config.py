"""Twitter bot file"""
from datetime import datetime
from random import randint
from random import shuffle

import json
import os
import time
import traceback
import yaml

from cloakbrowser import launch_persistent_context
from global_variable import *
from utility_function import *


# Undifined Variable
# pylint: disable=E0602

# Too general exception
# pylint: disable=W0718

# No exception type specified
# pylint: disable=W0702

# Line is too long
# pylint: disable=C0301

class TwitterBot():
    """Main class"""
    def __init__(self):
        with open("../../configuration.yml", "r",encoding="utf-8") as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)
        with open("configuration.yml", "r",encoding="utf-8") as file:
            self.data2 = yaml.load(file, Loader=yaml.FullLoader)
        
        self.username = self.data2["account_username"][0]
        self.password = self.data2["account_password"][0]
        self.today_date = datetime.now().date()

        current_directory = os.getcwd()
        currentDir = current_directory.split("\\")[-1]
        
        self.browser = launch_persistent_context(user_data_dir=f"./{currentDir}",geoip=True,headless=False,humanize=True)
        self.page = self.browser.new_page()
        
        self.otp_accounts = print_file_content("../../otp_acc.txt").lower().replace("\t"," ").strip().split("\n")
        self.list_of_account_you_follow = print_file_content("list_of_account_you_follow.txt").lower().split("\n")
        self.print_error = False

        self.otp_acc = False
        with open("../../discord_data_dict.json", "r", encoding="utf-8") as file:
            self.discord_dict = json.load(file)

        for acc in self.otp_accounts:
            if self.username.lower() in acc.lower() and " " in acc.lower():
                print("OTP Account")
                self.otp_acc = True
                self.otp_code = acc.split()[1]
                print(self.otp_code)
                break

        if self.username == "test_account":
            self.username = currentDir

    def start(self) -> bool:
        """A function to start the bot"""
        print(f"Hello {self.username}")
        self.page.goto(TWITTER_LOGIN_PAGE_URL)

        #date_today = datetime.now().strftime("%d/%m/%Y")
        #reset_file("last_run.txt")
        
        #url_to_test = "https://x.com/L_ThinkTank/status/2063274599328948555"

        #time.sleep(3600)
        time.sleep(600)
        self.browser.close()

        
        

config = TwitterBot()
config.start()

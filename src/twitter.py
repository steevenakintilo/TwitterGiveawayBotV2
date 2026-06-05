from cloakbrowser import launch
from .global_variable import *
from random import randint

import time
import traceback
import yaml


# pylint: disable=E0602

class TwitterBot():
    def __init__(self):
        self.browser = launch(geoip=True,headless=False,humanize=True)
        self.page = self.browser.new_page(viewport=None)
        with open("configuration.yml", "r",encoding="utf-8") as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)
        self.username = self.data["account_username"][0]
        self.password = self.data["account_password"][0]
        
    def login(self):
        """A function to login to your account"""
        try:
            self.page.goto(TWITTER_LOGIN_PAGE_URL)
            self.page.locator(USERNAME_OR_EMAIL_ATTRIBUTE).fill(self.username)
            self.page.locator(BUTTON_SUBMIT_ATTRIBUTE).click()
            self.page.locator(PASSWORD_ATTRIBUTE).fill(self.password)
            self.page.locator(BUTTON_SUBMIT_ATTRIBUTE).click()
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                print("Connection Error")
                return False

            traceback.print_exc()
            return False

    def accept_cookie(self):
        """A function that accept cookie"""
        try:
            self.page.locator('xpath=//*[@id="layers"]/div/div[3]/div/div/div/div[2]/button[1]').click()
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.accept_cookie()
            
            traceback.print_exc()

    def start(self):
        """A function to start the bot"""
        print(f"Hello {self.username}")
        if self.login() is False:
            return False
        self.accept_cookie()
        time.sleep(10000)

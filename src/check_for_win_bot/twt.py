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
from datetime import datetime, timedelta, date
from global_variable_ import *
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
        with open("configuration.yml", "r",encoding="utf-8") as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)
        
        self.username = self.data["account_username"][0]
        self.password = self.data["account_password"][0]
        self.today_date = datetime.now().date()

        self.browser = launch_persistent_context(user_data_dir="./check_for_win_bot",geoip=True,headless=False,humanize=False)
        self.page = self.browser.new_page()
        
        self.otp_accounts = print_file_content("../../otp_acc.txt").lower().replace("\t"," ").strip().split("\n")
        current_directory = os.getcwd()
        currentDir = current_directory.split("\\")[-1]
        self.print_error = False

        self.otp_acc = False
        with open("../../discord_data_dict.json", "r", encoding="utf-8") as file:
            self.discord_dict = json.load(file)

        for acc in self.otp_accounts:
            if self.username.lower() in acc.lower() and " " in acc.lower():
                print("OTP Account")
                self.otp_acc = True
                self.otp_code = acc.split()[1]
                print(self.otp_acc,self.otp_code)
                break
        
        if self.username == "test_account":
            self.username = currentDir

    def login(self):
        """A function to login to your account"""
        try:
            self.page.goto(TWITTER_LOGIN_PAGE_URL)
            
            self.page.locator(USERNAME_OR_EMAIL_ATTRIBUTE).fill(self.username)
            time.sleep(10)

            self.page.locator(BUTTON_SUBMIT_ATTRIBUTE).click()
            #self.random_stop()
            time.sleep(10)
            
            self.page.locator(PASSWORD_ATTRIBUTE).fill(self.password)
            time.sleep(10)
            
            # time.sleep(10)
            # return True
            #self.page.locator(PASSWORD_ATTRIBUTE).press("Enter")

            self.page.locator(BUTTON_SUBMIT_ATTRIBUTE2).click()
            time.sleep(10)
            
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                print("Connection Error")
                return False
            if self.print_error:
                traceback.print_exc()
            return False

    def accept_cookie(self) -> None:
        """A function that accept cookie"""
        try:
            self.page.locator(ACCEPT_COOKIE_ATTRIBUTE).click()
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.accept_cookie()
            if self.print_error:
                traceback.print_exc()

    def is_login_good(self) -> bool:
        """A function that check if the login went well"""
        try:
            self.page.goto(f"https://x.com/{self.username}", wait_until="domcontentloaded")
            time.sleep(randint(5,10))

            if self.page.viewport_size is None:
                self.page.set_viewport_size({"width": 1280, "height": 720})

            try:
                self.page.locator(EDIT_PROFILE_ATTRIBUTE).click(timeout=3000)
            except:
                self.page.locator(MAKE_A_POST_ATTRIBUTE).click(timeout=3000)

            time.sleep(randint(1,5))
            return True
        except Exception as e:
            traceback.print_exc()

            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.is_login_good()

            return False

    def set_otp_code(self,code) -> bool:
        """A function that will set otp code"""
        try:
            self.page.locator(OTP_CODE_TEXTBOX_ATTRIBUTE).click()
            time.sleep(3)
            time.sleep(randint(1,5))
            print("otp code " , generate_totp(code.upper()))
            self.page.locator(OTP_CODE_TEXTBOX_ATTRIBUTE).fill(generate_totp(code.upper()))
            time.sleep(3)
            self.random_stop()
            return True

        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.set_otp_code(code)

            if self.print_error:
                traceback.print_exc()

            return False

    def random_stop(self) -> None:
        """A function that add random time.sleep"""
        time.sleep(randint(1,60))

    def search_tweets(self,search_query,user) -> list[str]:
        """A function that sear tweets"""
        self.page.goto(SEARCH_TWEET_URL)
        time.sleep(5)
        self.page.locator(SEARCHBOX_ATTRIBUTE).fill(search_query)
        time.sleep(3)
        self.page.locator(SEARCHBOX_ATTRIBUTE).press("Enter")
        time.sleep(3)
        self.page.goto(f"{self.page.url}&f=live")
        time.sleep(3)
        #tweet_info = self.page.locator(TWEET_ATTRIBUTE).text_content()
        try:
            tweet = self.page.locator(TWEET_ATTRIBUTE).first
            outer_html = tweet.evaluate("el => el.outerHTML")
            #text = tweet.inner_text()
            tweet_id = f"https://x.com/i/web/status/{outer_html.split("/status/")[2].split("/")[0]}"
            all_giveaway_won = print_file_content("giveaway_won.txt").lower().split("\n")
            if tweet_id.lower() not in all_giveaway_won:
                write_into_file("giveaway_won.txt",tweet_id+"\n")

            send_message_discord(f"{user} won a new giveaway",self.discord_dict["giveaway_won_channel"])
            send_message_discord(f"Giveaway link {tweet_id}",self.discord_dict["giveaway_won_channel"])
            send_message_discord(f"Search querry done {self.page.url}&f=live",self.discord_dict["giveaway_won_channel"])

            print(f"{user} won a new giveaway")
            print(tweet_id)
            print("\n\n\n")
            print(f"{self.page.url}&f=live")
            time.sleep(15)
        except:
            time.sleep(1)

    def remove_days(self,days_to_remove=14):
        """A function that remove x days from a date"""
        if days_to_remove < 0:
            days_to_remove = 0

        date_format = "%Y-%m-%d"
        today_date = datetime.now().strftime("%Y-%m-%d")
        current_date = datetime.strptime(today_date, date_format)
        new_date = current_date - timedelta(days=days_to_remove)

        return(new_date.strftime(date_format))

    def start(self,max_retry=0) -> bool:
        """A function to start the bot"""
        print("Searching for giveaway you may have won")

        send_message_discord("Searching for giveaway won!",self.discord_dict["giveaway_won_channel"])

        last_run = print_file_content("last_run.txt")
        date_today = datetime.now().strftime("%d/%m/%Y")
        first_time = False

        if len(last_run) > 3:
            write_into_file("last_run.txt",date_today)
            write_into_file("all_run.txt",date_today+"\n")

        else:
            first_time = True
            reset_file("last_run.txt")
            write_into_file("last_run.txt",date_today)
            write_into_file("all_run.txt",date_today+"\n")

        if first_time:
            time.sleep(3)
            if self.login() is False:
                if max_retry == 0:
                    self.browser.close()
                    self.start(1)
                else:
                    self.browser.close()
                    return False

                #CHECK OTP APRES

            if self.otp_acc:
                print("icicici")
                if self.set_otp_code(self.otp_code) is False:
                    if max_retry == 0:
                        self.browser.close()
                        self.start(1)
                    else:
                        self.browser.close()
                        send_message_discord(f"OTP error on login for https://x.com/{self.username}",self.discord_dict["list_of_login_error_channel"])

                        return False
            else:
                first_time = True

        if self.is_login_good() is False:
            send_message_discord(f"Bad login for https://x.com/{self.username}",self.discord_dict["list_of_login_error_channel"])

            self.browser.close()
            return False

        if first_time:
            time.sleep(10)
        self.page.goto("https://x.com/home")
        #url_to_test = "https://x.com/L_ThinkTank/status/2063274599328948555"

        time.sleep(10)
        self.page.goto(TWEET_TO_SEE_AFTER_LOGIN)

        time.sleep(10)

        if first_time:
            self.accept_cookie()
            time.sleep(30)

        list_of_user = print_file_content("../../all_acc.txt").lower().split("\n")
        search_user = "("

        for user in list_of_user:
            search_user =f'@{user} '
            search_query = "("
            for win_word in self.data["win_keywords"]:
                search_query+=f'"{win_word}" OR '

            search_query = search_query[0:-5]
            search_result = search_user + " " + search_query
            self.search_tweets(f'{search_result}")  since:{str(self.remove_days(14))}',user)
            print(f'{search_result}")')
            print("\n\n\n")
            
        send_message_discord("End of search",self.discord_dict["giveaway_won_channel"])
        self.browser.close()
        return True

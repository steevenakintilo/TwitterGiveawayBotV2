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
        
        self.username = ""
        self.password = self.data2["account_password"][0]
        self.today_date = datetime.now().date()

        current_directory = os.getcwd()
        currentDir = current_directory.split("\\")[-1]
        self.currentDir = currentDir
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

    
    def login(self,username,password):
        """A function to login to your account"""
        try:
            self.page.goto(TWITTER_LOGIN_PAGE_URL)
            
            self.page.locator(USERNAME_OR_EMAIL_ATTRIBUTE).fill(username)
            self.page.locator(BUTTON_SUBMIT_ATTRIBUTE).click()
            #self.random_stop()
            self.page.locator(PASSWORD_ATTRIBUTE).fill(password)

            # time.sleep(10)
            # return True
            #self.page.locator(PASSWORD_ATTRIBUTE).press("Enter")

            self.page.locator(BUTTON_SUBMIT_ATTRIBUTE2).click()

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
            
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.is_login_good()

            return False
        
    def random_stop(self) -> None:
        """A function that add random time.sleep"""
        time.sleep(randint(1,60))
    
    def set_otp_code(self,code) -> bool:
        """A function that will set otp code"""
        try:
            self.page.locator(OTP_CODE_TEXTBOX_ATTRIBUTE).click()
            time.sleep(randint(1,5))
            print("otp code " , generate_totp(code.upper()))
            try:
                self.page.locator(OTP_CODE_TEXTBOX_ATTRIBUTE).fill(generate_totp(code.upper()))
            except:
                self.page.keyboard.type(generate_totp(code.upper()))
            
            self.random_stop()
            return True
            # try:
            #     self.page.locator(CODEPASS_TEXTBOX_ATTRIBUTE).fill("2001")
            # except:
            #     pass

        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.set_otp_code(code)

            if self.print_error:
                traceback.print_exc()

            return False


    def change_username(self,new_username) -> bool:
        """A function to change your username"""
        try:
            self.page.goto(CHANGE_USERNAME_PAGE)
            time.sleep(randint(1,3))
            self.page.locator(CHANGE_USERNAME_ATTRIBUTE).click()
            time.sleep(randint(1,3))
            self.page.locator(CHANGE_USERNAME_ATTRIBUTE).fill("")
            time.sleep(randint(1,2))
            self.page.locator(CHANGE_USERNAME_ATTRIBUTE).fill(new_username)
            time.sleep(randint(1,3))
            self.page.locator(SAVE_SETTING_BUTTON_ATTRIBUTE).click()
            time.sleep(randint(5,10))
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.change_username(new_username)
            return False

    def change_password(self,old_password,new_password) -> bool:
        """A function to change your password"""
        try:
            self.page.goto(CHANGE_PASSWORD_PAGE)

            time.sleep(randint(1,3))
            self.page.locator(CONFIRM_PASSWORD_ATTRIBUTE).click()
            self.page.locator(CHOOSE_NEW_PASSWORD_ATTRIBUTE).click()
            self.page.locator(CONFIRM_NEW_PASSWORD_ATTRIBUTE).click()


            time.sleep(randint(1,3))
            self.page.locator(CONFIRM_PASSWORD_ATTRIBUTE).fill(old_password)
            self.page.locator(CHOOSE_NEW_PASSWORD_ATTRIBUTE).fill(new_password)
            self.page.locator(CONFIRM_NEW_PASSWORD_ATTRIBUTE).fill(new_password)
            self.page.locator(SAVE_SETTING_BUTTON_ATTRIBUTE).click()
            time.sleep(randint(5,10))
            
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.change_password(old_password,new_password)

            #traceback.print_exc()
            return False

    def change_information(self,new_name,new_bio,new_location) -> bool:
        """A function to change your username"""
        try:
            self.page.goto(CHANGE_PROFILE_PAGE)
            time.sleep(randint(1,3))

            # NAME
            self.page.locator(CHANGE_NAME_ATTRIBUTE).click()
            time.sleep(randint(1,3))
            self.page.locator(CHANGE_NAME_ATTRIBUTE).fill("")
            time.sleep(randint(1,2))
            self.page.locator(CHANGE_NAME_ATTRIBUTE).fill(new_name)
            time.sleep(randint(1,3))

            #BIO
            self.page.locator(CHANGE_BIO_ATTRIBUTE).click()
            time.sleep(randint(1,3))
            self.page.locator(CHANGE_BIO_ATTRIBUTE).fill("")
            time.sleep(randint(1,2))
            self.page.locator(CHANGE_BIO_ATTRIBUTE).fill(new_bio)
            time.sleep(randint(1,3))

            #LOCATION
            self.page.locator(CHANGE_LOCATION_ATTRIBUTE).click()
            time.sleep(randint(1,3))
            self.page.locator(CHANGE_LOCATION_ATTRIBUTE).fill("")
            time.sleep(randint(1,2))
            self.page.locator(CHANGE_LOCATION_ATTRIBUTE).fill(new_location)
            time.sleep(randint(1,3))

            self.page.locator(SAVE_PROFILE_BUTTON_ATTRIBUTE).click()
            time.sleep(randint(5,10))
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.change_information(new_name,new_bio,new_location)
            return False
    def change_banner(self,filepath):
        """A function to change your banner"""
        try:
            self.page.goto(CHANGE_PROFILE_PAGE)
            time.sleep(randint(5,10))
            REMOVE_BANNER_ATTRIBUTE = 'xpath=//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div[3]/div/button[3]'
            try:
                self.page.locator(REMOVE_BANNER_ATTRIBUTE).click()
                time.sleep(randint(2,4))
            except:
                pass
            self.page.locator(CHANGE_PICTURE_ATTRIBUTE).nth(0).set_input_files(filepath)
            time.sleep(5)
            self.page.locator(CONFIRM_NEW_PICTURE_ATTRIBUTE).evaluate("el => el.click()")
            time.sleep(randint(5,10))
            return True
        except Exception as e:

            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.change_banner(filepath)
            return False
    def change_profile_picture(self,filepath,load_page=False):
        """A function to change your profile picture"""
        try:
            if load_page:
                self.page.goto(CHANGE_PROFILE_PAGE)
                time.sleep(randint(5,10))
            self.page.locator(CHANGE_PICTURE_ATTRIBUTE).nth(1).set_input_files(filepath)
            time.sleep(5)
            self.page.locator(CONFIRM_NEW_PICTURE_ATTRIBUTE).click()
            time.sleep(randint(5,10))
            self.page.locator(SAVE_PROFILE_BUTTON_ATTRIBUTE).click()
            time.sleep(randint(5,10))

            return True
        except Exception as e:

            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.change_profile_picture(filepath)
            return False

    def check_if_private(self,username) -> bool:
        """A function that check if an account is private"""

        try:
            self.page.goto(f"https://x.com/{username}")
            time.sleep(randint(5,10))
            try:
                self.page.locator(PRIVATE_ACCOUNT_BUTTON_OBJ).click()
                return True                
            except:
                return False

            # self.page.goto(CHECK_IF_ACCOUNT_IS_PRIVATE_PAGE)
            # time.sleep(randint(5,10))
            # self.page.locator(PRIVATE_ACCOUNT_BUTTON_ATTRIBUTE).click()
            
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.check_if_private(username)
            return False
    
    def change_language_to_english(self) -> bool:
        """A function to change the language to english"""
        try:
            self.page.goto(CHANGE_LANGUAGE_PAGE)
            time.sleep(randint(5,10))
            current_language = self.page.locator("body").inner_text().split("-")[1].split("\n")[0]

            if "english" in current_language.lower() or "british english" in current_language.lower():
                print("English already set")
                return True
            
            time.sleep(randint(1,3))
            self.page.locator(CHOOSE_LANGUAGE_INPUT_ATTRIBUTE).click()
            time.sleep(randint(1,3))
            self.page.locator(CHOOSE_LANGUAGE_INPUT_ATTRIBUTE).fill(current_language)
            time.sleep(randint(1,3))
            self.page.locator(CHANGE_LANGUAGE_BUTTON_ATTRIBUTE).click()
            
            time.sleep(randint(3,5))
            self.page.locator(CHOOSE_LANGUAGE_INPUT_ATTRIBUTE).click()
            time.sleep(randint(1,3))
            self.page.locator(CHOOSE_LANGUAGE_INPUT_ATTRIBUTE).fill("English")
            time.sleep(randint(1,3))
            self.page.locator(CHANGE_LANGUAGE_BUTTON_ATTRIBUTE).click()
            time.sleep(randint(5,10))
            self.page.locator(SUBMIT_NEW_LANGUAGE_ATTRIBUTE).click()
            time.sleep(randint(1,3))
            #

        except Exception as e:
            traceback.print_exc()
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.change_language_to_english()
            return False


    def del_first_line(self,filepath):
        """A function that delete the first line of a file"""
        with open(filepath, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(filepath, "w", encoding="utf-8") as file:
            file.writelines(lines[1:])

    def start(self) -> bool:
        """A function to start the bot"""
        print(f"Hello {self.username}")
        try:
            order = print_file_content("../order.txt").split("\n")[0]
        except:
            return True
        if len(order) < 10:
            return True
        order_info_list = order.split(":")
        print(order.split(":"))

        self.otp_acc = True
        self.otp_code = order_info_list[4]
        old_password = order_info_list[1]
        new_password = "steeven1"
        current_username = order_info_list[0]
        new_username = print_file_content("../../random_ok_username.txt").split("\n")[0]
        new_bio = print_file_content("../../random_bio.txt").split("\n")[0]
        new_location = print_file_content("../../random_city.txt").split("\n")[0]
        new_name = print_file_content("../../random_username.txt").split("\n")[0]
        self.username = current_username
        print(old_password,new_password,current_username,new_username,new_bio,new_location,new_name)
             
    
        self.page.goto(TWITTER_LOGIN_PAGE_URL)

        need_login = True

        if need_login:
            check_login = self.is_login_good()
            time.sleep(10)

            if check_login is False:
                if self.login(current_username,old_password) is False:
                    send_message_discord(f"Bad login on creation for https://x.com/{self.username}",self.discord_dict["list_of_login_error_channel"])
                    self.browser.close()
                    return False

                #CHECK OTP APRES

                if self.otp_acc:
                    if self.set_otp_code(self.otp_code) is False:
                        self.browser.close()
                        send_message_discord(f"OTP error on login for creation of https://x.com/{self.username}",self.discord_dict["list_of_login_error_channel"])
                        self.browser.close()
                        return False


            if self.is_login_good() is False:
                send_message_discord(f"Bad login for https://x.com/{self.username}",self.discord_dict["list_of_login_error_channel"])

                self.browser.close()
                return False
            time.sleep(10)
            self.page.goto("https://x.com/home")
            #url_to_test = "https://x.com/L_ThinkTank/status/2063274599328948555"

            time.sleep(10)
            self.page.goto(TWEET_TO_SEE_AFTER_LOGIN)

            time.sleep(10)

            self.accept_cookie()
            time.sleep(10)

            #date_today = datetime.now().strftime("%d/%m/%Y")
            #reset_file("last_run.txt")

            #url_to_test = "https://x.com/L_ThinkTank/status/2063274599328948555"

            #time.sleep(3600)

        if need_login is False:
            time.sleep(10)

        done = True
        if done:
            self.change_password(old_password,new_password)

            self.change_username(new_username)

            self.change_information(new_name,new_bio,new_location)

            profile_picture_dir = r"C:\Users\sakin\Music\zzzzzzzzzPhoto\photo_de_profile_ok"
            banner_dir = r"C:\Users\sakin\Music\zzzzzzzzzPhoto\bannieres_ok"
            random_profile_picture_path = rf"{profile_picture_dir}\{os.listdir(profile_picture_dir)[0]}"
            random_banner_path = rf"{banner_dir}\{os.listdir(banner_dir)[0]}"

            new_banner = self.change_banner(random_banner_path)
            if new_banner is False:
                new_banner = self.change_banner(random_banner_path)

            if new_banner:
                os.remove(random_banner_path)
            new_profile_picture = self.change_profile_picture(random_profile_picture_path,not new_banner)
            if new_profile_picture is False:
                new_profile_picture = self.change_profile_picture(random_profile_picture_path,not new_banner)    
            if new_profile_picture:
                os.remove(random_profile_picture_path)
            is_private = self.check_if_private(new_username)
            print("is_private " , is_private)
            self.change_language_to_english()

            self.page.goto(f"https://x.com/{new_username}")
            time.sleep(randint(5,10))
            self.page.screenshot(path="profile.png")
            print(f"New account {new_username} done!")
            if is_private:
                send_message_discord_with_pic(f"New account {new_username} done but he is private! https://x.com/{new_username}",self.discord_dict["new_account_made_channel"],"profile.png")
            else:
                send_message_discord_with_pic(f"New account {new_username} done! https://x.com/{new_username}",self.discord_dict["new_account_made_channel"],"profile.png")

                
        self.del_first_line("../../random_ok_username.txt")
        self.del_first_line("../../random_bio.txt")
        self.del_first_line("../../random_city.txt")
        self.del_first_line("../../random_name.txt")
        self.del_first_line("../order.txt")
        try:
            group_of_the_day = int(print_file_content("../../group_of_the_day.txt")[0])
            group_of_the_day = randint(1,3)
            write_into_file("all_acc.txt",new_username+"\n")
            write_into_file("otp_acc.txt",new_username+" " + self.otp_code + "\n")
            write_into_file(f"account_of_groupe{group_of_the_day}_name.txt",new_username+"\n")
        except:
            pass
        self.browser.close()
        return True


config = TwitterBot()
config.start()

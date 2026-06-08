from cloakbrowser import launch
from .global_variable import *
from random import randint

import time
import traceback
import yaml



# Undifined Variable
# pylint: disable=E0602

# Too general exception
# pylint: disable=W0718

# No exception type specified
# pylint: disable=W0702

class TwitterBot():
    """Main class"""
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
            self.page.locator(ACCEPT_COOKIE_ATTRIBUTE).click()
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.accept_cookie()

            traceback.print_exc()

    def like_a_tweet(self,url):
        """A function to like a tweet"""
        try:
            self.page.goto(url)
            self.page.locator(LIKE_A_TWEET_ATTRIBUTE).click()
            self.random_stop()
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.like_a_tweet(url)

            traceback.print_exc()

    def unlike_a_tweet(self,url):
        """A function to unlike a tweet"""
        try:
            self.page.goto(url)
            self.page.locator(UNLIKE_A_TWEET_ATTRIBUTE).click()
            self.random_stop()
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.unlike_a_tweet(url)

            traceback.print_exc()

    def retweet_a_tweet(self,url,load_page=True):
        """A function to retweet a tweet"""
        try:
            if load_page:
                self.page.goto(url)
            self.page.locator(RETWEET_A_TWEET_ATTRIBUTE).click()
            time.sleep(randint(1,5))
            self.page.locator(RETWEET_CONFIRM_ATTRIBUTE).click()
            self.random_stop()
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.retweet_a_tweet(url,load_page)

            traceback.print_exc()
    
    
    def unretweet_a_tweet(self,url,load_page=True):
        """A function to retweet a tweet"""
        try:
            if load_page:
                self.page.goto(url)
            self.page.locator(UNRETWEET_A_TWEET_ATTRIBUTE).click()
            time.sleep(randint(1,5))
            self.page.locator(UNRETWEET_CONFIRM_ATTRIBUTE).click()
            
            self.random_stop()
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.unretweet_a_tweet(url,load_page)

            traceback.print_exc()
    
    def comment_a_tweet(self,url,text,load_page=True):
        """A function to comment a tweet"""
        try:
            if load_page:
                self.page.goto(url)
            #self.page.locator(COMMENT_A_TWEET_ATTRIBUTE).click()
            self.page.locator(COMMENT_TEXTBOX_ATTRIBUTE).click()  
            self.page.locator(COMMENT_A_TWEET_ATTRIBUTE).fill(text)
            time.sleep(randint(1,5))
            self.page.locator(POST_A_TWEET_BUTTON_ATTRIBUTE).click()
            self.random_stop()


        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.comment_a_tweet(url,text,load_page)

            traceback.print_exc()
    
    def follow_an_account(self,account):
        """A function to follow an account"""
        try:
            self.page.goto(f"https://x.com/{account}")
            self.page.locator(FOLLOW_AN_ACCOUNT_ATTRIBUTE).click()
            self.random_stop()


        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.follow_an_account(account)

            traceback.print_exc()

    def unfollow_an_account(self,account):
        """A function to unfollow an account"""
        try:
            self.page.goto(f"https://x.com/{account}")
            self.page.locator(UNFOLLOW_AN_ACCOUNT_ATTRIBUTE).click()
            time.sleep(randint(1,5))
            self.page.locator(UNFOLLOW_AN_ACCOUNT_CONFIRM_ATTRIBUTE).click()
            self.random_stop()

        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.unfollow_an_account(account)

            traceback.print_exc()

    def is_login_good(self):
        """A function that check if the login went well"""
        try:
            self.page.goto(f"https://x.com/{self.username}")
            self.page.locator(EDIT_PROFILE_ATTRIBUTE)
            time.sleep(randint(1,5))
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.is_login_good()

            return False

    def setup_passcode(self,fast=False):
        """A function that will create a passcode"""
        try:
            if fast is False:
                self.page.locator(CREATE_A_PASSCODE_ATTRIBUTE).click()
                time.sleep(randint(1,5))

            self.page.locator(CODEPASS_TEXTBOX_ATTRIBUTE).fill("2001")
            time.sleep(randint(1,5))

            self.page.locator(CODEPASS_TEXTBOX_ATTRIBUTE).fill("2001")
            time.sleep(randint(1,5))
            
            # try:
            #     self.page.locator(CODEPASS_TEXTBOX_ATTRIBUTE).fill("2001")
            # except:
            #     pass

        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)

    def is_passcode_for_dm_needed(self):
        """A function that check if passcode for dm is needed"""
        try:
            self.page.locator(FORGOT_PIN_ATTRIBUTE).wait_for(timeout=5000)
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                    time.sleep(60 * 15)
                    self.is_passcode_for_dm_needed()

            return False
    
    def check_dm(self):
        """A function that will check if an user has recieved a new dm"""
        try:
            try:
                self.page.locator(NEW_DM_ATTRIBUTE).wait_for(timeout=5000)
                if self.is_passcode_for_dm_needed():
                    self.setup_passcode(True)
                
            except:
                return
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.check_dm()
            return
    def random_stop(self):
        """A function that add random time.sleep"""
        time.sleep(randint(1,60))

    def start(self):
        """A function to start the bot"""
        print(f"Hello {self.username}")
        first_time = False
        if self.login() is False:
            self.browser.close()
            return False

        if self.is_login_good() is False:
            print(f"Bad login on {self.username}")
            self.browser.close()
            return False
        
        time.sleep(10)
        self.page.goto(TWEET_TO_SEE_AFTER_LOGIN)
        url_to_test = "https://x.com/L_ThinkTank/status/2063274599328948555"
        
        self.random_stop()
        self.accept_cookie()
        time.sleep(30)
        if first_time:
            self.setup_passcode()
        else:
            self.check_dm()
        # self.retweet_a_tweet("https://x.com/L_ThinkTank/status/2063274599328948555")
        # self.unretweet_a_tweet("https://x.com/L_ThinkTank/status/2063274599328948555")
        # self.retweet_a_tweet("https://x.com/L_ThinkTank/status/2063274599328948555",False)
        # self.follow_an_account("L_ThinkTank")
        # self.unfollow_an_account("L_ThinkTank")
        # self.follow_an_account("L_ThinkTank")
        
        time.sleep(10000)
        self.browser.close()
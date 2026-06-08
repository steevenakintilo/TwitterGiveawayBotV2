"""Twitter bot file"""

from cloakbrowser import launch
from datetime import datetime
from global_variable import *
from utility_function import *
from random import randint
from random import shuffle

import json
import os
import time
import traceback
import yaml

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
        self.browser = launch(geoip=True,headless=False,humanize=True)
        self.page = self.browser.new_page(viewport=None)
        with open("../../configuration.yml", "r",encoding="utf-8") as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)
        self.username = self.data["account_username"][0]
        self.password = self.data["account_password"][0]
        self.today_date = datetime.now().date()
        
        self.otp_accounts = print_file_content("../txt_account_file_folder/otp_acc.txt").lower().replace("\t"," ").strip().split("\n")
        self.list_of_account_you_follow = print_file_content("list_of_account_you_follow.txt").lower().split("\n")
        current_directory = os.getcwd()
        currentDir = current_directory.split("\\")[-1]

        self.otp_acc = False
        try:
            with open("../../discord_data_dict2.json", "r", encoding="utf-8") as file:
                self.discord_dict = json.load(file)
        except:
            with open("../../discord_data_dict2.json", "r", encoding="utf-8") as file:
                self.discord_dict = json.load(file)

        for acc in self.otp_accounts:
            if self.username.lower() in acc.lower() and " " in acc.lower():
                print("OTP Account")
                self.otp_acc = True
                self.otp_code = acc.split()[1]
                print(self.otp_acc,self.otp_code)
        
        if self.username == "test_account":
            self.username = currentDir
        
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

    def accept_cookie(self) -> None:
        """A function that accept cookie"""
        try:
            self.page.locator(ACCEPT_COOKIE_ATTRIBUTE).click()
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.accept_cookie()

            traceback.print_exc()

    def like_a_tweet(self,url) -> bool:
        """A function to like a tweet"""
        try:
            self.page.goto(url)
            self.page.locator(LIKE_A_TWEET_ATTRIBUTE).click()
            self.random_stop()
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.like_a_tweet(url)

            traceback.print_exc()
            return False
    def unlike_a_tweet(self,url) -> bool:
        """A function to unlike a tweet"""
        try:
            self.page.goto(url)
            self.page.locator(UNLIKE_A_TWEET_ATTRIBUTE).click()
            self.random_stop()
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.unlike_a_tweet(url)

            traceback.print_exc()
            return False

    def retweet_a_tweet(self,url,load_page=True) -> bool:
        """A function to retweet a tweet"""
        try:
            if load_page:
                self.page.goto(url)
            self.page.locator(RETWEET_A_TWEET_ATTRIBUTE).click()
            time.sleep(randint(1,5))
            self.page.locator(RETWEET_CONFIRM_ATTRIBUTE).click()
            self.random_stop()
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.retweet_a_tweet(url,load_page)

            traceback.print_exc()
            return False
    
    
    def unretweet_a_tweet(self,url,load_page=True) -> bool:
        """A function to retweet a tweet"""
        try:
            if load_page:
                self.page.goto(url)
            self.page.locator(UNRETWEET_A_TWEET_ATTRIBUTE).click()
            time.sleep(randint(1,5))
            self.page.locator(UNRETWEET_CONFIRM_ATTRIBUTE).click()
            
            self.random_stop()
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.unretweet_a_tweet(url,load_page)

            traceback.print_exc()
            return False
    def comment_a_tweet(self,url,text,load_page=True) -> bool:
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
            return True

        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.comment_a_tweet(url,text,load_page)

            traceback.print_exc()
            return False
    
    def follow_an_account(self,account) -> bool:
        """A function to follow an account"""
        try:
            if account.lower() in self.list_of_account_you_follow():
                print(f"SKIP {account} you already follow it")
                return True
            self.page.goto(f"https://x.com/{account}")
            try:
                self.page.locator(UNFOLLOW_AN_ACCOUNT_ATTRIBUTE).wait_for(timeout=3000)
                print(f"You already follow {account}")
                return True
            except:
                pass
            self.page.locator(FOLLOW_AN_ACCOUNT_ATTRIBUTE).click()
            self.random_stop()
            write_into_file("list_of_account_you_follow.txt",account.lower()+"\n")
            return True

        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.follow_an_account(account)

            traceback.print_exc()
            return False

    def unfollow_an_account(self,account) -> bool:
        """A function to unfollow an account"""
        try:
            self.page.goto(f"https://x.com/{account}")
            self.page.locator(UNFOLLOW_AN_ACCOUNT_ATTRIBUTE).click()
            time.sleep(randint(1,5))
            self.page.locator(UNFOLLOW_AN_ACCOUNT_CONFIRM_ATTRIBUTE).click()
            self.random_stop()
            return True

        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.unfollow_an_account(account)

            traceback.print_exc()
            return False

    def is_login_good(self) -> bool:
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

    def setup_passcode(self,fast=False) -> bool:
        """A function that will create a passcode"""
        try:
            if fast is False:
                self.page.locator(CREATE_A_PASSCODE_ATTRIBUTE).click()
                time.sleep(randint(1,5))

            self.page.locator(CODEPASS_TEXTBOX_ATTRIBUTE).fill("2001")
            time.sleep(randint(1,5))

            self.page.locator(CODEPASS_TEXTBOX_ATTRIBUTE).fill("2001")
            time.sleep(randint(1,5))
            return True
            
            # try:
            #     self.page.locator(CODEPASS_TEXTBOX_ATTRIBUTE).fill("2001")
            # except:
            #     pass

        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
            return False

    def set_otp_code(self,code) -> bool:
        """A function that will set otp code"""
        try:
            self.page.locator(OTP_CODE_TEXTBOX_ATTRIBUTE).click()
            time.sleep(randint(1,5))
            self.page.locator(OTP_CODE_TEXTBOX_ATTRIBUTE).fill(code)
            self.random_stop()
            return True
            # try:
            #     self.page.locator(CODEPASS_TEXTBOX_ATTRIBUTE).fill("2001")
            # except:
            #     pass

        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.set_otp_code()
            return False
    
    def is_passcode_for_dm_needed(self)  -> bool:
        """A function that check if passcode for dm is needed"""
        try:
            self.page.locator(FORGOT_PIN_ATTRIBUTE).wait_for(timeout=5000)
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.is_passcode_for_dm_needed()

            return False

    def check_dm(self)  -> None:
        """A function that will check if an user has recieved a new dm"""
        try:
            try:
                self.page.locator(NEW_DM_ATTRIBUTE).wait_for(timeout=5000)
                if self.is_passcode_for_dm_needed():
                    self.setup_passcode(True)

            except:
                return None
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.check_dm()
            return None

    def random_stop(self) -> None:
        """A function that add random time.sleep"""
        time.sleep(randint(1,60))

    def is_giveaway_over(self,url) -> int:
        """This function check if the giveaway is over"""
        draw_date = print_file_content(r"../txt_files_folder/drawDate.txt").lower().split("\n")
        for draw in draw_date:
            if url.lower() in draw:
                giveaway_date = datetime.strptime(draw.split(" ")[0], '%Y-%m-%d').date()
                delta = self.today_date - giveaway_date
                if delta.days == 0:
                    return 0
                elif delta.days > 0:
                    return -1
                else:
                    return 1
        return -999

    def is_giveaway_date_today(self) -> list:
        """This function check if a giveaway date is today"""
        draw_date = print_file_content(r"../txt_files_folder/drawDate.txt").lower().split("\n")
        today_giveaway = []
        for draw in draw_date:
            if len(str(draw)) > 10:
                giveaway_date = datetime.strptime(draw.split(" ")[0], '%Y-%m-%d').date()
                delta = self.today_date - giveaway_date
                if delta.days == 0:
                    today_giveaway.append(draw.split(" ")[1])
        return today_giveaway

    def is_user_valid(self,user) -> bool:
        """A function that check if an username is valid"""
        valid_char = "abcdefghijklmnopqrstuvwxyz0123456789_"
        user = user.lower()

        for u in user:
            if u not in valid_char:
                return False
        return True

    def who_many_people_to_tag(self,nb) -> list:
        "A function that return the right number of people to tag and their username"

        try:
            accountListToTag = print_file_content("account_to_tag.txt").split("\n")
            accounts_to_tag = []

            for acc in accountListToTag:
                lower_string = str(acc).lower()
                if self.username.lower() in lower_string or self.username.lower() == lower_string:
                    acc = acc.replace(self.username,"").split(",")
                    for account in acc:
                        if len(account) > 3:
                            accounts_to_tag.append(" @"+account + " ")
                    shuffle(accounts_to_tag)
                    break
        except:
            accounts_to_tag = ["@Inoxtag " , "@Mediavenir " , "@Arkunir"]
            shuffle(accounts_to_tag)

        if nb == 1:
            return accounts_to_tag[0]
        if nb == 2:
            return accounts_to_tag[0]+" "+accounts_to_tag[1]
        return " ".join(accounts_to_tag)

    
    def get_all_giveaway_data(self) -> list:
        """A function that will get all the giveaway url,comment and account to follow"""
        list_of_tweet_url = []
        list_of_account_to_follow = []
        list_of_comment = []
        need_to_comment_or_not = []
        skip_this_giveaway = []
        redo_this_giveaway = []

        all_giveaway = print_file_content("../txt_files_folder/all_giveaway.txt").lower().split("\n")
        all_account_to_follow = print_file_content("../txt_files_folder/user_to_follow.txt").lower().split("\n")
        all_comment = print_file_content("../txt_files_folder/all_comment.txt").lower().split("\n")
        for giveaway in all_giveaway:
            split_giveaway = giveaway.split(" ")
            if len(split_giveaway[0]) > 1:
                date = datetime.strptime(split_giveaway[1].replace(":","-"), '%Y-%m-%d').date()
                delta = self.today_date - date
                if delta.days <= 6:
                    over = self.is_giveaway_over(split_giveaway[0])
                    if over == 0:
                        skip_this_giveaway.append(False)
                        redo_this_giveaway.append(True)
                    elif over == -1:
                        skip_this_giveaway.append(True)
                        redo_this_giveaway.append(False)
                    else:
                        skip_this_giveaway.append(False)
                        redo_this_giveaway.append(False)

                    list_of_tweet_url.append(split_giveaway[0])

        for account_to_follow in all_account_to_follow:
            split_account = account_to_follow.split(" ")
            if len(split_account[0]) > 1:
                date = datetime.strptime(split_account[1].replace(":","-"), '%Y-%m-%d').date()
                delta = self.today_date - date
                if delta.days <= 6 and self.is_user_valid(split_account[0]) and split_account[0] not in list_of_account_to_follow:
                    list_of_account_to_follow.append(split_account[0])

        for comment in all_comment:
            split_comment = comment.split("##@@##")
            if len(split_comment[0]) > 1:
                date = datetime.strptime(split_comment[-1].replace(":","-"), '%Y-%m-%d').date()
                delta = self.today_date - date
                if delta.days <= 6:
                    if split_comment[0] == "true":
                        #print(split_comment)
                        if "sentence_for_tag" in split_comment[1]:
                            sentence_part_one = self.data["sentence_for_tag"][randint(0 , len(self.data["sentence_for_tag"]) - 1)]
                            sentence_part_two = ""
                            if "@1@" in split_comment[1]:
                                sentence_part_two = self.who_many_people_to_tag(1)
                            if "@2@" in split_comment[1]:
                                sentence_part_two = self.who_many_people_to_tag(2)
                            if "@3@" in split_comment[1]:
                                sentence_part_two = self.who_many_people_to_tag(3)
                            list_of_comment.append(sentence_part_one + " " + sentence_part_two)
                        if "sentence_for_random_comment" in split_comment[1]:
                            sentence_part_one = self.data["sentence_for_random_comment"][randint(0 , len(self.data["sentence_for_random_comment"]) - 1)]
                            sentence_part_two = ""

                            if "@1@" in split_comment[1]:
                                sentence_part_two = self.who_many_people_to_tag(1)
                            if "@2@" in split_comment[1]:
                                sentence_part_two = self.who_many_people_to_tag(2)
                            if "@3@" in split_comment[1]:
                                sentence_part_two = self.who_many_people_to_tag(3)
                            list_of_comment.append(sentence_part_one + " " + sentence_part_two)
                        if "[" not in split_comment[1] and "]" not in split_comment[1]:
                            if "@1@" in split_comment[1]:
                                list_of_comment.append(self.who_many_people_to_tag(1))
                            if "@2@" in split_comment[1]:
                                list_of_comment.append(self.who_many_people_to_tag(2))
                            if "@3@" in split_comment[1]:
                                list_of_comment.append(self.who_many_people_to_tag(3))

                        if "[" in split_comment[1] and "]" in split_comment[1]:
                            sentence_part_one = ""
                            sentence_part_two = ""
                            two_part = False
                            part_two_comment = ""

                            if "@1@" in split_comment[1]:
                                sentence_part_two = self.who_many_people_to_tag(1)
                            if "@2@" in split_comment[1]:
                                sentence_part_two = self.who_many_people_to_tag(2)
                            if "@3@" in split_comment[1]:
                                sentence_part_two = self.who_many_people_to_tag(3)


                            if len(split_comment[1].split("]")) > 0:
                                two_part = True
                                part_two_comment = split_comment[1].split("]")[1]
                            if two_part:
                                split_split_comment = split_comment[1].replace("[","").replace("]","").split(", ")                 
                                shuffle(split_split_comment)
                                sentence_part_one = split_split_comment[0].replace("'","") + " " + part_two_comment 
                            else:
                                split_split_comment = split_comment[1].replace("[","").replace("]","").split(", ")
                                shuffle(split_split_comment)
                                sentence_part_one = split_split_comment[0].replace("'","")

                            list_of_comment.append(sentence_part_one + " " + sentence_part_two)
                        need_to_comment_or_not.append(True)
                    else:
                        list_of_comment.append(".")
                        need_to_comment_or_not.append(False)

        list_of_good_comment = []

        for comment in list_of_comment:
            list_of_good_comment.append(comment.replace("@1@"," ").replace("@2@"," ").replace("@3@"," ").replace("@4@"," "))
        return list_of_tweet_url , list_of_account_to_follow , list_of_good_comment , need_to_comment_or_not , skip_this_giveaway

    def start(self) -> bool:
        """A function to start the bot"""
        print(f"Hello {self.username}")

        # dateT = datetime.now().strftime("%d/%m/%Y")
        # write_into_file("last_run.txt",dateT)
        # write_into_file("all_run.txt",dateT+"\n")

        last_run = print_file_content("last_run.txt")

        if len(last_run) > 3:
            target_date = datetime.strptime(last_run, "%d/%m/%Y")
            # Get today's date
            today = datetime.today()

            # Difference in days
            delta = target_date - today
            date_today = datetime.now().strftime("%d/%m/%Y")

            if int(str(delta).split(" ")[0]) <= -4:
                print("Account can run")
                write_into_file("last_run.txt",date_today)
                write_into_file("all_run.txt",date_today+"\n")

            else:
                print("Account already run not long time ago")
                return True

        first_time = False
        if self.login() is False:
            self.browser.close()
            return False

        #CHECK OTP APRES

        if self.otp_acc:
            if self.set_otp_code(self.otp_code) == False:
                self.browser.close()
                send_message_discord(f"OTP error on login for https://x.com/{self.username}",self.discord_dict["list_of_running_account_channel"])
                return False

        
        if self.is_login_good() is False:
            print(f"Bad login on {self.username}")
            send_message_discord(f"Bad login for https://x.com/{self.username}",self.discord_dict["list_of_running_account_channel"])
            self.browser.close()
            return False

        time.sleep(10)
        self.page.goto(TWEET_TO_SEE_AFTER_LOGIN)
        #url_to_test = "https://x.com/L_ThinkTank/status/2063274599328948555"

        self.random_stop()
        self.accept_cookie()
        time.sleep(30)
        send_message_discord(f"{self.username} is running https://x.com/{self.username}",self.discord_dict["list_of_running_account_channel"])
        if first_time:
            self.setup_passcode()
        else:
            self.check_dm()

        time.sleep(10)

        list_of_tweet_url , list_of_account_to_follow , list_of_comment , need_to_comment_or_not , skip_this_giveaway  = self.get_all_giveaway_data()
        print(list_of_tweet_url)
        print(list_of_account_to_follow)
        print(need_to_comment_or_not)
        print(list_of_comment)

        done_giveaway = []
        today_giveaway = self.is_giveaway_date_today()
        bad_giveaway = print_file_content("../txt_files_folder/ban_giveaway.txt").lower()

        if len(today_giveaway) > 0:
            for giv in today_giveaway:
                print(f"Giveaway to redo today: {giv}")
                if giv not in bad_giveaway:
                    self.unlike_a_tweet(giv)
                    self.like_a_tweet(giv)
                    self.unretweet_a_tweet(giv,False)
                    self.retweet_a_tweet(giv,False)
                    done_giveaway.append(giv)
                    
        giveaway_done = print_file_content("giveaway_done.txt").lower().split("\n")    
        if len(list_of_account_to_follow) == 0:
            print("No giveaway found bye")
            return
        

        # FOLLOW PEOPLE PART 1

        if len(list_of_account_to_follow) > 1:
            split_list_nb = randint(1,len(list_of_account_to_follow) - 1)
        else:
            split_list_nb = 1
        
        for i , account in enumerate(list_of_account_to_follow):
            if i <= split_list_nb:
                print(f"User {i}/{len(list_of_account_to_follow)}")
                self.follow_an_account(account)
        
        # DO GIVEAWAY

        for i , giveaway in enumerate(list_of_tweet_url):
            print(f"Giveaway number {i}/{len(list_of_tweet_url)}")
            if giveaway.lower() not in giveaway_done and skip_this_giveaway[i] != True and giveaway.lower() not in done_giveaway and giveaway.lower() not in bad_giveaway:
                like = self.like_a_tweet(giveaway)
                retweet = self.retweet_a_tweet(giveaway,False)
                comment = True
                if need_to_comment_or_not[i]:
                    comment = self.comment_a_tweet(giveaway,list_of_comment[i],False)
                if like and retweet and comment:
                    write_into_file("giveaway_done.txt",giveaway.lower()+"\n")
                    done_giveaway.append(giveaway.lower())

        # FOLLOW PEOPLE PART 2

        for i , account in enumerate(list_of_account_to_follow):
            if i > split_list_nb:
                print(f"User {i}/{len(list_of_account_to_follow)}")
                self.follow_an_account(account)

        # RT RANDOM TWEET

        all_random_rt = print_file_content("../txt_files_folder/recent_random_rt.txt").lower().split("\n")
        random_rt_done = print_file_content("random_rt_done.txt").lower().split("\n")
        

        list_of_random_rt_tweet = []
        for random_rt in all_random_rt:
            split_random_rt = random_rt.split(" ")
            if len(split_random_rt[0]) > 1:
                date = datetime.strptime(split_random_rt[1].replace(":","-"), '%Y-%m-%d').date()
                delta = self.today_date - date
                if delta.days <= 6:
                    list_of_random_rt_tweet.append(split_random_rt[0])
        
        shuffle(list_of_random_rt_tweet)
        
        for random_rt in list_of_random_rt_tweet:
            if random_rt.lower() not in random_rt_done:
                if self.retweet_a_tweet(random_rt):
                    write_into_file("random_rt_done.txt",random_rt.lower()+"\n")


        # self.retweet_a_tweet("https://x.com/L_ThinkTank/status/2063274599328948555")
        # self.unretweet_a_tweet("https://x.com/L_ThinkTank/status/2063274599328948555")
        # self.retweet_a_tweet("https://x.com/L_ThinkTank/status/2063274599328948555",False)
        # self.follow_an_account("L_ThinkTank")
        # self.unfollow_an_account("L_ThinkTank")
        # self.follow_an_account("L_ThinkTank")
        print(f"Giveaway done on {self.username}")
        self.browser.close()
        return True
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
        
        current_directory = os.getcwd()
        currentDir = current_directory.split("\\")[-1]
        
        
        self.username = self.data2["account_username"][0]
        if len(self.username) < 3:
            self.username = currentDir
        self.password = self.data2["account_password"][0]
        self.today_date = datetime.now().date()

        self.browser = launch_persistent_context(user_data_dir=f"./{self.username}",geoip=True,headless=False,humanize=True)
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
                print(self.otp_acc,self.otp_code)
                break

        if self.username == "test_account":
            self.username = currentDir

    def login(self):
        """A function to login to your account"""
        try:
            self.page.goto(TWITTER_LOGIN_PAGE_URL)
            
            self.page.locator(USERNAME_OR_EMAIL_ATTRIBUTE).fill(self.username)
            self.page.locator(BUTTON_SUBMIT_ATTRIBUTE).click()
            #self.random_stop()
            self.page.locator(PASSWORD_ATTRIBUTE).fill(self.password)

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
            
            
    def like_a_tweet(self,url,print_error=False) -> bool:
        """A function to like a tweet"""
        try:
            self.page.goto(url)
            if print_error:
                time.sleep(10)
            time.sleep(randint(1,3))
            self.page.locator(LIKE_A_TWEET_ATTRIBUTE).click()
            #self.random_stop()
            time.sleep(randint(1,10))
            write_into_file("../../list_of_giveaway_done_today.txt",url+"\n")
            write_into_file("../../list_of_all_giveaway_done.txt",url+"\n")
            
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.like_a_tweet(url)

            if print_error:
                traceback.print_exc()
            return False
    def unlike_a_tweet(self,url) -> bool:
        """A function to unlike a tweet"""
        try:
            self.page.goto(url)
            self.page.locator(UNLIKE_A_TWEET_ATTRIBUTE).click()
            #self.random_stop()
            time.sleep(randint(1,10))
            
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.unlike_a_tweet(url)

            if self.print_error:
                traceback.print_exc()
            
            return False

    def retweet_a_tweet(self,url,load_page=True,print_error=False,random_rt=False) -> bool:
        """A function to retweet a tweet"""
        try:
            if random_rt and url.lower() in print_file_content("random_rt_done.txt").lower().split("\n"):
                return True
            if load_page:
                self.page.goto(url)
            self.page.locator(RETWEET_A_TWEET_ATTRIBUTE).click()
            time.sleep(randint(1,5))
            self.page.locator(RETWEET_CONFIRM_ATTRIBUTE).click()
            #self.random_stop()
            time.sleep(randint(1,10))
            
            try:
                self.page.locator(UNLOCK_MORE_BUTTON_ATTRIBUTE).click(timeout=2500)
            except:
                pass
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.retweet_a_tweet(url,load_page)
            if print_error:
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

            #self.random_stop()
            time.sleep(randint(1,10))
            
            return True
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.unretweet_a_tweet(url,load_page)

            if self.print_error:
                traceback.print_exc()
            
            return False
    def comment_a_tweet(self,url,text,load_page=True,print_error=False) -> bool:
        """A function to comment a tweet"""
        try:
            if url.lower() in print_file_content("giveaway_done.txt").lower().split("\n"):
                return True
            if len(text) == 0:
                return True
            if load_page:
                self.page.goto(url)
            #self.page.locator(COMMENT_A_TWEET_ATTRIBUTE).click()
            self.page.locator(COMMENT_TEXTBOX_ATTRIBUTE).click()
            self.page.locator(COMMENT_A_TWEET_ATTRIBUTE).fill("   " + text.replace("\n"," "))
            time.sleep(randint(1,5))
            self.page.locator(POST_A_TWEET_BUTTON_ATTRIBUTE).click()
            #self.random_stop()
            time.sleep(randint(10,15))
            return True

        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.comment_a_tweet(url,text,load_page)

            if print_error:
                traceback.print_exc()
            return False

    def comment_a_tweet_with_a_picture(self,url,text,filepath,load_page=True,print_error=False) -> bool:
        """A function to comment a tweet"""
        try:
            if len(text) == 0:
                return True
            if load_page:
                self.page.goto(url)

            time.sleep(2)
            self.page.locator(COMMENT_TEXTBOX_ATTRIBUTE).click()
            time.sleep(5)
            self.page.set_input_files(COMMENT_A_POST_ATTRIBUTE, filepath)
            time.sleep(5)
            time.sleep(randint(1,15))

            #self.page.locator(COMMENT_A_TWEET_ATTRIBUTE).click()
            self.page.locator(COMMENT_A_TWEET_ATTRIBUTE).fill("   " + text.replace("\n"," "))
            time.sleep(randint(1,5))
            time.sleep(5)


            self.page.locator(POST_A_TWEET_BUTTON_ATTRIBUTE).click()
            #self.random_stop()
            time.sleep(randint(10,15))
            return True

        except Exception as e:
            traceback.print_exc()
            
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.comment_a_tweet(url,text,load_page)

            if print_error:
                traceback.print_exc()
            return False

    def follow_an_account(self,account,print_error=False) -> bool:
        """A function to follow an account"""
        try:
            
            if account.lower() in print_file_content("../txt_files_folder/ban_account.txt").lower() or account.lower() == self.username:
                return True
            
            if account.lower() in self.list_of_account_you_follow:
                print(f"SKIP {account} you already follow it")
                return True
            
            your_account_to_follow = print_file_content("../../all_acc.txt").split("\n")
            if account.lower() in your_account_to_follow:
                if randint(1,10) != 10:
                    return True
            
            self.page.goto(f"https://x.com/{account}")
            # try:
            #     self.page.locator(UNFOLLOW_AN_ACCOUNT_ATTRIBUTE).wait_for(timeout=3000)
            #     print(f"You already follow {account}")
            #     return True
            # except:
            #     pass
            self.page.locator(FOLLOW_AN_ACCOUNT_ATTRIBUTE).click()
            try:
                self.page.locator(UNFOLLOW_AN_ACCOUNT_CONFIRM_ATTRIBUTE).wait_for(timeout=3000)
                print(f"You already follow {account}")
                return True
            except:
                pass


            print(f"You have followed another account: {account}")
            self.random_stop()
            self.random_stop()
            self.random_stop()
            
            write_into_file("list_of_account_you_follow.txt",account.lower()+"\n")
            return True

        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.follow_an_account(account)
            
            if account.lower() not in print_file_content("follow_error.txt").lower():
                write_into_file("follow_error.txt",account+"\n")
            
            if print_error:
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

            if self.print_error:
                traceback.print_exc()
            
            return False

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

    def setup_passcode(self,fast=False) -> bool:
        """A function that will create a passcode"""
        try:
            self.page.goto(DM_PAGE)
            if fast is False:
                try:
                    self.page.locator(CREATE_A_PASSCODE_ATTRIBUTE).click()
                    time.sleep(randint(1,5))
                except:
                    pass
            self.page.locator(CODEPASS_TEXTBOX_ATTRIBUTE).click()
            time.sleep(randint(1,5))

            self.page.locator(CODEPASS_TEXTBOX_ATTRIBUTE).fill("2001")
            time.sleep(randint(1,5))

            try:
                self.page.locator(CODEPASS_TEXTBOX_ATTRIBUTE).fill("2001")
            except:
                pass

            return True

            # try:
            #     self.page.locator(CODEPASS_TEXTBOX_ATTRIBUTE).fill("2001")
            # except:
            #     pass

        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
            if self.print_error:
                traceback.print_exc()
            
            return False

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

    def is_passcode_for_dm_needed(self)  -> bool:
        """A function that check if passcode for dm is needed"""
        try:
            self.page.goto(DM_PAGE)
            time.sleep(randint(1,5))
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
                else:
                    self.page.goto(DM_PAGE)

                time.sleep(15)
                self.page.screenshot(path="screenshot.png")
                
                send_message_discord_with_pic(f"{self.username} got a new DM check it out!",self.discord_dict["new_dm_channel"])
                time.sleep(3)
            except:
                return None
        except Exception as e:
            if "Page.goto: net::ERR_INTERNET_DISCONNECTED " in str(e):
                time.sleep(60 * 15)
                self.check_dm()
            #traceback.print_exc()
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
            accountListToTag = print_file_content("../../account_to_tag.txt").split("\n")
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
            try:
                return accounts_to_tag[0]
            except:
                accounts_to_tag = ["@Inoxtag " , "@Mediavenir " , "@Arkunir"]
                return accounts_to_tag[0]
            
        if nb == 2:
            try:
                return accounts_to_tag[0]+" "+accounts_to_tag[1]
            except:
                accounts_to_tag = ["@Inoxtag " , "@Mediavenir " , "@Arkunir"]
                return accounts_to_tag[0]+" "+accounts_to_tag[1]

        try:    
            return " ".join(accounts_to_tag)
        except:
            accounts_to_tag = ["@Inoxtag " , "@Mediavenir " , "@Arkunir"]
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

    def start(self,max_retry=0) -> bool:
        """A function to start the bot"""
        print(f"Hello {self.username}")

        # dateT = datetime.now().strftime("%d/%m/%Y")
        # write_into_file("last_run.txt",dateT)
        # write_into_file("all_run.txt",dateT+"\n")

        
        last_run = print_file_content("last_run.txt")
        all_run = print_file_content("all_run.txt")
        date_today = datetime.now().strftime("%d/%m/%Y")
        first_time = False
        first_time_dm = True
        
        if len(all_run) > 3:
            first_time_dm = False
        
        if len(last_run) > 3:
            target_date = datetime.strptime(last_run[0:10], "%d/%m/%Y")
            # Get today's date
            today = datetime.today()

            # Difference in days
            delta = target_date - today
            
            if int(str(delta).split(" ")[0]) <= -4:
                print("Account can run")
                reset_file("last_run.txt")
                write_into_file("last_run.txt",date_today)
                write_into_file("all_run.txt",date_today+"\n")

            else:
                if max_retry != 1 and len(print_file_content("giveaway_done.txt").lower().split("\n")) != 0:
                    print("Account already run not long time ago")
                    return True
                
            
        else:
            first_time = True
            reset_file("last_run.txt")
            write_into_file("last_run.txt",date_today)
            write_into_file("all_run.txt",date_today+"\n")

        if first_time:
            check_login = self.is_login_good()
            time.sleep(30)
            if check_login == False:
                if self.login() is False:
                    if max_retry == 0:
                        self.browser.close()
                        self.start(1)
                    else:
                        self.browser.close()
                        return False

                #CHECK OTP APRES

                if self.otp_acc:
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

            # self.login()
            # if self.is_login_good() is False:
            #     print(f"Bad login on {self.username}")
            #     send_message_discord(f"Bad login for https://x.com/{self.username}",self.discord_dict["list_of_login_error_channel"])
            #     self.browser.close()
            #     return False


        
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
        
        send_message_discord(f"{self.username} is running https://x.com/{self.username}",self.discord_dict["list_of_running_account_channel"])

        
        if first_time_dm:
            self.setup_passcode()
        else:
            self.check_dm()


        list_of_tweet_url , list_of_account_to_follow , list_of_comment , need_to_comment_or_not , skip_this_giveaway  = self.get_all_giveaway_data()
        print(list_of_tweet_url)
        print(list_of_account_to_follow)
        print(need_to_comment_or_not)
        print(list_of_comment)
        
        done_giveaway = []
        today_giveaway = self.is_giveaway_date_today()
        bad_giveaway = print_file_content("../txt_files_folder/ban_giveaway.txt").lower()
        giveaway_done = print_file_content("giveaway_done.txt").lower().split("\n")

        if len(today_giveaway) > 0:
            for giv in today_giveaway:
                print(f"Giveaway to redo today: {giv}")
                if giv not in bad_giveaway:
                    if giv in giveaway_done:
                        self.unlike_a_tweet(giv)
                        self.unretweet_a_tweet(giv,True)
                        self.random_stop()
                        self.like_a_tweet(giv)
                        self.retweet_a_tweet(giv,True)
                        self.random_stop()
                        done_giveaway.append(giv)



        write_into_file("../../list_of_all_run.txt",f"{self.username} {date_today}")
                
        if len(list_of_account_to_follow) == 0 and len(done_giveaway) == 0:
            print("No giveaway found bye")
            self.browser.close()
            return

        # FOLLOW ALL YOUR ACCOUNT
        try:
            if len(print_file_content("giveaway_done.txt").lower().split("\n")) >= 0:
                your_account_to_follow = print_file_content("../../all_acc.txt").split("\n")
                for i , account in enumerate(your_account_to_follow):
                    if account.lower() in print_file_content("../txt_files_folder/ban_account.txt").lower() or account.lower() == self.username or account.lower() in self.list_of_account_you_follow:
                        continue
                    print(f"Your own account {account} {i + 1}/{len(your_account_to_follow)}")
                    
                    follow = self.follow_an_account(account,False)
                    if follow is False:
                        self.follow_an_account(account,False)
        except:
            pass

        # FOLLOW PEOPLE PART 1

        if len(list_of_account_to_follow) > 1:
            split_list_nb = randint(1,len(list_of_account_to_follow) - 1)
        else:
            split_list_nb = 1
        


        check_login = self.is_login_good()
        time.sleep(randint(20,40))
        if check_login == False:
            send_message_discord(f"{self.username} got locked during the run https://x.com/{self.username}",self.discord_dict["account_locked_during_run"])
            print(f"{self.username} got locked during the run 1")
            self.browser.close()
            return False
        
        shuffle(list_of_account_to_follow)
        for i , account in enumerate(list_of_account_to_follow):
            if i <= split_list_nb:
                if account.lower() in print_file_content("../txt_files_folder/ban_account.txt").lower() or account.lower() == self.username or account.lower() in self.list_of_account_you_follow:
                    continue
                
                print(f"User {account} {i + 1}/{len(list_of_account_to_follow)}")
                follow = self.follow_an_account(account,False)
                if follow is False:
                    self.follow_an_account(account,False)




        check_login = self.is_login_good()
        time.sleep(randint(20,40))
        if check_login == False:
            send_message_discord(f"{self.username} got locked during the run https://x.com/{self.username}",self.discord_dict["account_locked_during_run"])
            print(f"{self.username} got locked during the run 2")
            self.browser.close()
            return False
        
        # DO GIVEAWAY
        shuffle_list = []
        for i in range(len(list_of_tweet_url)):
            shuffle_list.append(i)
        shuffle(shuffle_list)
        skip = 0
        for i , giveaway in enumerate(list_of_tweet_url):
            giveaway = list_of_tweet_url[shuffle_list[i]]
            if giveaway.lower() in giveaway_done or skip_this_giveaway[shuffle_list[i]] is True or giveaway.lower() in done_giveaway or giveaway.lower() in bad_giveaway:
                skip+=1

        giveaway_nb = 0
        

        comment_a_post_with_piture = False
        list_of_pic_giveaway = [
        ]
        for giveaway in list_of_pic_giveaway:
            if giveaway.lower() not in giveaway_done and comment_a_post_with_piture:
                try:
                    list_of_picture_filepath = r"C:\Users\sakin\Desktop\code\TwitterGiveawayBotV2\picture_path"
                    list_of_picture = os.listdir(list_of_picture_filepath)
                    shuffle(list_of_picture)
                    random_picture = rf"{list_of_picture_filepath}\{list_of_picture[0]}"
                    like = self.like_a_tweet(giveaway)
                    if like is False:
                        like = self.like_a_tweet(giveaway,False)


                    retweet = self.retweet_a_tweet(giveaway,False)
                    if retweet is False:
                        retweet = self.retweet_a_tweet(giveaway,True,False)

                    comment = True
                    comment = self.comment_a_tweet_with_a_picture(giveaway,"#CdiscountSoldes " , random_picture,True,False)
                    if comment is False:
                        time.sleep(randint(1,10))
                        comment = self.comment_a_tweet(giveaway,"#CdiscountSoldes Merci" ,True,False)

                    if like and retweet and comment:
                        write_into_file("giveaway_done.txt",giveaway.lower()+"\n")
                    
                except:
                    print("Comment a tweet with picture error")
                
        for i , giveaway in enumerate(list_of_tweet_url):
            giveaway = list_of_tweet_url[shuffle_list[i]]
            if giveaway.lower() not in giveaway_done and skip_this_giveaway[shuffle_list[i]] is not True and giveaway.lower() not in done_giveaway and giveaway.lower() not in bad_giveaway:
                giveaway_nb+=1
                print(f"Giveaway number {giveaway_nb}/{len(list_of_tweet_url) - skip} {giveaway}")
                like = self.like_a_tweet(giveaway)
                if like is False:
                    like = self.like_a_tweet(giveaway,False)


                retweet = self.retweet_a_tweet(giveaway,False)
                if retweet is False:
                    retweet = self.retweet_a_tweet(giveaway,True,False)

                comment = True
                if need_to_comment_or_not[shuffle_list[i]]:
                    comment = self.comment_a_tweet(giveaway,list_of_comment[shuffle_list[i]],False)
                    if comment is False:
                        comment = self.comment_a_tweet(giveaway,list_of_comment[shuffle_list[i]],True,False)

                if like and retweet and comment:
                    write_into_file("giveaway_done.txt",giveaway.lower()+"\n")
                    done_giveaway.append(giveaway.lower())
                self.random_stop()
        # FOLLOW PEOPLE PART 2

        for i , account in enumerate(list_of_account_to_follow):
            if i > split_list_nb:
                if account.lower() in print_file_content("../txt_files_folder/ban_account.txt").lower() or account.lower() == self.username or account.lower() in self.list_of_account_you_follow:
                    continue
                
                print(f"User {account} {i + 1}/{len(list_of_account_to_follow)}")
                follow = self.follow_an_account(account,False)
                if follow is False:
                    self.follow_an_account(account,False)

        # RT RANDOM TWEET

        all_random_rt = print_file_content("../txt_files_folder/recent_random_rt.txt").lower().split("\n")
        random_rt_done = print_file_content("random_rt_done.txt").lower().split("\n")

        list_of_random_rt_tweet = []
        # for random_rt in all_random_rt:
        #     split_random_rt = random_rt.split(" ")
        #     if len(split_random_rt[0]) > 1:
        #         date = datetime.strptime(split_random_rt[1].replace(":","-"), '%Y-%m-%d').date()
        #         delta = self.today_date - date
        #         if delta.days <= 6:
        #             list_of_random_rt_tweet.append(split_random_rt[0])

        for random_rt in all_random_rt:
            split_random_rt = random_rt.split(" ")
            if len(split_random_rt[0]) > 1:
                list_of_random_rt_tweet.append(split_random_rt[0])

        shuffle(list_of_random_rt_tweet)

        check_login = self.is_login_good()
        time.sleep(randint(20,40))
        if check_login == False:
            send_message_discord(f"{self.username} got locked during the run https://x.com/{self.username}",self.discord_dict["account_locked_during_run"])
            print(f"{self.username} got locked during the run 3")
            self.browser.close()
            return False
        
        rt_done_list = []
        if len(done_giveaway) <= 4:
            nb = randint(10,15)
            if nb < len(list_of_random_rt_tweet):
                list_of_random_rt_tweet = list_of_random_rt_tweet[0:nb]
        elif len(done_giveaway) < 10:
            nb = randint(20,30)
            if nb < len(list_of_random_rt_tweet):
                list_of_random_rt_tweet = list_of_random_rt_tweet[0:nb]
    
        for i , random_rt in enumerate(list_of_random_rt_tweet):
            if random_rt.lower() not in random_rt_done and random_rt not in rt_done_list:
                if self.retweet_a_tweet(random_rt,True,False,True):
                    write_into_file("random_rt_done.txt",random_rt.lower()+"\n")
                    print(f"Random retweet done {i + 1}/{len(list_of_random_rt_tweet)} {random_rt}")
                    rt_done_list.append(random_rt)


        # self.retweet_a_tweet("https://x.com/L_ThinkTank/status/2063274599328948555")
        # self.unretweet_a_tweet("https://x.com/L_ThinkTank/status/2063274599328948555")
        # self.retweet_a_tweet("https://x.com/L_ThinkTank/status/2063274599328948555",False)
        # self.follow_an_account("L_ThinkTank")
        # self.unfollow_an_account("L_ThinkTank")
        # self.follow_an_account("L_ThinkTank")
        print(f"Giveaway done on {self.username}")
        try:
            write_into_file("../../all_account_run.txt",self.username + " "  + date_today + "\n")
        except:
            pass
        self.browser.close()
        return True

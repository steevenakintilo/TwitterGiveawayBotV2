# pylint: disable-all


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from os import system
import time
import os.path

import pickle
from selenium.webdriver.common.action_chains import ActionChains

from search import search_tweet_for_better_rt ,  get_giveaway_url
from selenium.webdriver.common.by import By
from get_tweet import *
import traceback

from random import randint

import time
import traceback

from selenium.webdriver import ActionChains

import pyperclip
from discord_webhook import DiscordWebhook
import yaml
import json

with open("../../configuration.yml", "r") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
 

class Scraper:
    
    wait_time = 5
    headless = data["headless"]
    options = webdriver.ChromeOptions()
    
    
    #proxy_server_url = "185.199.229.156"
    #options.add_argument(f'--proxy-server={proxy_server_url}')
    

    #options.add_argument('headless')
    options.add_argument("--log-level=3")  # Suppress all logging levels
    
    driver = webdriver.Chrome(options=options)  # to open the chromedriver    
    #options = webdriver.FirefoxOptions()
    #options.headless = False

    #driver = webdriver.Firefox(options=options)
    

    


def get_who_to_follow(S,text,username):

    try:
        a = username
        b = text
        c = list_of_account_to_follow(a ,b.strip().replace("\n",""))
        c = c.replace(",","").strip()
        c = c.split(" ")
        d = []
        for elem in c:
            if elem.lower() not in d:
                d.append(elem.lower())
        return(d)
    except:
        print("Bref userrrr")
        return("")



def save_coockie(selenium_session,nb):
    pickle.dump(selenium_session.driver.get_cookies(), open(f"cookies0.pkl", "wb"))

def print_pkl_info(nb):
    file_path = f"cookies0.pkl"
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return (data) 

def print_file_info(path):
    f = open(path, 'r',encoding="utf-8")
    content = f.read()
    f.close()
    return(content)

def send_message_discord(msg,url_name):
    try:
        webhook = DiscordWebhook(url=url_name, content=msg)
        response = webhook.execute()
    except:
        pass


def reset_file(path):  
    try:
        f = open(path, "w")
        f.write("")    
        f.close  
    except:
        pass

def is_user_valid(user):
    valid_char = "0123456789abcdefghijklmnopqrstuvwxyz_"
    for letter in user.lower():
        if letter not in user:
            return False
    return True

def main_one():
    with open("../../configuration.yml", "r",encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    

    with open("../../discord_data_dict.json", "r", encoding="utf-8") as file:
        discord_dict = json.load(file)

    try:
        send_message_discord(f"Hello there!",discord_dict["list_of_giveaway_channel"])
    except:
        pass
   
    account_num = 0
    tweet_txt = []
    crash_follow = []
    t_follow = []
    tt_follow = []
    tttt_follow = []
    t_comment_or_not , t_full_comment, t_follows = [] , [] , []
    
    account_num = 0
    ELON_MUSK = 55

    account_num+=1
    S = Scraper()
    try:
        ck = print_pkl_info(0)
        print(len(str(ck)) , " len de ck")
        
        if len(str(ck)) > ELON_MUSK:
            username_info = data["account_username"]
            S.driver.get("https://x.com")
            
            cookies = pickle.load(open(f"cookies{0}.pkl","rb"))
            for cookie in cookies:
                S.driver.add_cookie(cookie)
            time.sleep(0.2)
            time.sleep(S.wait_time)    
            #accept_coockie(S)
            time.sleep(S.wait_time)    
        
        else:
            a = 10 / 0
        #print("Connecting to " + str(username_info[i]))
        time.sleep(1)
    except Exception as e:
        print("Run python twt_cookies.py to save cookie for the account!")
        return
        traceback.print_exc()
        try:
            from twt_cookies import main_ckk
            xxxz = main_ckk()
            return []
        except:
            return []

    

    S.driver.refresh()
    time.sleep(5)
    
    skip_giveaway = False
    if skip_giveaway == False:
        tweet_from_url , tweet_txt , tweet_user = get_giveaway_url(S)  
        max_nb = 50
        if len(tweet_from_url) >= max_nb:
            tweet_from_url , tweet_txt , tweet_user = get_giveaway_url(S,True)

        for d in range(len(tweet_from_url)):
            time.sleep(1)
            try:
                crash_follow.append(tweet_user[d])
                for g in get_who_to_follow(S,tweet_txt[d],tweet_user[d]):
                    tt_follow.append(g)
            except:
                print("caca follow")
        for tt in tt_follow:
            t_follow.append(tt)

        
        try:
            t_follows.remove("")
        except:
            pass
        for t in t_follows:
            if t != "":
                t_follow.append(t.replace(" ",""))
        
        t_follow = list(dict.fromkeys(t_follow))
        

        for c in t_follow:
            if c.lower() not in tttt_follow and len(c) < 16 and len(c) > 3:
                tttt_follow.append(c.lower().replace("@",""))
        
        print(tttt_follow)
        today_date = datetime.now().strftime("%Y:%m:%d")

        for user_to_follow in tttt_follow:
            if is_user_valid(user_to_follow):
                write_into_file("../txt_files_folder/user_to_follow.txt",f"{user_to_follow} {today_date}"+"\n")
        

        not_found = 0
        for tweet in tweet_from_url:
            #rsend_message_discord(tweet,55)
            
            if tweet in print_file_info("../txt_files_folder/all_giveaway.txt"):
                not_found +=1
                continue
        
        #rsend_message_discord("I'm skyler white yooo",55)
        try:
            if not_found == len(tweet_from_url):
                send_message_discord(f"No giveaway found today",discord_dict["list_of_giveaway_channel"])
            else:
                send_message_discord(f"List of giveaway found {len(tweet_from_url) - not_found} today {today_date}",discord_dict["list_of_giveaway_channel"])
        except:
            pass
        for tweet in tweet_from_url:
            #rsend_message_discord(tweet,55)
            
            if tweet in print_file_info("../txt_files_folder/all_giveaway.txt"):
                continue
            
            write_into_file("../txt_files_folder/all_giveaway.txt",f"{tweet} {today_date}"+"\n")
            try:
                send_message_discord(tweet,discord_dict["list_of_giveaway_channel"])
            except:
                pass
        
        t_comment_or_not , t_full_comment, blabla = giweaway_from_url_file(tweet_txt,crash_follow,S)
        
        for comment_or_not , full_comment in zip(t_comment_or_not,t_full_comment):
            write_into_file("../txt_files_folder/all_comment.txt",f"{comment_or_not}##@@##{full_comment}##@@##{today_date}"+"\n")



    if skip_giveaway is False:
        time.sleep(120)
    skip_random_rt = False
    reset_file("../txt_files_folder/recent_random_rt.txt")
    try:
        
        rt_already_in = []
        with open("../../random_rt_theme.yml", "r") as file:
            random_rt_theme_data = yaml.load(file, Loader=yaml.FullLoader)

        list_of_theme = ["general","foot","music"]
        list_of_theme_yml = [
            random_rt_theme_data["general_rt"],
            random_rt_theme_data["foot_rt"],
            random_rt_theme_data["music_rt"]
        ]
        today_date = datetime.now().strftime("%Y:%m:%d")
        for theme , yml_theme in zip(list_of_theme,list_of_theme_yml):
            rt_url = search_tweet_for_better_rt(S,yml_theme)
            for random_rt in rt_url:
                if f"{random_rt} {theme}" not in rt_already_in:
                    
                    
                    write_into_file("../txt_files_folder/all_random_rt.txt",f"{random_rt} {today_date}"+"\n")
                    #write_into_file("../txt_files_folder/all_random_rt_theme.txt",f"{random_rt} {today_date} {theme}"+"\n")
                    write_into_file("../txt_files_folder/recent_random_rt.txt",f"{random_rt} {today_date} {theme}"+"\n")
                    rt_already_in.append(f"{random_rt} {theme}")    
        
        
    
    except:
        if skip_random_rt == False and data["random_retweet_and_tweet"]:
            today_date = datetime.now().strftime("%Y:%m:%d")
            rt_url = search_tweet_for_better_rt(S)


            reset_file("../txt_files_folder/recent_random_rt.txt")
            for random_rt in rt_url:
                write_into_file("../txt_files_folder/all_random_rt.txt",f"{random_rt} {today_date}"+"\n")
                write_into_file("../txt_files_folder/recent_random_rt.txt",f"{random_rt} {today_date}"+"\n")
        
    print("End of the program")



#time.sleep(600)
main_one()

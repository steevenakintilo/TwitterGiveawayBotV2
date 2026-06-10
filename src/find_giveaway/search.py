from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from datetime import datetime, timedelta, date
from get_tweet import *
from random import shuffle
import os
import traceback
import time
from discord_webhook import DiscordWebhook
import emoji
import re

import pyperclip

def remove_emojie(text):
    return emoji.replace_emoji(text, replace='')



def remove_days(days_to_remove):
    if days_to_remove < 0:
        days_to_remove = 0
    
    date_format = "%Y-%m-%d"
    today_date = datetime.now().strftime("%Y-%m-%d")
    current_date = datetime.strptime(today_date, date_format)
    new_date = current_date - timedelta(days=days_to_remove)
    
    return(new_date.strftime(date_format))

def parse_number(num):
    num = str(num)
    if "B" in num:
        if "." in num:
            num  = num.replace(".","").replace("B","")
            num  = num + "00000000"
            
        else:
            num = num.replace("B","")
            num  = num + "000000000"
            
    elif "M" in num:
        if "." in num:
            num  = num.replace(".","").replace("M","")
            num  = num + "00000"

        else:
            num = num.replace("B","")
            num  = num + "000000"
    
    elif "K" in num:
        if "." in num:
            num  = num.replace(".","").replace("K","")
            num = num + "00"
        else:
            num = num.replace("K","")
            num = num + "000"
    else:
        if "." in num:
            num  = num.replace(".","")
    
    if "," in num:
        num = num.replace(",","")
    
    return int(num)

def convert_string_to_date(date_string):
    original_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    new_date = original_date + timedelta(hours=2)
    return (new_date)

def are_last_x_elements_same(lst,x):
    lst_2 = []
    if len(lst) < x:
        return False
    if len(lst) >= x:
        lst.reverse()
        for i in range(0,x):
            l = lst[i]
            if l not in lst_2 and len(lst_2) != 0:
                return False
            else:
                lst_2.append(l)
    return True

def check_elem_on_a_list(elem_, list_):
    return next((l for l in list_ if elem_ in l.lower()), elem_)


def get_tweet_info(selenium_session,url):
    tweet_info_dict = {"username":"",
    "text":"",}

    try:
        selenium_session.driver.set_page_load_timeout(15)
        selenium_session.driver.get(url)
        user_tweet = url.split("/")[3]
        
        time.sleep(0.02)    
        #selenium_session.driver.refresh()
        time.sleep(0.02)
    
        element = WebDriverWait(selenium_session.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')))
        tweet_info = selenium_session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
        pos = 0
        for i in range(len(tweet_info)):
            r = tweet_info[i]
            if url.split("x.com")[1] in str(r.get_attribute("outerHTML")):
                pos = i
                break
        
        element = WebDriverWait(selenium_session.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))        
        
        print("")
        
        _tweet_data = selenium_session.driver.find_elements(By.CSS_SELECTOR,'[data-testid="tweet"]')
        _tweet_text = selenium_session.driver.find_elements(By.CSS_SELECTOR,'[data-testid="tweetText"]')
        
        tweet_data = str(_tweet_data[pos].text).split("\n")
        tweet_text = str(_tweet_text[pos].text)
        time.sleep(0.4)
        return (tweet_text)

    except Exception as e:
        if "net::ERR_NAME_NOT_RESOLVED" in str(e):
            print("Wifi error sleeping 3 minutes")

            time.sleep(300)
            return ("WIFI")

        try:
            element = WebDriverWait(selenium_session.driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetText"]')))
            return element.text
        except:
            print("Bref tweet info")
            return False
        print("Bref tweet info")
        #traceback.print_exc()
        #selenium_session.driver.refresh()
        return (False)

def get_tweet_nb_of_rt(selenium_session,url):
    tweet_info_dict = {"username":"",
    "text":"",}

    try:
        selenium_session.driver.set_page_load_timeout(15)
        selenium_session.driver.get(url)
        user_tweet = url.split("/")[3]
        
        time.sleep(0.02)    
        #selenium_session.driver.refresh()
        time.sleep(0.02)
    
        element = WebDriverWait(selenium_session.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')))
        tweet_info = selenium_session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
        pos = 0
        for i in range(len(tweet_info)):
            r = tweet_info[i]
            if url.split("x.com")[1] in str(r.get_attribute("outerHTML")):
                pos = i
                break
        
        element = WebDriverWait(selenium_session.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="retweet"]')))  

        element = selenium_session.driver.find_elements(By.CSS_SELECTOR,'[data-testid="retweet"]')

        nb_of_rt = element[pos].text
        print("")
        
        time.sleep(0.4)
        return (nb_of_rt)

    except Exception as e:
        if "net::ERR_NAME_NOT_RESOLVED" in str(e):
            print("Wifi error sleeping 3 minutes")

            time.sleep(300)
            return ("WIFI")
        #traceback.print_exc()
        #selenium_session.driver.refresh()
        return (0)

def search_tweet(selenium_session,query="hello",nb_of_tweet_to_search=10,sss=0):
    list_of_tweet_url = []
    selenium_data = []
    list_of_tweet_url_ = []
    list_len = []
    data_list = []
    text_list = []
    #url_from_file = print_file_info("url.txt").split("\n")
    tweets_url = []
        
    tweet_info_dict = {"username":"",
    "text":"",
    "id":0,
    "url":"",
    "date":"",
    "like":0,
    "retweet":0,
    "reply":0,}
    p = '"'
    nb = 0
    error_list = 0
    try:
        
        selenium_session.driver.set_page_load_timeout(15)
        selenium_session.driver.get("https://x.com/explore")
        
        run  = True
        p = '"'
        time.sleep(5)
        

        try:
            element = WebDriverWait(selenium_session.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="SearchBox_Search_Input"]')))
            input_box = selenium_session.driver.find_element(By.CSS_SELECTOR, '[data-testid="SearchBox_Search_Input"]')
        
        except:
            selenium_session.driver.refresh()
            time.sleep(10)
            input_box = selenium_session.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/form/div[1]/div/div/div/div/div[2]/div/input')
        
        input_box.click()
        input_box.send_keys(query)
        input_box.send_keys(Keys.ENTER)
        time.sleep(5)
        
        nb_of_tweet_to_search = 99

        try:
            current_url = selenium_session.driver.current_url
            rdz = selenium_session.driver.current_url
            selenium_session.driver.get(current_url+"&f=live")
        except:
            print("current url not here")
        time.sleep(5)
        # 200 180 pour les erreur
        # if nb_of_tweet_to_search > 100:
        #     selenium_session.driver.get(current_url+"&f=live")
        #     time.sleep(3)
        while run:
            try:
                element = WebDriverWait(selenium_session.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
            except:
                print("error searching tweet sleep for 30 sec")
                time.sleep(5)
                try:
                    selenium_session.driver.get(current_url+"&f=live")
                    time.sleep(5)
                    selenium_session.driver.refresh()
                    time.sleep(5)
                    element = WebDriverWait(selenium_session.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
                except:
                    print("error searching tweet even after refresh")
                    return(data_list)
            tweets_info = selenium_session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
            tweets_text = selenium_session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')
            last_tweet = tweets_info[len(tweets_info) - 1]
            for tweet_info, tweet_text in zip(tweets_info, tweets_text):
                if len(data_list) >= nb_of_tweet_to_search:
                    run = False
                if are_last_x_elements_same(list_len,250) == True:
                    run = False
                if error_list > 230:
                    print("bye")
                    run = False
                list_len.append(len(data_list))
                
                if tweet_info not in selenium_data:
                    try:
                        lower_data = str(tweet_info.get_property('outerHTML')).lower()
                        splinter = "href=" + p + "/"
                        lower_data = lower_data.split(splinter)
                        user = lower_data[4]
                        user = user.split(p)
                        tweet_stuff = user[0]
                        tweet_link = "https://x.com/" + tweet_stuff
                        user = tweet_stuff.split("/")[0]
                        tweet_link = tweet_link.replace("/analytics","")
                        text_ = tweet_text.text
                        
                        if len(text_) > 150:
                            text_ = "ok"
                        
                        if "/status" in tweet_link:
                            get_date = str(str(str(str(str(tweet_info.get_property('outerHTML')).lower()).split("datetime")[1]).split(" ")[0]).split(".000z")[0]).replace("t"," ").replace("=","")
                            tweet_info_dict = {"username":user,"text":text_,"id":int(str(tweet_link.split("status/")[1]).replace("/photo/1","")),"url":tweet_link,"date":str(convert_string_to_date(get_date.replace(p,""))),}
                            data_list.append(tweet_info_dict)
                            #print("list len ", len(list_of_tweet_url))
                        selenium_data.append(tweet_info)
                        selenium_session.driver.execute_script("arguments[0].scrollIntoView();", last_tweet)
                        time.sleep(0.030)
                    except:
                        try:
                            lower_data = str(tweet_info.get_property('outerHTML')).lower()
                            splinter = "href=" + p + "/"
                            lower_data = lower_data.split(splinter)
                            user = lower_data[5]
                            user = user.split(p)
                            tweet_stuff = user[0]
                            tweet_link = "https://x.com/" + tweet_stuff
                            user = tweet_stuff.split("/")[0]
                            text_ = tweet_text.text
                            
                            if len(text_) > 150:
                                text_ = "ok"
                        
                            if tweet_link[len(tweet_link) - 1] in "0123456789" and "status" in tweet_link:
                                get_date = str(str(str(str(str(tweet_info.get_property('outerHTML')).lower()).split("datetime")[1]).split(" ")[0]).split(".000z")[0]).replace("t"," ").replace("=","")
                                tweet_info_dict = {"username":user,"text":text_,"id":int(str(tweet_link.split("status/")[1]).replace("/photo/1","")),"url":tweet_link,"date":str(convert_string_to_date(get_date.replace(p,""))),}
                                data_list.append(tweet_info_dict)
                                list_of_tweet_url.append(tweet_link)
                            
                            selenium_data.append(tweet_info)                        
                            selenium_session.driver.execute_script("arguments[0].scrollIntoView();", last_tweet)
                            time.sleep(0.030)
                        except Exception as e:
                            if nb_of_tweet_to_search > 100:
                                #print("caca erreur")
                                error_list+=1
                                selenium_session.driver.execute_script("window.scrollBy(0, 10);")
                            time.sleep(0.1)

                else:
                    if nb_of_tweet_to_search > 100:    
                        #print("caca not here " , error_list)
                        error_list+=1
                        selenium_session.driver.execute_script("window.scrollBy(0, 500);")
        
        if len(data_list) > nb_of_tweet_to_search:
            for i in range(0,nb_of_tweet_to_search):
                list_of_tweet_url_.append(data_list[i])
            return(list_of_tweet_url_)

        else:
            return (data_list)
    except Exception as e:
        if "net::ERR_NAME_NOT_RESOLVED" in str(e):
            print("Wifi error sleeping 3 minutes")

            time.sleep(300)
        print("Error searching " + query + " tweet")
        time.sleep(3)
        return(data_list)

def send_message_discord(msg):
    try:
        urls = "https://discord.com/api/webhooks/1194945640392835102/oqtcZlNwcTo-3DI-MV-mqTmKAeWFhiQoQmoLPRIjKLHeL7aqg33JQ7aONE-e6LPW22QL"
        webhook = DiscordWebhook(url=urls, content=msg)
        response = webhook.execute()
    except:
        pass

def sssend_message_discord(msg):
    try:
        urls = "https://discord.com/api/webhooks/1346210400978337832/JXAYC-fC-zYWUm2wAIGP5hmlPOr3zl92JgIJmf-DBqqsXOc3M21RIJP2X0SRJIC4lRrX"
        webhook = DiscordWebhook(url=urls, content=msg)
        response = webhook.execute()
    except:
        pass

def search_tweets(selenium_session,query="hello",nb_of_tweet_to_search=10,recent=False):
    start_time = time.time()  # Start the timer
    list_of_tweet_url = []
    selenium_data = []
    list_of_tweet_url_ = []
    list_len = []
    data_list = []
    text_list = []
    #url_from_file = print_file_info("url.txt").split("\n")
    tweets_url = []
    
    current_directory = os.getcwd()
    currentDir = current_directory.split("\\")[-1]
    username_info = currentDir 

    print("s " , username_info)
    tweet_info_dict = {"username":"",
    "text":"",
    "id":0,
    "url":"",
    "date":"",
    "like":0,
    "retweet":0,
    "reply":0,}
    p = '"'
    nb = 0
    idxxx = 0
    nbE = 77
    if "lang:fr à min_retweets:500" in query:
        print("fck kzn")
        nbE = 1500     
    try:
        
        selenium_session.driver.set_page_load_timeout(15)
        selenium_session.driver.get("https://x.com/explore")
        run  = True
        p = '"'
        time.sleep(5)
        element = WebDriverWait(selenium_session.driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="SearchBox_Search_Input"]')))
        input_box = selenium_session.driver.find_element(By.CSS_SELECTOR, '[data-testid="SearchBox_Search_Input"]')
        input_box.click()
        input_box.send_keys(query)
        input_box.send_keys(Keys.ENTER)
        time.sleep(5)
        error_counter = 0
        error_checker = []
        error_nb = 0
        indexer = -1

        if recent == True:
            current_url = selenium_session.driver.current_url
            selenium_session.driver.get(current_url+"&f=live")
            time.sleep(5)

        timeout = 150
        while run:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print("Timeout reached. Exiting search.")
                return data_list
            element = WebDriverWait(selenium_session.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))

            error_checker.append(element)
            for e in error_checker:
                if error_checker.count(e) >= nbE:
                    send_message_discord(f"{username_info}\n got rt problem with thise search: {query} \n Replace those words/account!!! \n +++++++")        
                    print("Idxxxx value " , idxxx)
                    return data_list
            tweets_info = selenium_session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
            tweets_text = selenium_session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')
            last_tweet = tweets_info[len(tweets_info) - 1]
            for tweet_info, tweet_text in zip(tweets_info, tweets_text):
                indexer+=1
                idxxx=1
                if len(data_list) >= nb_of_tweet_to_search:
                    run = False
                list_len.append(len(data_list))
                if are_last_x_elements_same(list_len,250) == True:
                    run = False
                if tweet_info not in selenium_data:
                    try:
                        lower_data = str(tweet_info.get_property('outerHTML')).lower()
                        splinter = "href=" + p + "/"
                        lower_data = lower_data.split(splinter)
                        user = lower_data[4]
                        user = user.split(p)
                        tweet_stuff = user[0]
                        tweet_link = "https://x.com/" + tweet_stuff
                        user = tweet_stuff.split("/")[0]
                        tweet_link = tweet_link.replace("/analytics","")
                        text_ = tweet_text.text
                        if len(text_) > 220:
                            text_ = "ok"
                        
                        if "/status" in tweet_link:
                            get_date = str(str(str(str(str(tweet_info.get_property('outerHTML')).lower()).split("datetime")[1]).split(" ")[0]).split(".000z")[0]).replace("t"," ").replace("=","")
                            tweet_info_dict = {"big_text":tweet_text.text , "username":user,"text":text_,"id":int(str(tweet_link.split("status/")[1]).replace("/photo/1","")),"url":tweet_link,"date":str(convert_string_to_date(get_date.replace(p,""))),}
                            data_list.append(tweet_info_dict)
                            #print("list len ", len(list_of_tweet_url))
                        selenium_data.append(tweet_info)
                        selenium_session.driver.execute_script("arguments[0].scrollIntoView();", last_tweet)
                        time.sleep(0.030)
                    except:
                        try:
                            lower_data = str(tweet_info.get_property('outerHTML')).lower()
                            splinter = "href=" + p + "/"
                            lower_data = lower_data.split(splinter)
                            user = lower_data[5]
                            user = user.split(p)
                            tweet_stuff = user[0]
                            tweet_link = "https://x.com/" + tweet_stuff
                            user = tweet_stuff.split("/")[0]
                            text_ = tweet_text.text
                                    
                            if len(text_) > 220:
                                text_ = "ok"
                        
                            if tweet_link[len(tweet_link) - 1] in "0123456789" and "status" in tweet_link:
                                get_date = str(str(str(str(str(tweet_info.get_property('outerHTML')).lower()).split("datetime")[1]).split(" ")[0]).split(".000z")[0]).replace("t"," ").replace("=","")
                                tweet_info_dict = {"big_text":tweet_text.text , "username":user,"text":text_,"id":int(str(tweet_link.split("status/")[1]).replace("/photo/1","")),"url":tweet_link,"date":str(convert_string_to_date(get_date.replace(p,""))),}
                                data_list.append(tweet_info_dict)
                                list_of_tweet_url.append(tweet_link)
                            
                            selenium_data.append(tweet_info)                        
                            selenium_session.driver.execute_script("arguments[0].scrollIntoView();", last_tweet)
                            time.sleep(0.030)
                        except Exception as e:
                            time.sleep(0.1)

        
        print("Idxxxx value " , idxxx)
        return (data_list)
    except Exception as e:
        if "net::ERR_NAME_NOT_RESOLVED" in str(e):
            print("Wifi error sleeping 3 minutes")

            time.sleep(300)
        
        print("Error searching " + query + " tweet")
        time.sleep(3)
        print("Idxxxx value " , idxxx)
        return(data_list)



def comment_a_tweet(S,url,text):
    stop = True
    while stop:
        
        try:
            S.driver.set_page_load_timeout(15)
            S.driver.get(url)
            time.sleep(0.001)
            pos = 0
            try:
                element = WebDriverWait(S.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')))
            except:
                print("cell innder div not here")
                time.sleep(1)
                
            tweet_info = S.driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
            for i in range(len(tweet_info)):
                r = tweet_info[i]
                if url.split("x.com")[1] in str(r.get_attribute("outerHTML")):
                    pos = i
                    break
            
            try:
                element = WebDriverWait(S.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="reply"]')))
            except:
                
                print("reply div not here")
                time.sleep(1)

            comment_button = S.driver.find_elements(By.CSS_SELECTOR, '[data-testid="reply"]')
            time.sleep(0.25)
            #comment_button[pos].click()
            try:
                S.driver.execute_script("arguments[0].click();", comment_button[pos])
            except:
                try:
                    S.driver.execute_script("arguments[0].click();", comment_button[0])
                    print("comment bug hehehe 1")
                except:
                    try:
                        comment_button = S.driver.find_element(By.CSS_SELECTOR, '[data-testid="reply"]')
                        S.driver.execute_script("arguments[0].click();", comment_button)
                        print("commebt bug hahahahaha 2")
                    except:
                        print("comment bug hihih ntm 3")
                        return False

            time.sleep(2)
            try:
                element = WebDriverWait(S.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')))
            except:
                
                print("tweet text area div not here")
                time.sleep(1)
            
            textbox = S.driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
            S.driver.execute_script("arguments[0].scrollIntoView();", textbox)
            time.sleep(2)
            for t in text:
                textbox.send_keys(t)
                #time.sleep(0.02)
            textbox.send_keys(" ")
            textbox.send_keys(Keys.RETURN)
            time.sleep(1)
            #textbox.click()
            #print("ok 2")
            time.sleep(2)
            if "@" in text:
                time.sleep(3)
            try:
                element = WebDriverWait(S.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetButton"]')))
            except:
                print("tweetbtn not here")       
                time.sleep(1)
            
            wait = WebDriverWait(S.driver, 10)
            target_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButton"]')))
            S.driver.execute_script("arguments[0].scrollIntoView();", target_element)
            time.sleep(0.25)
            S.driver.execute_script("arguments[0].click();", target_element)
            
            #target_element.click()
            if "@" in text:
                time.sleep(3)
            else:
                time.sleep(3)
            print("comment done")
            return True
        
        except Exception as e:
            if "KeyboardInterrupt" in str(e):
                traceback.print_exc()
            print("Bref comment")
            #S.driver.refresh()
            time.sleep(0.5)
            return False


def get_absolute_picture_path(relative_path):
    current_directory = os.getcwd()    
    absolute_path = os.path.join(current_directory, relative_path)
    if os.path.exists(absolute_path) and os.path.isfile(absolute_path):
        return absolute_path
    else:
        return relative_path


def get_random_pic(nb):
    
    if nb == 1:
        picPath = r'D:\toto\RakuPic'
    else:
        picPath = r'D:\toto\LenoPic'
    

    # Liste les fichiers dans les répertoires
    filesP = os.listdir(picPath)

    # Chemins complets pour chaque fichier
    filesPic = [os.path.join(picPath, file) for file in filesP]

    return (filesPic[randint(0,len(filesPic) - 1)])

def comment_a_tweet_with_pic(S,url,text,filepath="",type="picture"):
    stop = True
    filepath = get_absolute_picture_path(filepath)
    print(filepath , " aca pdodp")
    while stop:
        
        try:
            S.driver.set_page_load_timeout(15)
            S.driver.get(url)
            time.sleep(0.001)
            pos = 0
            try:
                element = WebDriverWait(S.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')))
            except:
                print("cell innder div not here")
                time.sleep(1)
                
            tweet_info = S.driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
            for i in range(len(tweet_info)):
                r = tweet_info[i]
                if url.split("x.com")[1] in str(r.get_attribute("outerHTML")):
                    pos = i
                    break
            
            try:
                element = WebDriverWait(S.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="reply"]')))
            except:
                
                print("reply div not here")
                time.sleep(1)

            
            comment_button = S.driver.find_elements(By.CSS_SELECTOR, '[data-testid="reply"]')
            time.sleep(0.25)
            #comment_button[pos].click()
            try:
                S.driver.execute_script("arguments[0].click();", comment_button[pos])
            except:
                try:
                    S.driver.execute_script("arguments[0].click();", comment_button[0])
                    print("comment bug hehehe 1")
                except:
                    try:
                        comment_button = S.driver.find_element(By.CSS_SELECTOR, '[data-testid="reply"]')
                        S.driver.execute_script("arguments[0].click();", comment_button)
                        print("commebt bug hahahahaha 2")
                    except:
                        print("comment bug hihih ntm 3")
                        return False

            time.sleep(2)          

            try:
                input_file = S.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                input_file[0].send_keys(filepath)
            except:
                file_input = S.driver.find_element(By.XPATH,"//input[@type='file']")
                file_input.send_keys(filepath)

            time.sleep(2)
            
            time.sleep(2)
            try:
                element = WebDriverWait(S.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')))
            except:
                
                print("tweet text area div not here")
                time.sleep(1)

            textbox = S.driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
            S.driver.execute_script("arguments[0].scrollIntoView();", textbox)
            time.sleep(2)
            for t in text:
                textbox.send_keys(t)
                #time.sleep(0.02)
            textbox.send_keys(" ")
            textbox.send_keys(Keys.RETURN)
            time.sleep(1)
            #textbox.click()
            #print("ok 2")
            time.sleep(2)

            
            if "@" in text:
                time.sleep(3)
            try:
                element = WebDriverWait(S.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetButton"]')))
            except:
                print("tweetbtn not here")       
                time.sleep(1)
            
            wait = WebDriverWait(S.driver, 10)
            target_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButton"]')))
            S.driver.execute_script("arguments[0].scrollIntoView();", target_element)
            time.sleep(0.25)
            S.driver.execute_script("arguments[0].click();", target_element)
            
            
            time.sleep(10)

            #target_element.click()
            if "@" in text:
                time.sleep(3)
            else:
                time.sleep(3)
            print("comment done")
            return True
        
        except Exception as e:
            if "KeyboardInterrupt" in str(e):
                traceback.print_exc()
            print("Bref comment")
            traceback.print_exc()
            #S.driver.refresh()
            time.sleep(0.5)
            return False

def remove_hashtags(string):
    new_string = ''
    for word in string.split():
        if not word.startswith('#'):
            new_string += ' ' + word
    new_string = new_string.strip()
    return new_string

def search_tweet_for_better_rt(selenium_session):
    d = Data()
    with open("configuration.yml", "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    nb = data["random_retweet_nb"]
    username_info = data["account_username"][0]
    current_directory = os.getcwd()
    currentDir = current_directory.split("\\")[-1]
    try:
        username_info = currentDir 
    except:
        username_info = currentDir

    bigRecent = True
    accb = print_file_info("accb.txt").lower().split("\n")
    accz = print_file_info("accz.txt").lower().split("\n")
    
    if username_info.lower() in accb or username_info.lower() in accz:
        print("little guy")
        bigRecent = False
        nb = 30
    random_action = data["random_action"]
    word_to_rt = data["word_to_rt"]
    rt_your_word = data["rt_your_word"]
    rt_to_blacklist = data["rt_to_blacklist"]
    blacklist = False
    tweet_found_ = []
    url_list = []
    tweet_url = []
    already_comment = print_file_info("comment.txt").split("\n")
    accb = print_file_info("accb.txt").lower()
    already_rt = print_file_info("../txt_files_folder/all_random_rt.txt").split("\n")
    
    # urll = print_file_info("url.txt").split("\n")
    # for u in urll:
    #     already_rt.append(u)
    
    try:
        nbTweetDone = len(print_file_info("../txt_files_folder/recent_url.txt").split("\n")) - 1
    except:
        nbTweetDone = 9999

    print("Leeennnnn nbTweetDone " , nbTweetDone)
    if len(print_file_info("../txt_files_folder/recent_url.txt").split("\n")) <= 1:
        nbTweetDone = randint(12,25)
    if nbTweetDone <= 4:
        nb = randint(15,25)
    elif nbTweetDone < 10:
        nb = randint(20,30)
    if random_action == True and nb > 0:
        nb = randint(1,nb)
    if nbTweetDone == 0:
        nb = randint(5,15)
    if bigRecent == False:
        rrecent = False

    #rrecent = False
    if random_action == False:
        if rt_your_word == False:
            
            tweet_found = search_tweet(selenium_session,str(get_trend(selenium_session)[0]),nb)
            if d.tweet_lang != "any":
                tweet_found = search_tweet(selenium_session,' lang:'+d.tweet_lang + " " + str(get_trend(selenium_session)[0]) +" since:"+str(remove_days(30)),nb) 
            for tweet in tweet_found:
                if tweet["url"] not in url_list:
                    for r in rt_to_blacklist:
                        if r in tweet["url"]:
                            blacklist == True
                    if blacklist == False:
                        url_list.append(tweet["url"])
                    blacklist = False
        else:
            rt_found = 0
            rot = "-concours -jeuxconcours -rt -follow -tas -like -tag -giveaway -cadeau -cadeaux -retweet "

            
            rot2 = "-concours -jeuxconcours -rt -follow -tas -like -tag -giveaway -cadeau -cadeaux -retweet"

            minrt = " min_retweets:5 "
            sentence_word = "min_retweets:5 "
            sentence_acc = "min_retweets:5 "
            ze = ' " '
            nb_nb_word = 0
            for i in range(len(word_to_rt)):
                if "from" in word_to_rt[i]:
                    spt = word_to_rt[i].split(" ")[0]
                    sentence_acc = sentence_acc + spt + " OR "
                    if "-concours -jeuxconcours -rt -follow -tas -like -tag -giveaway -cadeau -cadeaux -jeuconcours -retweet" in sentence_word:
                        sentence_word = sentence_word.replace("-concours -jeuxconcours -rt -follow -tas -like -tag -giveaway -cadeau -cadeaux -jeuconcours -retweet min_retweets:5","")
                else:
                    sentence_word = sentence_word + " " + ze + word_to_rt[i].replace(rot,"") + ze +  " OR "
                    sentence_word = sentence_word.replace(rot,"").replace(rot2,"")
                    if "-concours -jeuxconcours -rt -follow -tas -like -tag -giveaway -cadeau -cadeaux -jeuconcours -retweet min_retweets:5" in sentence_word:
                        sentence_word = sentence_word.replace("-concours -jeuxconcours -rt -follow -tas -like -tag -giveaway -cadeau -cadeaux -jeuconcours -retweet min_retweets:5","")
                    nb_nb_word+=1

            sentence_acc = sentence_acc[:-3]
            sentence_word = sentence_word[:-3]

            
            sentence_word+=" " + rot
            sentence_acc+=" " + rot 


            if nbTweetDone >= 10:
                nb = nb + 5
            else:
                nb = nb + 1
            try:
                nb_of_tweet = randint(2,nb-20)
            except:
                if nbTweetDone <= 4:
                    nb = 15
                    nb_of_tweet = 10
                elif nbTweetDone < 10:
                    nb = 20
                    nb_of_tweet = 20
                else:            
                    nb_of_tweet = 25
            if nbTweetDone == 0:
                nb = randint(5,15)


            tweet_found , tweet_found2 = "" , ""
            kaizen = False
            if d.tweet_lang != "any":
                if nb_nb_word > 0 and d.minimum_rt != 2525 and "kaizen" not in str(sentence_word):
                    print("xoxo 1")
                    try:
                        tweet_found = search_tweets(selenium_session,' lang:'+d.tweet_lang + " " + str(sentence_word) +" since:"+str(remove_days(30)),nb_of_tweet)
                        if tweet_found == "WIFI":
                            tweet_found = search_tweets(selenium_session,' lang:'+d.tweet_lang + " " + str(sentence_word) +" since:"+str(remove_days(30)),nb_of_tweet)
                        #print("RT search for words : ")
                        #print(' lang:'+d.tweet_lang + " " + str(sentence_word) +" since:"+str(remove_days(30)))
                        print(len(tweet_found), " mot ")
                    except:
                        time.sleep(10)
                        try:
                            tweet_found = search_tweets(selenium_session,' lang:'+d.tweet_lang + " " + str(sentence_word) +" since:"+str(remove_days(30)),nb_of_tweet)
                        except:
                            pass
                        print("here 2")
                        pass
                
                elif nb_nb_word > 0 and d.minimum_rt == 2525 and "kaizen" not in str(sentence_word):
                    print("they dont know me son")
                    try:
                        tweet_found = search_tweets(selenium_session,' lang:'+d.tweet_lang + " " + str(sentence_word) +" min_retweets:150 since:"+str(remove_days(30)),nb_of_tweet)
                        if tweet_found == "WIFI":
                            tweet_found = search_tweets(selenium_session,' lang:'+d.tweet_lang + " " + str(sentence_word) +" min_retweets:150 since:"+str(remove_days(30)),nb_of_tweet)
                        #print("RT search for words : ")
                        #print(' lang:'+d.tweet_lang + " " + str(sentence_word) +" since:"+str(remove_days(30)))
                        print(len(tweet_found), " mot ")
                    except:
                        time.sleep(10)
                        try:
                            tweet_found = search_tweets(selenium_session,' lang:'+d.tweet_lang + " " + str(sentence_word) +" min_retweets:150 since:"+str(remove_days(30)),nb_of_tweet)
                        except:
                            pass
                        print("here 2")
                        pass
                
                elif d.minimum_rt > 3000 and "kaizen" in str(sentence_word):
                    print("dzdzdz dz")
                    kaizen = True
                    nb_of_tweet = 35
                    if nbTweetDone <= 4:
                        nb_of_tweet = 15
                    elif nbTweetDone < 10:
                        nb_of_tweet = randint(20,30)
                    if nbTweetDone == 0:
                        nb = randint(5,15)
    
                    try:
                        tweet_found = search_tweets(selenium_session," lang:fr le min_retweets:900",nb_of_tweet)
                        if tweet_found == "WIFI":
                            tweet_found = search_tweets(selenium_session," lang:fr le min_retweets:900",nb_of_tweet)
                        #print("RT search for words : ")
                        #print(' lang:'+d.tweet_lang + " " + str(sentence_word) +" since:"+str(remove_days(30)))
                        print(len(tweet_found), " mot ")
                    except:
                        time.sleep(10)
                        try:
                            tweet_found = search_tweets(selenium_session," lang:fr le min_retweets:900",nb_of_tweet)
                        except:
                            pass
                        print("here 2")
                        pass
                    for t in tweet_found:
                        if "follow" in t["big_text"].lower() or "concours" in t["big_text"].lower() or "+ rt" in t["big_text"].lower() or "retweet" in t["big_text"].lower() or "pour participer" in t["big_text"].lower() or "rt +" in t["big_text"].lower() :
                            print("Won't rt giveaway for random rt")
                            print(t["url"])
                        else:
                            if t["url"] not in already_rt:
                                url_list.append(t["url"])
                                write_into_file("../txt_files_folder/all_randomrt.txt",t["url"]+"\n")
                    

                    print("not enough kaizen tweet found will search more")
                    time.sleep(60)
                    if len(tweet_found) < 4:
                        tweet_found = search_tweets(selenium_session," lang:fr le min_retweets:200",30)

                    for t in tweet_found:
                        if "follow" in t["big_text"].lower() or "concours" in t["big_text"].lower() or "+ rt" in t["big_text"].lower() or "retweet" in t["big_text"].lower() or "pour participer" in t["big_text"].lower() or "rt +" in t["big_text"].lower() :
                            print("Won't rt giveaway for random rt")
                            print(t["url"])
                        else:
                            if t["url"] not in already_rt:
                                url_list.append(t["url"])
                                write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
                    
                elif nb_nb_word > 0 and d.minimum_rt == 2525 and "kaizen" in str(sentence_word):
                    print("weie 1")
                    kaizen = True
                    nb_of_tweet = 35
                    if nbTweetDone <= 4:
                        nb_of_tweet = 15
                    elif nbTweetDone < 10:
                        nb_of_tweet = randint(20,30)
                    if nbTweetDone == 0:
                        nb = randint(5,15)
    
                    try:
                        tweet_found = search_tweets(selenium_session," lang:fr à min_retweets:500",nb_of_tweet)
                        if tweet_found == "WIFI":
                            tweet_found = search_tweets(selenium_session," lang:fr à min_retweets:500",nb_of_tweet)
                        #print("RT search for words : ")
                        #print(' lang:'+d.tweet_lang + " " + str(sentence_word) +" since:"+str(remove_days(30)))
                        print(len(tweet_found), " mot ")
                    except:
                        time.sleep(10)
                        try:
                            tweet_found = search_tweets(selenium_session," lang:fr à min_retweets:500",nb_of_tweet)
                        except:
                            pass
                        print("here 2")
                        pass
                    for t in tweet_found:
                        if "follow" in t["big_text"].lower() or "concours" in t["big_text"].lower() or "+ rt" in t["big_text"].lower() or "retweet" in t["big_text"].lower() or "pour participer" in t["big_text"].lower() or "rt +" in t["big_text"].lower() :
                            print("Won't rt giveaway for random rt")
                            print(t["url"])
                        else:
                            if t["url"] not in already_rt:
                                url_list.append(t["url"])
                                write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
                    

                    print("not enough kaizen tweet found will search more")
                    time.sleep(60)
                    if len(tweet_found) < 4:
                        tweet_found = search_tweets(selenium_session," lang:fr à min_retweets:500",30)

                    for t in tweet_found:
                        if "follow" in t["big_text"].lower() or "concours" in t["big_text"].lower() or "+ rt" in t["big_text"].lower() or "retweet" in t["big_text"].lower() or "pour participer" in t["big_text"].lower() or "rt +" in t["big_text"].lower() :
                            print("Won't rt giveaway for random rt")
                            print(t["url"])
                        else:
                            if t["url"] not in already_rt:
                                url_list.append(t["url"])
                                write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
                    
                
                if kaizen == False:
                    print("fucked")
                    try:
                        rrecent = False
                        recent = randint(1,10)
                        
                        if recent > 7:
                            rrecent = True
                        if d.minimum_rt == 2525:
                            rrecent = False
                        if username_info.lower() in accb.lower() or username_info.lower() in accz.lower():
                            rrecent = False
                        if bigRecent == False:
                            rrecent = False
                        sentence_acc = sentence_acc.replace("min_retweets:5", " ")
                        if len(tweet_found) == 0 or nb_nb_word == 0:
                            tweet_found2 = search_tweets(selenium_session,str(sentence_acc) + "min_retweets:5" +" since:"+str(remove_days(30)),nb-3,rrecent)
                            if tweet_found2 == "WIFI":
                                tweet_found2 = search_tweets(selenium_session,str(sentence_acc) + "min_retweets:5" +" since:"+str(remove_days(30)),nb-3,rrecent)
                        else:
                            tweet_found2 = search_tweets(selenium_session,str(sentence_acc) +" since:"+str(remove_days(30)),nb-nb_of_tweet,rrecent)
                            if tweet_found2 == "WIFI":
                                tweet_found2 = search_tweets(selenium_session,str(sentence_acc) +" since:"+str(remove_days(30)),nb-nb_of_tweet,rrecent)
                        #print("RT search for accounts: ")
                        #print(str(sentence_acc) +" since:"+str(remove_days(30)),nb-nb_of_tweet)
                        print(len(tweet_found2)," compte ")
                    
                    except:
                        time.sleep(10)
                        try:
                            if len(tweet_found) == 0 or nb_nb_word == 0:
                                tweet_found2 = search_tweets(selenium_session,str(sentence_acc) + "min_retweets:5" +" since:"+str(remove_days(30)),nb-3)
                                if tweet_found2 == "WIFI":
                                    tweet_found2 = search_tweets(selenium_session,str(sentence_acc) + "min_retweets:5" +" since:"+str(remove_days(30)),nb-3)
                            else:
                                tweet_found2 = search_tweets(selenium_session,str(sentence_acc) +" since:"+str(remove_days(30)),nb-nb_of_tweet)
                                if tweet_found2 == "WIFI":
                                    tweet_found2 = search_tweets(selenium_session,str(sentence_acc) +" since:"+str(remove_days(30)),nb-nb_of_tweet)
                            print(len(tweet_found), " nouveaux mot ")
                            print(len(tweet_found2)," nouveaux compte ")

                            if len(tweet_found) + len(tweet_found2) < 2:
                                time.sleep(300)
                                tweet_found2 = search_tweets(selenium_session,"from:alertesinfos OR from:Cerfiafr OR from:BFMTV min_retweets:80" +" since:"+str(remove_days(30)),nb-nb_of_tweet)
                                print("len apres la der des der  " , len(tweet_found2))
                        except:
                            pass
                        

                        print("here bof")
                        #traceback.print_exc()
                        pass
                
                    if len(tweet_found) + len(tweet_found2) < 5 and kaizen == False and nbTweetDone > 10:
                        print("Not enough tweet found will try again")
                        time.sleep(10)
                        tweet_found = search_tweets(selenium_session,' lang:'+d.tweet_lang + " " + str(sentence_word) +" since:"+str(remove_days(60)),20,True)
                        time.sleep(15)
                        tweet_found2 = search_tweets(selenium_session,str(sentence_acc) + "min_retweets:5" +" since:"+str(remove_days(60)),20,True)
                        print("Word: " , len(tweet_found) ," Account: " , len(tweet_found2))
                        time.sleep(5)

                    if len(tweet_found) + len(tweet_found2) < 15 and kaizen == False and nbTweetDone > 10:
                        print("Not enough tweet found will rt more")
                        if nb_nb_word > 0:
                            if d.minimum_rt < 1500:
                                tweet_found2 = search_tweets(selenium_session,str(sentence_word) + "min_retweets:5" +" since:"+str(remove_days(300)),25,True)             
                            else:
                                tweet_found2 = search_tweets(selenium_session,str(sentence_word) + "min_retweets:5" +" since:"+str(remove_days(300)),35,True)             
                            try:    
                                for t in tweet_found2:
                                    if "follow" in t["big_text"].lower() or "concours" in t["big_text"].lower() or "+ rt" in t["big_text"].lower() or "retweet" in t["big_text"].lower() or "pour participer" in t["big_text"].lower() or "rt +" in t["big_text"].lower() :
                                        print("Won't rt giveaway for random rt")
                                        print(t["url"])
                                    else:
                                        if t["url"] not in already_rt:
                                            url_list.append(t["url"])
                                            write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
                            except:
                                traceback.print_exc()
                                print("here 4")
                                pass   
                                
                        if d.minimum_rt < 1500:
                            tweet_found2 = search_tweets(selenium_session,str(sentence_acc) + "min_retweets:5" +" since:"+str(remove_days(30)),15,True)             
                        else:
                            tweet_found2 = search_tweets(selenium_session,str(sentence_acc) + "min_retweets:5" +" since:"+str(remove_days(30)),25,True)             
                        try:    
                            for t in tweet_found2:
                                if "follow" in t["big_text"].lower() or "concours" in t["big_text"].lower() or "+ rt" in t["big_text"].lower() or "gagner" in t["big_text"].lower() or "gagnez" in t["big_text"].lower() or "tas le" in t["big_text"].lower() or "t.a.s" in t["big_text"].lower() or "tirage au" in t["big_text"].lower():
                                    print("Won't rt giveaway for random rt")
                                    print(t["url"])
                                else:
                                    if t["url"] not in already_rt:
                                        url_list.append(t["url"])
                                        write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
                        except:
                            traceback.print_exc()
                            print("here 4")
                            pass   
                        
                    if nb_nb_word > 0:
                        try:
                            for t in tweet_found:
                                if "follow" in t["big_text"].lower() or "concours" in t["big_text"].lower() or "+ rt" in t["big_text"].lower() or "gagner" in t["big_text"].lower() or "gagnez" in t["big_text"].lower() or "tas le" in t["big_text"].lower() or "t.a.s" in t["big_text"].lower() or "tirage au" in t["big_text"].lower():
                                    print("Won't rt giveaway for random rt")
                                    print(t["url"])
                                else:
                                    if t["url"] not in already_rt:
                                        url_list.append(t["url"])
                                        write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
                        except:
                            traceback.print_exc()
                            print("here 3")
                            pass

                    try:    
                        for t in tweet_found2:
                            if "follow" in t["big_text"].lower() or "concours" in t["big_text"].lower() or "+ rt" in t["big_text"].lower() or "de gagner" in t["big_text"].lower() or "de gagnez" in t["big_text"].lower() or "tas le" in t["big_text"].lower() or "t.a.s" in t["big_text"].lower() or "tirage au" in t["big_text"].lower():
                                print("Won't rt giveaway for random rt")
                                print(t["url"])
                            else:
                                if t["url"] not in already_rt:
                                    url_list.append(t["url"])
                                    write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
    
                    except:
                        traceback.print_exc()
                        print("here 4")
                        pass   
                comment_list = []
                comment_text = []
                nb_rdm = randint(1,4)

                gpt = 1
                response_tweet = []
                
                if d.minimum_rt < 900 and d.minimum_rt!= 200 and d.minimum_rt != 250:
                    gpt = randint(1,30)
                elif d.minimum_rt > 900 and d.minimum_rt < 1900:
                    gpt = randint(1,25)                    
                else:
                    gpt = randint(1,20)
                
                print("GPT VALUE " , gpt)
                #write_into_file("error.txt","5")
                gpt = 0
                if gpt != 1:
                    return url_list 
                
                # for z in tweet_found2:
                #     try:
                #         if z["url"] not in already_comment:
                #             t_text = zet_tweet_info(selenium_session,z["url"])
                #             if len(t_text) >= 25 and len(t_text) <= 225 and t_text.count(" ") >= 10 and nb_rdm>=len(comment_list):
                #                 comment_list.append(z["url"]) 
                #                 comment_text.append(t_text)
                #                 write_into_file("comment.txt",z["url"])
                #                 write_into_file("comment.txt","\n")
                #     except:
                #         print("wtf")
                #         pass
                try:
                    chs = randint(0,len(comment_list) - 1)
                    #tweett_url = comment_list[chs]
                    #tweett_text = comment_text[chs]
                    #tweett_urls = []
                    #tweeett_texts = []
                    pdo = '"'

                    #return url_list 

                    gpt = 1
                    print("GPT VALUE " , gpt)
                    print("nbTweetDone: " , nbTweetDone)
                    print("Nb of tweet_found " , len(url_list))
            
                    # try:
                    #     if len(comment_list) > 0:
                    #         from scrap import maker
                    #         res = maker(comment_text,nb_rdm)
                    #         #res = res.replace(pdo,"")
                    #         for i in range(len(comment_text)):
                    #             rose = res[i].replace(pdo,"")
                    #             cds = randint(1,2)
                    #             if comment_list[i] not in response_tweet and comment_text[i].count(" ") >= 4 and "this content may violate" not in comment_text[i].lower() and len(comment_text[i]) < 220:
                    #                 r = remove_hashtags(rose)
                    #                 if cds == 1:
                    #                     r = re.sub(r'\b#\w+\b', ' ', rose)
                    #                     if comment_a_tweet(selenium_session,comment_list[i].replace("ChatGPT" , " ").replace("chatgpt" , " ").replace("a dit :" , " "),rose) == False:
                    #                         print("Will try to comment again...")
                    #                         time.sleep(10)
                    #                         quote_a_tweet(selenium_session,comment_list[i].replace("ChatGPT" , " ").replace("chatgpt" , " ").replace("a dit :" , " "),rose)

                    #                     response_tweet.append(comment_list[i])
                    #                     time.sleep(10)
                    #                 else:
                    #                     quote_a_tweet(selenium_session,comment_list[i].replace("ChatGPT" , " ").replace("chatgpt" , " ").replace("a dit :"," "),remove_emojie(rose))
                    #                     response_tweet.append(comment_list[i])
                    #                     time.sleep(10)
                    #     pass
                    # except:
                    #     pass                
                except:
                    #traceback.print_exc()
                    pass
                if randint(1,10) == 2:
                    return url_list[::-1]
                if randint(1,5) == 2:
                    random.shuffle(url_list)
                return url_list 
           
            for tweet in tweet_url:
                #print(tweet["text"] , tweet["url"])
                if tweet["url"] not in url_list:
                    for r in rt_to_blacklist:
                        if r in tweet["url"]:
                            blacklist == True
                    if blacklist == False:
                        url_list.append(tweet["url"])
                    blacklist == False

    else:
        try:
            trend = get_trend(selenium_session)
            trend.append("a")
            if word_to_rt == True:
                trend = word_to_rt
                if len(trend) == 0:
                    trend = get_trend(selenium_session)
                    trend.append("a")
                print("hello")   
            for i in range(nb):
                tweet_found = search_tweet(selenium_session,str(trend[randint(0,len(trend) - 1)]),1)
                if d.tweet_lang != "any":
                    tweet_found = search_tweet(selenium_session,' lang:'+d.tweet_lang + " " + str(trend[randint(0,len(trend) - 1)]) +" since:"+str(remove_days(30)),1)
                for t in tweet_found:
                    if t["url"] not in url_list:
                        for r in rt_to_blacklist:
                            if r in tweet["url"]:
                                blacklist == True
                    if blacklist == False:
                        url_list.append(tweet["url"])
                    blacklist == False
            
            #url_list = []
            #for tweet in tweet_found_:
            #    url_list.append(tweet)
        except:
            tweet_found = search_tweet(selenium_session,str(get_trend(selenium_session)[0]),nb)
            if d.tweet_lang != "any":
                tweet_found = search_tweet(selenium_session,' lang:'+d.tweet_lang + " " + str(get_trend(selenium_session)[0]) +" since:"+str(remove_days(30)),nb)
            for tweet in tweet_found:
                if tweet["url"] not in url_list:
                    for r in rt_to_blacklist:
                        if r in tweet["url"]:
                            blacklist == True
                    if blacklist == False:
                        url_list.append(tweet["url"])
                    blacklist == False
    
    return url_list

def list_inside_text(list_one,text):
    for l in list_one:
        if l.lower() not in text.lower():
            return False
    return True


def split_date(string):
    with open("configuration.yml", "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    keydate = data["date_keyword"]
    splitage = ""
    for k in keydate:
        if k.lower() in string.lower():
            splitage = string.lower().split(k.lower())
            if "\n" in splitage[1]:
                ssp = splitage[1].split("\n")
                return ssp[0]
            else:
                return splitage[1]
            
    return "o"

def check_date(string):
    with open("configuration.yml", "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    keydate = data["date_keyword"]
    splitage = ""
    for k in keydate:
        if k.lower() in string.lower():
            splitage = string.split(k.lower())
            #ssp = splitage[1].split("\n")
            return True
    #print("nop")
    return False

def get_digit(s):
  o = ""
  n = "0123456789"
  for ss in s:
    if ss in n:
        o+=ss
  return o

def make_date(day,month,year):
   full_date = ""
   day = str(day)
   month = str(month)
   if len(day) == 1:
      day = "0"+ day
   if len(month) == 1:
      month = "0" + month
   if month != "12":
       year = 2026
   full_date = str(year) + "-" + month + "-" + day
   return (full_date)

def get_giveaway_draw_date(date_str, text):
    month_names = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    today = datetime.now().date()
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    year = datetime.now().year
    
    if "demain" in text.lower():
        return date + timedelta(days=1)
    
    days_mapping = { 
        "24h": 1, "16h": 1, "12h": 1, "1 jour": 1, "1 jours": 1, "1J": 1,
        "48h": 2, "2 jour": 2, "2 jours": 2, "2J": 2,
        "72h": 3, "3 jour": 3, "3 jours": 3, "3J": 3,
        "4 jour": 4, "4 jours": 4, "4J": 4,
        "5 jour": 5, "5 jours": 5, "5J": 5,
        "6 jour": 6, "6 jours": 6, "6J": 6,
        "7 jour": 7, "une semaine": 7, "1 semaine": 7, "7 jours": 7, "7J": 7,
        "10 jour": 10,
        "14 jour": 14, "2 semaine": 14,
        "1 mois": 30
    }
    
    for day_text, value in days_mapping.items():
        if day_text in text.lower():
            return date + timedelta(days=value)
    
    for m in month_names:
        if m in text:
            t = text.split(m)[0].strip()
            try:
                day = int(''.join(filter(str.isdigit, t)))
                month = month_names.index(m) + 1
                draw_date = datetime(year, month, day).date()
                return draw_date
            except ValueError:
                pass
    
    if "/" in text:
        try:
            day, month = map(int, text.split("/")[:2])
            draw_date = datetime(year, month, day).date()
            return draw_date
        except ValueError:
            pass
    
    if "." in text:
        try:
            day, month = map(int, text.split(".")[:2])
            draw_date = datetime(year, month, day).date()
            return draw_date
        except ValueError:
            pass
    
    return None

def is_date_good(date_str,text):
    text = text.lower()
    month = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
    #week = ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
    today = datetime.now().date()
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    month_ = datetime.now().month
    year = datetime.now().year
    add = 999
    custom_date = ""
    
    if "demain" in text.lower():
        add = 1
        delta = date + timedelta(days=add)
        if delta < today:
            return False
        else:
            return True
    
    if "dans" in text.lower() or "jours" in text.lower() and "dans les commentaires" not in text.lower() and "dans les comm" not in text.lower():
        days_mapping = { 
            "24h": 1, "16h": 1, "12h": 1, "24 heures": 1, "12 heures": 1, "16 heures": 1,
            "1 jour": 1, "à 12h": 1, "à 13h": 1, "à 14h": 1, "à 15h": 1, "à 16h": 1,
            "à 17h": 1, "à 18h": 1, "à 19h": 1, "à 20h": 1, "à 21h": 1, "1 jours": 1, "1jours": 1, "1 Jours": 1, "1J": 1,"1 J":1,
            "48h": 2, "36h": 2, "48 heures": 2, "36 heures": 2, "2 jour": 2, "2 jours": 2, "2jour": 2, "2jours": 2, "2J": 2,"2 J":2,
            "72h": 3, "72 heures": 3, "3 jour": 3, "3 jours": 3, "3jours": 3, "3 Jours": 3, "3J": 3,"3 J":3,
            "4 jour": 4, "4 j": 4, "4 jours": 4, "4jours": 4, "4 Jours": 4, "4J": 4,"4 J":4,
            "5 jour": 5, "5 j": 5, "5 jours": 5, "5jours": 5, "5 Jours": 5, "5J": 5,"5 J ":5,
            "6 jour": 6, "6 j": 6, "6 jours": 6, "6jours": 6, "6 Jours": 6, "6J": 6,"6 J":6,
            "7 jour": 7, "une semaine": 7, "1 semaine": 7, "7 jours": 7, "7jours": 7, "7J": 7,"7 J":7,
            "10 jour": 10, "10 j": 10,
            "14 jour": 14, "14 j": 14, "2 semaine": 14, "deux semaine": 14,
            "1 mois": 30
        }

        add = 0
        for day_text, value in days_mapping.items():
            if day_text in text.lower():
                add = value
                break

        if add is not None:
            delta = date + timedelta(days=add)
            return delta >= today
        else:
            return False
    else:
       for m in month:
          if m in text:
             t = text.split(m)[0]
             t = get_digit(t)
             if month != "décembre":
                year=2025
             day_date = make_date(t,month.index(m)+1,year)
             day_date = datetime.strptime(day_date, '%Y-%m-%d').date()
             if day_date < today:
                return False
             else:
                return True
             continue
       
       if text.count("/") >= 1:
        t = text.split("/")
        day , month = t[0] , t[1] 
        day , month = get_digit(day) , get_digit(month)
        
        #if str(month) == 12 and month_ < 11:
        #    year = year - 1
        if len(day) == 1:
            day = "0"+ day
        if len(month) == 1:
            month = "0" + month
        
        try:
            month = month[0:2]
        except:
            month = month
        if month != "12":
            year = 2026
        full_date = str(year) + "-" + month + "-" + day
        #print("Full date: " , full_date)
        #print("Year: " , year , " Month: " ,  month , " Day: " , day)
        
        try:
            day_date = datetime.strptime(full_date, '%Y-%m-%d').date()
        except:
            print(day_date)
            print("day error caca")
            return True
        if day_date < today:
            return False
        else:
            return True
        
       elif text.count(".") >= 1:  
        t = text.split(".")
        day , month = t[0] , t[1]
        day , month = get_digit(day) , get_digit(month)
        
        #if str(month) == 12 and month_ < 11:
        #    year = year - 1

        if len(day) == 1:
            day = "0"+ day
        if len(month) == 1:
            month = "0" + month
        try:
            month = month[0:2]
        except:
            month = month
        if month != "12":
            year = 2026
        full_date = str(year) + "-" + month + "-" + day
        #print("Full date: " , full_date)
        #print("Year: " , year , " Month: " ,  month , " Day: " , day)
        try:
            day_date = datetime.strptime(full_date, '%Y-%m-%d').date()
        except:
            print("day error caca")
            return True
        if day_date < today:
            return False
        else:
            return True
    
    if "demain" in text.lower():
        add = 1
        delta = date + timedelta(days=add)
        if delta < today:
            return False
        else:
            return True

    return True



def get_giveaway_url(selenium_session,search=False):
    try:
        d = Data()
        reset_file("../txt_files_folder/recent_url.txt")

        tweets_need_to_comment_or_not = []
        tweets_text = []
        tweets_id = []
        tweets_url = []
        tweets_full_comment = []
        tweets_account_to_follow = []
        nb_of_giveaway_found = 0
        char = '#'
        full_phrase = ""
        doublon = 0
        url_from_file = print_file_info("../txt_files_folder/allurl.txt").split("\n")
        url_from_ban = ["krpokgpoerkgpkg"]
        #accb = print_file_info("accb.txt").lower().split("\n")
        accb = [""]
        url_from_like = print_file_info("../txt_files_folder/allurl.txt").split("\n")
        
        with open("configuration.yml", "r",encoding="utf-8") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
    

        #accz = print_file_info("accz.txt").lower().split("\n")
        accz = [""]
        #accrypto = print_file_info("accrypto.txt").lower().split("\n")
        accrypto = [""]
        username_info = data["account_username"][0]
        current_directory = os.getcwd()
        currentDir = current_directory.split("\\")[-1]
        try:
            username_info = currentDir 
        except:
            username_info = currentDir
        if username_info.lower() in accb or username_info.lower() in accz:
            print("little russiaan")
        print_data = False
        date_ = ""
        date_format = "%Y-%m-%d"
        check_ = []
        MAX = 1000
        giveaway_foud_per_word = 0
        ban_word = ""
        ban_word_list = []
        duplicated_url = []
        twt_text = ""
        cryptoBro = False
        tweet_user = []
        tweet_text = []
        time_url = []
        for banned_word in d.giveaway_to_blacklist:
            if "." not in banned_word:
                ban_word += "-" + banned_word + " "

        if len(ban_word) <= len(d.giveaway_to_blacklist):
            ban_word = ""
        nb_of_tweet_to_search = 50
        if d.minimum_rt < 700 and d.minimum_rt > 145 and d.minimum_rt != 198:
            #nb_of_tweet_to_search = 150
            nb_of_tweet_to_search = 100
            #d.minimum_rt = 1001
            d.nb_of_giveaway = 45
        if nb_of_tweet_to_search > 1000:
            nb_of_tweet_to_search = 1000
        if d.nb_of_giveaway > MAX:
            d.nb_of_giveaway = MAX
        
        
        d.nb_of_giveaway = MAX
        d.nb_of_giveaway = 1
        if username_info.lower() in accb:
            print("only doing big rt")
            d.minimum_rt = 2600
        
        if username_info.lower() in accz and username_info.lower() not in accrypto:
            print("only doing big big big big rt")
            d.minimum_rt = 4000
        
        if username_info.lower() in accrypto:
            print("only doing crypto giveaway")
            d.minimum_rt = 198
            cryptoBro = True 

        


                
        
        
        draw_date_list = []

        # # TAS LE 6 JANVIER

        # # try:
        # #     url = "https://x.com/msifrance/status/1871988335797014673"
        # #     if url not in url_from_file:
        # #         print("good good msifrance")
        # #         tweets_url.append(url)
        # #         tweet_user.append("msifrance")
        # #         tweets_text.append('Commente "#CalendrierMSI"') 
        # #         giveaway_foud_per_word+=1
        # # except:
        # #     print("bip bip error msifrance")
        
        # TAS LE 23
        # try:
        #     url = "https://x.com/Wshark67/status/1864738265716478134"
        #     if url not in url_from_file:
        #         print("good good Wshark67")
        #         tweets_url.append(url)
        #         tweet_user.append("ASUS_ROG_FR")
        #         tweet_user.append("Wshark67")
        #         tweets_text.append("tfdgdfgdmis")
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error Wshark67")

        # TAS LE 25

        # TAS LE 20
            
        
        # TAS JSP QUAND

        # try:
        #     url = "https://x.com/el_libro01/status/1869032763573338485"
        #     if url not in url_from_file:
        #         print("good good el_libro01")
        #         tweets_url.append(url)
        #         tweet_user.append("el_libro01")
        #         tweets_text.append("tag 2 ami") 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error el_libro01")
        
        # # TAS LE 25
        
        # try:
        #     url = "https://x.com/lebraqueurr/status/1869765758676607223"
        #     if url not in url_from_file:
        #         print("good good lebraqueurr")
        #         tweets_url.append(url)
        #         tweet_user.append("lebraqueurr")
        #         tweets_text.append("tag 2 ami") 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error lebraqueurr")
            
        # try:
        #     url = "https://x.com/OTP_LoL/status/1866498109037232280?t=XDz5iCRTKmUDtFnDyADysw&s=19"
        #     if url not in url_from_file:
        #         print("good good OTP_LoL")
        #         tweets_url.append(url)
        #         tweet_user.append("OTP_LoL")
        #         tweet_user.append("KITKATGaming")
        #         tweets_text.append("nijiefe")
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error OTP_LoL")
        
        # TAS JSP SURREMENT AVANT NOEL
        
        # TAS LE 25
        
        
        
        # TAS LE 25
        
        # TAS LE 26

        
        # TAS LE 26

        
        # TAS LE 24         
        # try:
        #     url = "https://x.com/CryptoastMedia/status/1871088354684456982"
        #     if url not in url_from_file:
        #         print("good good cryptoastMedia")
        #         tweets_url.append(url)
        #         tweet_user.append("cryptoastMedia")
        #         tweet_user.append("Bitpanda_FR")
        #         tweets_text.append("tfdgdfgdmis")
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error cryptoastMedia")

        
        # TAS LE 2

        # TAS JSP


        # TAS AJD
            
        # try:
        #     url = "https://x.com/Foot2RueUltras/status/1919008237057135095"
        #     scores = [
        #         "4-2", "4-3", "4-4","5-2", "5-3", "5-4",
        #         "6-2", "6-3", "6-4","6-5",
        #         "7-2", "7-3", "7-4","7-5"
               
        #     ]

        #     if url not in url_from_file:
        #         scr = random.choice(scores)
        #         e = randint(1, 2)
        #         equip = " pour f2r "
        #         if e == 2:
        #             equip = " pour fc slimi "
        #         score_text = scr + equip
        #         maximus = 0
        #         scoreFoot = print_file_info("../scoreFoot.txt").lower().split("\n")
        #         if len(scoreFoot) >= ((len(scores)) * 2) - 1:
        #             reset_file("../scoreFoot.txt")
        #         while score_text in scoreFoot:
        #             e = randint(1, 2)
        #             equip = " pour f2r "
        #             if e == 2:
        #                 equip = " pour fc slimi "        
        #             score_text = random.choice(scores) + equip
        #             maximus+=1
        #             if maximus == 200:
        #                 break
        #         write_into_file("../scoreFoot.txt",score_text+"\n")
        #         tweets_text.append(f'Commente "{score_text}"')
        #         tweet_user.append("Foot2RueUltras")
        #         tweets_url.append(url)
        #         print("good good Foot2RueUltras")
        # except:
        #     pass
        
        # TAS LE 18 JUIN

        # try:
        #     rlz = "https://x.com/SFR/status/1937124181558124725?t=3H-2c5j0ygAVYKGoyfsbLw&s=19"
        #     drawDate = print_file_info("../txt_files_folder/drawDate.txt").lower().split("\n")

        #     if rlz.lower() not in drawDate:
        #         write_into_file("../txt_files_folder/drawDate.txt","2021-07-01 https://x.com/SFR/status/1937124181558124725?t=3H-2c5j0ygAVYKGoyfsbLw&s=19\n")
        #     url = "https://x.com/SFR/status/1937124181558124725?t=3H-2c5j0ygAVYKGoyfsbLw&s=19"
        #     if url not in url_from_file:
        #         print("good good SFR")
        #         tweets_url.append(url)
        #         tweet_user.append("SFR")
        #         tweets_text.append("tefzfefzeis") 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error SFR")
        

        # # TAS LE 7

        # try:
        #     rlz = "https://x.com/coinacademy_fr/status/1939730407156502726"
        #     drawDate = print_file_info("../txt_files_folder/drawDate.txt").lower().split("\n")

        #     if rlz.lower() not in drawDate:
        #         write_into_file("../txt_files_folder/drawDate.txt","2021-07-07 https://x.com/coinacademy_fr/status/1939730407156502726\n")
        #     url = "https://x.com/coinacademy_fr/status/1939730407156502726"
        #     if url not in url_from_file:
        #         print("good good coinacademy_fr")
        #         tweets_url.append(url)
        #         tweet_user.append("coinacademy_fr")
        #         tweet_user.append("Bitpanda_fr")
        #         tweets_text.append("tag 1 amis") 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error SFR")
        

        # try:
        #     url = "https://x.com/CHOWH1_/status/1972373126496600359?t=dtzvkPSDO8hhVxrg8TK6Ww&s=19\n"
        #     drawDate = print_file_info("../txt_files_folder/drawDate.txt").lower().split("\n")

        #     if url.lower() not in drawDate:
        #         write_into_file("../txt_files_folder/drawDate.txt",f"2021-07-07 {url}")
        
        #     url = "https://x.com/CHOWH1_/status/1972373126496600359?t=dtzvkPSDO8hhVxrg8TK6Ww&s=19"
        #     if url not in url_from_file:
        #         print("good good CHOWH1_")
        #         tweets_url.append(url)
        #         tweet_user.append("CHOWH1_")
        #         tweet_user.append("ASUS_ROG_FR")
        #         tweets_text.append("fkjnfejknfkjerfer") 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error CHOWH1_") 
        
        from datetime import datetime

        # Get today's date
        today = datetime.today().date()

        # Target date
        #target_date = datetime(2025, 8, 20).date()
        #if today > target_date:
        
        
        
        # target_date = datetime(2025, 9, 15).date()
        # if today > target_date:

        #
        # try:
        #     comments = [
        #         "Fingers crossed!! 🤞",
        #         "Good luck everyone!",
        #         "I hope this is my time 😭🔥",
        #         "Let's gooo 🙌🙌",
        #         "Would love to win this!",
        #         "That laptop looks insane 😳",
        #         "Perfect timing, my PC is dying 😅",
        #         "Count me in!",
        #         "Hoping for the best!",
        #         "This would help so much 😭",
        #         "Good luck to all participants!",
        #         "Alienware always dropping heat 😍",
        #         "Let’s try my luck again 🤞",
        #         "Please be my lucky day 🙏",
        #         "This looks amazing 🔥",
        #         "I really need this upgrade!",
        #         "Wow this is sick 😳",
        #         "Thanks for the chance!",
        #         "Trying my luck 😁",
        #         "Hope I get lucky this time!",
        #         "Such a clean design!",
        #         "My laptop is literally falling apart lol",
        #         "This would be perfect for gaming 🕹️",
        #         "Crossing my fingers!",
        #         "Good luck to everyone entering!",
        #         "This looks dope!",
        #         "Count me in for this!",
        #         "My dream laptop fr 😭",
        #         "Appreciate the giveaway!",
        #         "I could use this for work and gaming!",
        #         "This thing looks like a beast 👀",
        #         "Hoping for a miracle 😅",
        #         "Already following, thanks for the opportunity!",
        #         "Let’s win this! 🔥",
        #         "Bro this is beautiful 😭",
        #         "Good luck to all!!",
        #         "I need this upgrade so bad 😭",
        #         "This would replace my toaster of a laptop 😂",
        #         "Looks insane!",
        #         "Fingers crossed 🤞🔥",
        #         "My laptop from 2012 is crying rn 😭",
        #         "Hoping to be the lucky winner!",
        #         "Great giveaway!",
        #         "This would be a game changer!",
        #         "Let’s do this! 💪",
        #         "Awesome opportunity!",
        #         "I need this for my studies too 🙏",
        #         "Sheeesh that’s clean 👀",
        #         "Would be amazing to win!",
        #         "Hope luck is on my side!",
        #         "This is so cool!",
        #         "Bless us with this laptop 🙏",
        #         "My setup desperately needs this 😂",
        #         "This looks powerful!",
        #         "Praying to the giveaway gods 🙌",
        #         "That RGB glow tho 👀",
        #         "I can already imagine gaming on it 😭🔥",
        #         "Good luck y’all!",
        #         "Thank you for doing this!",
        #         "Amazing laptop!",
        #         "This would help me get into streaming!",
        #         "Hoping to replace my old machine!",
        #         "Alienware always brings quality 🔥",
        #         "This would be a perfect Christmas gift 🎁",
        #         "I hope the RNG blesses me 😂",
        #         "Incredible giveaway!",
        #         "This is exactly what I need rn",
        #         "Let’s hope for the best!",
        #         "Entering now!",
        #         "This is gorgeous 😍",
        #         "Tryna win for real this time 😂",
        #         "My old laptop can’t handle anything anymore lol",
        #         "That screen looks amazing!",
        #         "Good luck everyone!!!",
        #         "Would be super useful!",
        #         "Hope I get picked 🙏",
        #         "This is HUGE 🔥",
        #         "My laptop last 1% of life 😂",
        #         "I'm manifesting this 😤✨",
        #         "Would love to win this for editing vids!",
        #         "This would be a huge upgrade!",
        #         "Let’s get it!!",
        #         "This is fire 🔥🔥",
        #         "Appreciate the chance!",
        #         "Could definitely use this!",
        #         "GL to all peeps entering!",
        #         "This is too clean 😳",
        #         "Bro I need this so bad lol",
        #         "Manifesting Alienware energy ✨",
        #         "Hope to see my name in the winner list 👀",
        #         "Such an awesome giveaway!",
        #         "I’m in! 🤞",
        #         "Please let me win this 🙏🔥",
        #         "Laptop of my dreams 😭",
        #         "This is super cool!",
        #         "Okay I REALLY need this 😂",
        #         "Thanks for doing this giveaway!",
        #         "Let’s hope RNG loves me!",
        #         "This would be incredible to win!",
        #         "Trying my luck again 🤞",
        #         "Good luck everyone & thanks!",
        #         "Such a beautiful machine 😍",
        #         "I need this MORE than oxygen 😂"
        #     ]
        #     url = "https://x.com/TeamLiquid/status/1991975268509237689"
        #     if url not in url_from_file:
        #         print("good good TeamLiquid")
        #         tweets_url.append(url)
        #         tweet_user.append("TeamLiquid")
        #         tweets_text.append(f'Commente "{random.choice(comments)}"') 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error TeamLiquid")
        

        



        
        
        # try:
        #     url = "https://x.com/AcerFrance/status/1998679125624586488"
        #     if url not in url_from_like:
        #         jeux = [
        #             "Red Dead Redemption 2",
        #             "The Witcher 3: Wild Hunt",
        #             "Elden Ring",
        #             "God of War (2018)",
        #             "God of War Ragnarök",
        #             "Horizon Zero Dawn",
        #             "Horizon Forbidden West",
        #             "Assassin's Creed Valhalla",
        #             "Cyberpunk 2077",
        #             "Grand Theft Auto V",
        #             "GTA Online",
        #             "Marvel's Spider-Man 2",
        #             "Sekiro: Shadows Die Twice",
        #             "Dark Souls III",
        #             "The Elder Scrolls V: Skyrim",
        #             "Fallout 4",
        #             "Fallout: New Vegas",
        #             "Control",
        #             "Hitman 3",
        #             "Resident Evil 2 (Remake)",
        #             "Resident Evil 4 (Remake)",
        #             "Doom Eternal",
        #             "Halo Infinite",
        #             "Forza Horizon 5",
        #             "FIFA 23",
        #             "Rocket League",
        #             "Fortnite",
        #             "Apex Legends",
        #             "Overwatch 2",
        #             "Valorant",
        #             "League of Legends",
        #             "Dota 2",
        #             "Minecraft",
        #             "Stardew Valley",
        #             "Animal Crossing: New Horizons",
        #             "The Last of Us Part II",
        #             "Ghost of Tsushima",
        #             "Persona 5 Royal",
        #             "Mass Effect Legendary Edition",
        #             "Metro Exodus",
        #             "Dishonored 2",
        #             "BioShock Infinite",
        #             "Portal 2",
        #             "Half-Life: Alyx",
        #             "Tom Clancy's Rainbow Six Siege",
        #             "Among Us",
        #             "Celeste",
        #             "Hades",
        #             "Dead Cells",
        #             "The Legend of Zelda: Breath of the Wild"
        #         ]
        #         print("good good AcerFrance")
        #         tweets_url.append(url)
        #         tweet_user.append("AcerFrance")
        #         tweet_user.append("Conforama")
                
        #         tweets_text.append(f'Commente "{random.choice(jeux)}"') 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error AcerFrance")
        

        

        # try:
        #     url = "https://x.com/Cdiscount/status/1994077523203010784"
        #     if url not in url_from_file:
        #         print("good good Cdiscount")
        #         tweets_url.append(url)
        #         tweet_user.append("Cdiscount")
        #         tweets_text.append('Commente "#CdiscountBlackFriday "') 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error Cdiscount")
        
        # try:
        #     url = "https://x.com/BattlefieldEAFR/status/1993364263365218392"
        #     if url not in url_from_file:
        #         print("good good BattlefieldEAFR")
        #         tweets_url.append(url)
        #         tweet_user.append("BattlefieldEAFR")
        #         tweets_text.append('Commente "#MSIxBATTLEFIELD6 "') 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error BattlefieldEAFR")
        


        # target_date = datetime(2025, 12, 21).date()
        # if today > target_date:
        #     try:
        #         url = "https://x.com/Frandroid/status/1995523288953446833"
        #         if url not in url_from_like:
        #             print("good good Frandroid")
        #             tweets_url.append(url)
        #             tweet_user.append("Frandroid")
        #             tweets_text.append('Commente "#FrandroidOffreMoi + Nintendo Switch 2 + Mario Kart World "') 
        #             giveaway_foud_per_word+=1
        #     except:
        #         print("bip bip error Frandroid")
            
        # try:
        #     url = "https://x.com/fekahdesbois/status/1993323563214889270"
        #     if url not in url_from_file:
        #         print("good good topachat")
        #         tweets_url.append(url)
        #         tweet_user.append("fekahdesbois")
        #         tweet_user.append("Chattynews_")
        #         tweets_text.append("kfprekgrekogrg") 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error fekahdesbois")

   
      
        # # target_date = datetime(2025, 12, 15).date()
        # # if today > target_date:
        # #     try:
        # #         url = "https://x.com/CHOWH1_/status/2000535636378259581"
        # #         if url not in url_from_like:
        # #             print("good good julienchieze")
        # #             tweets_url.append(url)
        # #             tweet_user.append("CHOWH1_")
        # #             tweet_user.append("ASUS_ROG_FR")
        # #             tweet_user.append("AMD_France")
                    
        # #             tweets_text.append("kgoperkgopkgpoerg") 
        # #             giveaway_foud_per_word+=1
        # #     except:
        # #         print("bip bip error julienchieze")

        
        # try:
        #     url = "https://x.com/Lockl34r/status/1999874591100215544"
        #     if url not in url_from_like:
        #         print("good good Lockl34r")
        #         tweets_url.append(url)
        #         tweet_user.append("Lockl34r")
        #         tweet_user.append("PoE2Actus")                
        #         tweets_text.append("kfprekgrekogrg") 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error Lockl34r")
        
        # try:
        #     url = "https://x.com/StealthGamerFR/status/1996535656701456414"
        #     if url not in url_from_like:
        #         print("good good StealthGamerFR")
        #         tweets_url.append(url)
        #         tweet_user.append("StealthGamerFR")
        #         tweet_user.append("nextlvlracing")
        #         tweet_user.append("moza_racing")
                
        #         tweets_text.append("kfprekgrekogrg") 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error StealthGamerFR")
        
        # try:
        #     url = "https://x.com/TopAchat/status/2001608385964241284"
        #     if url not in url_from_like:
        #         print("good good topachat")
        #         tweets_url.append(url)
        #         tweet_user.append("TopAchat")
        #         tweets_text.append('Commente "#PetitPapaTopAchat "') 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error TopAchat")

        # try:
        #     url = "https://x.com/predatorfrance/status/1994334700845011170"
        #     if url not in url_from_like:
        #         print("good good topachat")
        #         tweets_url.append(url)
        #         tweet_user.append("PredatorFrance")
        #         tweets_text.append('Commente "#PredatorxBadlands "') 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error fekahdesbois")

        # target_date = datetime(2025, 12, 7).date()
        # if today > target_date:
        #     try:
        #         url = "https://x.com/crypto__goku/status/2000473359864262990"
        #         if url not in url_from_like:
        #             print("good good crypto__goku")
        #             tweets_url.append(url)
        #             tweet_user.append("crypto__goku")
        #             tweets_text.append('Commente "Je participe"') 
        #             giveaway_foud_per_word+=1
        #     except:
        #         print("bip bip error crypto__goku")
 
        
        # try:
        #     url = "https://x.com/NRGgg/status/1991991548821876969"
        #     if url not in url_from_file:
        #         print("good good NRGgg")
        #         tweets_url.append(url)
        #         tweet_user.append("NRGgg")
        #         tweets_text.append("tag un ami") 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error NRGgg")
        
        # try:
        #     url = "https://x.com/e691ccecc035ie/status/1990192581448212842"
        #     if url not in url_from_file:
        #         print("good good e691ccecc035ie")
        #         tweets_url.append(url)
        #         tweet_user.append("x")
        #         tweets_text.append("kgoperkgopkgpoerg") 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error e691ccecc035ie")
        
        # target_date = datetime(2025, 12, 15).date()
        # if today > target_date:
        #     try:
        #         url = "https://x.com/julienchieze/status/1999096504343024065"
        #         if url not in url_from_like:
        #             print("good good julienchieze")
        #             tweets_url.append(url)
        #             tweet_user.append("julienchieze")
        #             tweet_user.append("redmagicgaming")
        #             tweets_text.append("kgoperkgopkgpoerg") 
        #             giveaway_foud_per_word+=1
        #     except:
        #         print("bip bip error julienchieze")

        # target_date = datetime(2025, 12, 20).date()
        # if today > target_date:
        #     try:
        #         url = "https://x.com/cryptoastmedia/status/1995379870709285304"
        #         if url not in url_from_like:
        #             print("good good cryptoastmedia")
        #             tweets_url.append(url)
        #             tweet_user.append("cryptoastmedia")
        #             tweet_user.append("bitstack")
        #             tweets_text.append("kgoperkgopkgpoerg") 
        #             giveaway_foud_per_word+=1
        #     except:
        #         print("bip bip error cryptoastmedia")

        #     try:
        #         url = "https://x.com/cryptoastmedia/status/1999765743626231955"
        #         if url not in url_from_like:
        #             print("good good cryptoastmedia")
        #             tweets_url.append(url)
        #             tweet_user.append("cryptoastmedia")
        #             tweet_user.append("krakenfx_FR")
        #             tweet_user.append("DorianKraken")
                    
        #             tweets_text.append("kgoperkgopkgpoerg") 
        #             giveaway_foud_per_word+=1
        #     except:
        #         print("bip bip error cryptoastmedia")
    
        target_date = datetime(2025, 12, 25).date()
        if today > target_date:
            try:
                url = "https://x.com/Inoxtag/status/1986874533337502057"
                if url not in url_from_like:
                    print("good good Inoxtag")
                    tweets_url.append(url)
                    tweet_user.append("Inoxtag")
                    tweets_text.append("kgoperkgopkgpoerg") 
                    giveaway_foud_per_word+=1
            except:
                print("bip bip error Inoxtag")

        
        # try:
        #     url = "https://x.com/ASUS_ROG_FR/status/1984191113855447243"
        #     if url not in url_from_file:
        #         print("good good ASUS_ROG_FR")
        #         tweets_url.append(url)
        #         tweet_user.append("ASUS_ROG_FR")
        #         tweets_text.append('Commente "#ROGPGW25 "') 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error ASUS_ROG_FR")

        # try:
        #     url = "https://x.com/ASUS_ROG_FR/status/1984542175334711517"
        #     if url not in url_from_file:
        #         print("good good ASUS_ROG_FR")
        #         tweets_url.append(url)
        #         tweet_user.append("ASUS_ROG_FR")
        #         tweets_text.append('Commente "#ROGPGW25 "') 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error ASUS_ROG_FR")

        if search:
            # for url in tweets_url:
            #     write_into_file("url.txt",url+"\n")
            #     write_into_file("recent_url.txt",url+"\n")

            from datetime import datetime
            dateT = datetime.now().strftime("%d/%m/%Y")             

            allurl = print_file_info("../txt_files_folder/allurl.txt").lower()
            for url in tweets_url:
                if url.lower() not in allurl:
                    write_into_file("../txt_files_folder/allurl.txt",url+ " " + dateT + " " + "\n")

            return (tweets_url,tweets_text,tweet_user)

        # target_date = datetime(2025, 10, 7).date()
        
        # try:
        #     url = "https://x.com/ADNanime/status/1978853445944709406"
        #     anime_list = [
        #     # animés récents / populaires
        #     "Dandadan",
        #     "Solo Leveling",
        #     "Kaiju No. 8",
        #     "The Apothecary Diaries",
        #     "Frieren: Beyond Journeys End",
        #     "Blue Box",
        #     "Wind Breaker",
        #     "Fire Force (Saison 3)",
        #     "Oshi no Ko",
        #     "Attack on Titan",
        #     "Jujutsu Kaisen",
        #     "Chainsaw Man",
        #     "Spy × Family",
        #     "Dan Da Dan",
        #     "Let’s Go Karaoke!",
        #     "My Happy Marriage",
        #     "Honey Lemon Soda",
        #     "The Dangers in My Heart",
        #     "Re:Zero",
        #     "Villainess Level 99",
        #     "Demon Slayer",
        #     "Delicious in Dungeon",
        #     "Wistoria: Wand and Sword",
        #     "That Time I Got Reincarnated as a Slime",
        #     "Devil May Cry (anime)",
        #     "Black Butler: Emerald Witch Arc",
        #     "Dragon Ball Z",
        #     "Dragon Ball",
        #     "Naruto",
        #     "Naruto Shippuden",
        #     "Bleach",
        #     "One Piece",
        #     "Hunter × Hunter",
        #     "Fairy Tail",
        #     "Fullmetal Alchemist: Brotherhood",
        #     "Death Note",
        #     "Yu Yu Hakusho",
        #     "Sailor Moon",
        #     "Gundam",
        #     "Neon Genesis Evangelion",
        #     "Cowboy Bebop",
        #     "Trigun",
        #     "Inuyasha",
        #     "Rurouni Kenshin",
        #     "Legacy of the “Big 3”: Naruto, One Piece, Bleach",
        #     "Yu-Gi-Oh!",
        #     "Fullmetal Alchemist",
        #     "Black Clover",
        #     "Mob Psycho 100",
        # ]

        #     if url not in url_from_file:
        #         print("good good ADNanime")
        #         tweets_url.append(url)
        #         tweet_user.append("ADNanime")
        #         tweets_text.append(f'Commente "{random.choice(anime_list)}"') 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error ADNanime") 
                

        # TAS SEMAINE PRO
        
        
        # TAS AJD

        
        # try:
        #     url = "https://x.com/Foot2RueUltras/status/1916960265041809918"
        #     if url not in url_from_file:
        #         print("good good Foot2RueUltras")
        #         tweets_url.append(url)
        #         tweet_user.append("Foot2RueUltras")
        #         tweets_text.append("fefeteggegergeri") 
        #         giveaway_foud_per_word+=1
        # except:
        #     print("bip bip error Foot2RueUltras")
        

        # TAS AJD
        
        # TAS LE 8 JUIN
        
        # TAS JSP

        if username_info.lower() in accrypto:
            print("o")
                    
            # try:
            #     giveaway = search_tweet(selenium_session,"from:papa_rieur min_retweets:220" +" since:"+str(remove_days(1)) + "-filter:replies " ,5)
            #     print("good good papa_rieur")
            #     print("len de giveaway papa_rieur " , len(giveaway))
            #     for g in giveaway:
            #         if g["url"] not in url_from_file:
            #             tweets_url.append(g["url"])
            #             tweet_user.append("FeelMining")
            #             tweets_text.append("nioeiofeziofz")
            #             giveaway_foud_per_word+=1
            # except:
            #     print("bip bip error papa_rieur")
            # time.sleep(15)
            # try:
            #     giveaway = search_tweet(selenium_session,"from:FeelMining min_retweets:220" +" since:"+str(remove_days(2)) + "-filter:replies " ,5)
            #     print("good good FeelMining")
            #     print("len de giveaway FeelMining " , len(giveaway))
            #     for g in giveaway:
            #         if g["url"] not in url_from_file:
            #             tweets_url.append(g["url"])
            #             tweet_user.append("FeelMining")
            #             tweets_text.append("écrit")
            #             giveaway_foud_per_word+=1
            # except:
            #     print("bip bip error FeelMining")
            
            # time.sleep(30)           
            
            
            # try:
            #     import random
            #     rdm_s = []
            #     url = "https://x.com/lenovofr/status/1867620503671751019?t=rS_9iWcULI9X7hfGQaEGaQ&s=19"
            #     if url not in url_from_file:
            #         print("good good lenovofr")
            #         url = "https://x.com/lenovofr/status/1867620503671751019?t=rS_9iWcULI9X7hfGQaEGaQ&s=19"
            #         picPath = get_random_pic(2)
            #         comment_a_tweet_with_pic(selenium_session,url, " " , picPath)
            #         tweets_url.append(url)
            #         tweet_user.append("lenovofr")
            #         tweets_text.append("rcacacact")
            #         giveaway_foud_per_word+=1
            # except:
            #     print("bip bip error lenovofr")


        
        if d.minimum_rt > 400:
            #if d.minimum_rt > 900:
            #    print("")
            # try:
            #     giveaway = search_tweet(selenium_session,"from:TheGuill84 min_retweets:900" +" since:"+str(remove_days(15)) + "-filter:replies " + ban_word ,1)
            #     print("good good TheGuill84") 
            #     for g in giveaway:
            #         if g["url"] not in url_from_file:
            #             tweets_url.append(g["url"])
            #             tweet_user.append("EvoluCraftV4")
            #             tweet_user.append("TheGuill84")
            #             tweets_text.append("mentionne un ami ")
            #             giveaway_foud_per_word+=1
            # except:
            #     print("bip bip error TheGuill84")

            time.sleep(10)
            
            # try:
            #     print("good good Snapdragon_FR")
            #     url = "https://x.com/Snapdragon_FR/status/1824385740018536639"
            #     if url not in url_from_file:
            #         tweets_url.append("https://x.com/Snapdragon_FR/status/1824385740018536639")
            #         tweet_user.append("Snapdragon_FR")
            #         toto = """
            #             La performance sans limite est à portée de clic ! Pour fêter notre arrivée sur X, tentez de remporter 2 #GalaxyS24Ultra : un pour vous et un pour un ami
            #             Suivez @Snapdragon_FR
            #             Taguez un ami
            #             Dites-nous ce que vous immortaliseriez avec son impressionnant zoom 100x
            #         """
            #         tweets_text.append(toto)
            #         giveaway_foud_per_word+=1
            # except:
            #     print("bip bip error Snapdragon_FR")
            
            
            # time.sleep(10)

            
            #https://x.com/UFA_Gaming/status/1833534001514004682
            #https://x.com/UgreenFR/status/1833446230330118602
            p = '"'

            #https://x.com/ErazerFrance/status/1844393176364130788

            
            #https://x.com/Esports_News_UK/status/1846893287627436163/photo/4            
            


            # TAS LE 16
            # try:
            #     rdm_s = []
            #     url = "https://x.com/lenovofr/status/1867620503671751019?t=rS_9iWcULI9X7hfGQaEGaQ&s=19"
            #     if url not in url_from_file:
            #         print("good good lenovofr")
            #         url = "https://x.com/lenovofr/status/1867620503671751019?t=rS_9iWcULI9X7hfGQaEGaQ&s=19"
            #         picPath = get_random_pic(2)
            #         comment_a_tweet_with_pic(selenium_session,url," ", picPath)
            #         tweets_url.append(url)
            #         tweet_user.append("lenovofr")
            #         tweets_text.append("rcacacact")
            #         giveaway_foud_per_word+=1
            # except:
            #     print("bip bip error lenovofr")

            
            # try:
            #     giveaway = search_tweet(selenium_session,"from:Crypto__Goku min_retweets:1000 follow" +" since:"+str(remove_days(5)) + "-filter:replies " ,10)
            #     print("good good Crypto__Goku")
            #     print("len de giveaway Crypto__Goku " , len(giveaway))
            #     for g in giveaway:
            #         if g["url"] not in url_from_file:
            #             tweets_url.append(g["url"])
            #             c_text = g["text"]
            #             if c_text == "ok":
            #                 c_text = get_tweet_info(selenium_session,g["url"])
            #             tweet_user.append("Crypto__Goku")
            #             tweets_text.append('Commente "je participe"')
            #             giveaway_foud_per_word+=1
            # except:
            #     print("bip bip error Crypto__Goku")
        
            #     time.sleep(30)            

            # # TAS LE 1
            # try:
            #     url = "https://x.com/reyesclothes/status/1859283672781799452"
            #     if url not in url_from_file:
            #         print("good good reyesclothes")
            #         tweets_url.append(url)
            #         tweet_user.append("reyesclothes")
            #         tweets_text.append("tag 1 ami")
            #         giveaway_foud_per_word+=1
            # except:
            #     print("bip bip error reyesclothes")

            # TAS J

            
            # try:
            #     giveaway = search_tweet(selenium_session,"from:NVIDIAGeForceFR min_retweets:500" +" since:"+str(remove_days(d.maximum_day)) + "-filter:replies " + ban_word ,3)
            #     print("good good NVIDIAGeForceFR")
            #     for g in giveaway:
            #         if g["url"] not in url_from_file:
            #             tweets_url.append(g["url"])
            #             tweet_user.append("NVIDIAGeForceFR")
            #             try:
            #                 c_text = get_tweet_info(selenium_session,g["url"])
            #                 tweets_text.append(c_text)
            #             except:
            #                 tweets_text.append("ok")    
                        
            #             giveaway_foud_per_word+=1
            # except:
            #     print("bip bip error NVIDIAGeForceFR")
            
            # try:
            #     giveaway = search_tweet(selenium_session,"j" +" since:"+str(remove_days(d.maximum_day)) + "-filter:replies " + ban_word ,3)
            #     print("good good Minxt0")
            #     for g in giveaway:
            #         if g["url"] not in url_from_file:
            #             tweets_url.append(g["url"])
            #             tweet_user.append("Minxt0")
            #             try:
            #                 c_text = get_tweet_info(selenium_session,g["url"])
            #                 tweets_text.append(c_text)
            #             except:
            #                 tweets_text.append("ok")    
                        
            #             giveaway_foud_per_word+=1
            # except:
            #     print("bip bip error Minxt0")


        # DOESNT WORK
         
        # d_word_to_search = print_file_info("searchQuery.txt").split("\n")
        # nb_of_tweet_to_search = 99
        # if d.minimum_rt < 900:
        #     d_word_to_search = d.word_to_search
        # d_word_to_search = print_file_info("searchQuery.txt").split("\n")

        # nb_of_giveaway_found = 0
        # if d.minimum_rt == 198:
        #     d_word_to_search = print_file_info("searchQueryCrypto.txt").split("\n")            
        #     d.minimum_rt = 250
        # else:
        #     d_word_to_search = print_file_info("searchQuery.txt").split("\n")
        #     #d_word_to_search = d.word_to_search

        d_word_to_search = data["words_to_search"]
        flopinfo = 0
        d.nb_of_giveaway = 10000
        time.sleep(350)
        for search_word in d_word_to_search:
            if print_data == False:
                print("### " , search_word)
                print("### nb of giveaway foud " , nb_of_giveaway_found , d.nb_of_giveaway)
                time.sleep(20)
            if nb_of_giveaway_found <d.nb_of_giveaway and "." not in search_word:
                text = search_word + ' lang:'+d.tweet_lang + " min_faves:"+str(d.minimum_like) + " min_retweets:"+str(d.minimum_rt)+" since:"+str(remove_days(d.maximum_day)) + " " + "-filter:replies " + ban_word
                if d.tweet_lang == "any":
                    text = search_word + " min_faves:"+str(d.minimum_like) + " min_retweets:"+str(d.minimum_rt)+" since:"+str(remove_days(d.maximum_day)) + " " + "-filter:replies " + ban_word
                #print("Search Querry")
                #print(text)
                giveaway = search_tweet(selenium_session,text,nb_of_tweet_to_search)
                
                
                for g in giveaway:
                    giveaway_foud_per_word+=1
                # if nb_of_tweet_to_search < 10:
                #     time.sleep(10)
                # if nb_of_tweet_to_search <= 100 and nb_of_tweet_to_search >= 10:
                #     time.sleep(40)                
                # if nb_of_tweet_to_search > 100 and nb_of_tweet_to_search <= 300:
                #     time.sleep(60)
                # if nb_of_tweet_to_search > 300 and nb_of_tweet_to_search <= 999:
                #     time.sleep(60)
                # if nb_of_tweet_to_search >= 1000:
                #     time.sleep(800)
                
                c_text = ""
                #skipThisOne = False
                ban_giveaway = print_file_info("../txt_files_folder/ban_giveaway.txt").split("\n")
                for g in giveaway:
                    if g["url"] in ban_giveaway:
                        continue
                    

                    x = get_tweet_nb_of_rt(selenium_session,g["url"])
                    
                    if len(str(x)) == 0:
                        continue
                    
                    try:
                        if int(x) < 250:
                            continue
                    except:
                        pass
                    if g["url"] not in tweets_url and check_for_forbidden_word(g["text"].lower()) == False and check_blacklist(g["username"]) == False and g["url"] not in url_from_file and g["url"].lower() not in url_from_ban and nb_of_giveaway_found < d.nb_of_giveaway and check_for_forbidden_word(g["username"].lower()) == False and g["url"] not in time_url:
                        if cryptoBro == True:
                            if len(g["text"])  < 15:
                                c_text = get_tweet_info(selenium_session,g["url"])
                                if c_text == False:
                                    flopinfo+=1
                                else:
                                    flopinfo = 0
                                
                                if flopinfo > 3:
                                    break

                                time.sleep(2)
                            else:
                                c_text = g["text"]
                        if type(c_text) != bool:
                            if cryptoBro == True and len(c_text) > 10:
                                if "fav" in g["text"].lower()  or "follow" in g["text"].lower() or "concours" in g["text"].lower() or " rt" in g["text"].lower() or "retweet" in g["text"].lower() or "pour participer" in g["text"].lower() or "like" in g["text"].lower() or "comment" in g["text"].lower() or "giveaway" in g["text"].lower():
                                    print("ok Crypto Giveaway " , g["url"])
                                else:
                                    print("not a crypto giveaway ", g["url"])
                                    continue
                                
                        if nb_of_giveaway_found>=d.nb_of_giveaway:
                            break
                        
                        c_text = g["text"]
                        if c_text == "ok":
                            try:
                                if g["url"] not in duplicated_url:
                                    c_text = get_tweet_info(selenium_session,g["url"])
                                    if c_text == False:
                                        flopinfo+=1
                                    else:
                                        flopinfo = 0
                                    
                                    if flopinfo > 3:
                                        break
                                    
                                    if c_text == False:
                                        c_text = g["text"]
                                else:        
                                    c_text = g["text"]
                            except:
                                c_text = g["text"]
                        
                        if check_date(c_text.lower()) == False:
                            tweets_url.append(g["url"])
                            nb_of_giveaway_found+=1
                            duplicated_url.append(g["url"])
                            tweet_user.append(g["username"])
                            tweets_text.append(c_text)
                        else:
                            try:
                                striiing = split_date(c_text)
                                right_date = is_date_good(str(g["date"].split(" ")[0]),striiing)
                                try:
                                    draw_url = print_file_info("../txt_files_folder/drawDate.txt").lower().split("\n")
                                    draw_date_ = get_giveaway_draw_date(str(g["date"].split(" ")[0]),striiing)
                                    if draw_date_ != None and g["url"].lower() not in draw_url:
                                        write_into_file("../txt_files_folder/drawDate.txt",str(draw_date_) + " " + g["url"]+"\n")
                                        draw_date_list.append(str(draw_date_))
                                    
                                except:
                                    traceback.print_exc()
                                    pass
                            except:
                                right_date = True
                            
                            
                            if right_date == True:
                                tweets_url.append(g["url"])
                                nb_of_giveaway_found+=1
                                duplicated_url.append(g["url"])
                                tweet_user.append(g["username"])
                                tweets_text.append(c_text)
                            else:
                                print("Times Up")
                                print(g["url"])
                                duplicated_url.append(g["url"])
                                time_url.append(g["url"])
                            
                    elif list_inside_text(search_word.split(" "), g["text"]) == False and g["url"] not in url_from_file and g["url"].lower() not in url_from_ban and g["url"] not in tweets_url and g["url"] not in duplicated_url and check_blacklist(g["username"]) == False and g["url"] not in time_url:
                        if nb_of_giveaway_found>=d.nb_of_giveaway:
                            break
                        c_text = g["text"]
                        if c_text == "ok":
                            try:
                                if g["url"] not in duplicated_url:
                                    c_text = get_tweet_info(selenium_session,g["url"])
                                    if c_text == False:
                                        flopinfo+=1
                                    else:
                                        flopinfo = 0
                                    
                                    if flopinfo > 3:
                                        break
                                    
                                    if c_text == False:
                                        c_text = g["text"]
                                else:        
                                    c_text = g["text"]
                        
                            except:
                                c_text = g["text"]
                        
                        if check_date(c_text.lower()) == False:
                            tweets_url.append(g["url"])
                            tweet_user.append(g["username"])
                            tweets_text.append(c_text)    
                            nb_of_giveaway_found+=1
                            duplicated_url.append(g["url"])
                        else:
                            if g["url"] not in duplicated_url:
                                try:
                                    striiing = split_date(c_text)
                                    right_date = is_date_good(str(g["date"].split(" ")[0]),striiing)
                                    try:
                                        draw_url = print_file_info("../txt_files_folder/drawDate.txt").lower().split("\n")
                                        draw_date_ = get_giveaway_draw_date(str(g["date"].split(" ")[0]),striiing)
                                        if draw_date_ != None and g["url"].lower() not in draw_url:
                                            write_into_file("../txt_files_folder/drawDate.txt",str(draw_date_) + " " + g["url"]+"\n")
                                    except:
                                        traceback.print_exc()
                                        pass

                                except:
                                    right_date = True
                                
                                if right_date == True:
                                    tweets_url.append(g["url"])
                                    nb_of_giveaway_found+=1
                                    tweet_user.append(g["username"])
                                    tweets_text.append(c_text)
                                    duplicated_url.append(g["url"])
                                else:
                                    print("Times Up")
                                    print(g["url"])
                                    time_url.append(g["url"])
                                    duplicated_url.append(g["url"])
                                    
                    if nb_of_giveaway_found>=d.nb_of_giveaway:
                        break
            giveaway_foud_per_word = 0
        
        
        if len(tweets_id) > d.nb_of_giveaway:
            dif = len(tweets_id) - d.nb_of_giveaway
            tweets_url = tweets_url[:dif]


        # max_nb = 100
        
        # if len(tweets_url) <= max_nb:
        #     for url in tweets_url:
        #         write_into_file("url.txt",url+"\n")
        #         write_into_file("recent_url.txt",url+"\n")

        tweets_account_to_follow = get_a_better_list(tweets_account_to_follow)
        if print_data == True:
            print(tweets_url)
            print("Nb of doublon " + str(doublon))
        print("Number of giveaway found = " + str(nb_of_giveaway_found))
        idx = 0
        for to in tweets_url:
            idx+=1
        if nb_of_giveaway_found > 0:
            print("Ending giveaway search the bot will now start doing giveaways")
        
        try:
            from datetime import datetime
            dateT = datetime.now().strftime("%d/%m/%Y")                    

            allurl = print_file_info("../txt_files_folder/allurl.txt").lower()
            for url in tweets_url:
                if url.lower() not in allurl:
                    write_into_file("../txt_files_folder/allurl.txt",url+ " " + dateT + " " + "\n")
                    write_into_file("../txt_files_folder/recent_url.txt",url+"\n")

        except:
            pass

        return (tweets_url,tweets_text,tweet_user)    
    except Exception as e:
        print("Error occured but we are still doing some giveaways")
        traceback.print_exc()
        return (tweets_url,tweets_text,tweet_user)   

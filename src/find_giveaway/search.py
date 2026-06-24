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
                #print("error searching tweet sleep for 30 sec")
                time.sleep(5)
                try:
                    selenium_session.driver.get(current_url+"&f=live")
                    time.sleep(5)
                    selenium_session.driver.refresh()
                    time.sleep(5)
                    element = WebDriverWait(selenium_session.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
                except:
                    #print("error searching tweet even after refresh")
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
                    #send_message_discord(f"{username_info}\n got rt problem with thise search: {query} \n Replace those words/account!!! \n +++++++")        
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
    with open("../../configuration.yml", "r") as file:
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
                                #write_into_file("../txt_files_folder/all_randomrt.txt",t["url"]+"\n")
                    

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
                                #write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
                    
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
                                #write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
                    

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
                                #write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
                    
                
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
                            #print(len(tweet_found), " nouveaux mot ")
                            #print(len(tweet_found2)," nouveaux compte ")

                            if len(tweet_found) + len(tweet_found2) < 2:
                                time.sleep(300)
                                tweet_found2 = search_tweets(selenium_session,"from:alertesinfos OR from:Cerfiafr OR from:BFMTV min_retweets:80" +" since:"+str(remove_days(30)),nb-nb_of_tweet)
                                #print("len apres la der des der  " , len(tweet_found2))
                                print("len after retry" , len(tweet_found2))
                                
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
                                            #write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
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
                                        #write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
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
                                        #write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
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
                                    #write_into_file("../txt_files_folder/all_random_rt.txt",t["url"]+"\n")
    
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
    with open("../../configuration.yml", "r") as file:
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
    with open("../../configuration.yml", "r") as file:
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
        "24h": 1, "16h": 1, "12h": 1, "1 jour": 1, "1 jours": 1, "1J": 1,"tirage demain":1,
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
            "24h": 1, "16h": 1, "12h": 1, "24 heures": 1, "12 heures": 1, "16 heures": 1,"tirage demain":1,
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
        
        with open("../../configuration.yml", "r",encoding="utf-8") as file:
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
        # #     url = "https://x.com/grfthjk/status/gthyjukil"
        # #     if url not in url_from_file:
        # #         print("good good msifrance")
        # #         tweets_url.append(url)
        # #         tweet_user.append("msifrance")
        # #         tweets_text.append('Commente "#CalendrierMSI"') 
        # #         giveaway_foud_per_word+=1
        # # except:
        # #     print("bip bip error msifrance")
        
        
        # target_date = datetime(2025, 12, 25).date()
        # if today < target_date:
        #     try:
        #         url = "https://x.com/^rtyuhi/status/gfhtjkl"
        #         if url not in url_from_like:
        #             print("good good Inoxtag")
        #             tweets_url.append(url)
        #             tweet_user.append("Inoxtag")
        #             tweets_text.append("kgoperkgopkgpoerg") 
        #             giveaway_foud_per_word+=1
        #     except:
        #         print("bip bip error Inoxtag")

        
        # target_date = datetime(2025, 10, 7).date()
        
        # try:
        #     url = "https://x.com/gthyjuki/status/htyjukilompù"
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

        d_word_to_search = data["words_to_search"]
        flopinfo = 0
        d.nb_of_giveaway = 10000
        for search_word in d_word_to_search:
            if print_data == False:
                print("### " , search_word)
                print("### nb of giveaway foud " , nb_of_giveaway_found , d.nb_of_giveaway)
                time.sleep(60)
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
                    try:
                        if g["url"] in print_file_info("../txt_files_folder/allurl.txt"):
                            continue
                    except:
                        pass
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
                                    draw_url2 = print_file_info("../txt_files_folder/drawDate.txt").lower()
                                    
                                    draw_date_ = get_giveaway_draw_date(str(g["date"].split(" ")[0]),striiing)
                                    if draw_date_ != None and g["url"].lower() not in draw_url2:
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
                                        draw_url2 = print_file_info("../txt_files_folder/drawDate.txt").lower()
                                        
                                        draw_date_ = get_giveaway_draw_date(str(g["date"].split(" ")[0]),striiing)
                                        if draw_date_ != None and g["url"].lower() not in draw_url2:
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

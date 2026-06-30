# TwitterGiveawayBotV2

This is a new version of my previous TwitterGiveawayBot:

https://github.com/steevenakintilo/TwitterGiveawayBot

## 📘 Summary

- [Requirements](#requirements)
- [Features](#features)
- [How does it works](#how-does-it-works)
- [.txt files](#txt-files)
- [Discord](#Discord)
- [How to add accounts?](#how-to-add-accounts)
- [Configuration file for each accounts](#configuration-file-for-each-accounts)
- [Global configuration file](#global-configuration-file)
- [Advices](#advices)

## Requirements
To make the code work you will need to have Python and Pip installed in your computer.

Link to download python: https://www.python.org/downloads/

Link to download pip: https://pip.pypa.io/en/stable/installation/

Link to download google chrome: https://www.google.com/intl/fr_fr/chrome/ 

If you Google Chrome isn't updated to the latest version the bot may won't work!

You should also add 6 discord weebhooks (and store their credentials into discord_data_dict.json file) to get valuable information about your accounts in your discord server.

Here is how to do a discord webhook: https://www.svix.com/resources/guides/how-to-make-webhook-discord/


Download all the modules required for the bot to work using this command:

```bash
    pip install -r requirements.txt
```

If it's your first time do this:


```bash
    python .\src\find_giveaway\twt_cookies.py
```

It will open a login twitter window and you will just need to enter account name and password of an account then the bot will save the cookies file of this account and use it to avoid re-login everytime.


If it's not your first time do this:

```bash
    python main.py
```

If the bot failed to launch after several just make an issues I will help you make it work / or dm me on my discord: "sangokuhomer".

## Features
- The bot use Cloak Browser instead of regular google chrome to avoid getting flagged as a bot
- The bot can work in any language.
- The bot only log in once then use profile so it doesn't need to log in again.
- The bot can work with account that require OTP code.
- The bot wait randomly between 1 to 60 seconds between each follow/giveaway done/random retweet done to look more human
- Unlilke the other bots you can find on github this one don't use api which means that any twitter account you have can be used with this bot.

- Like Retweet and Comment a tweet giveaway.
- Follow all the person asked for the giveaway.
- It can @ people when needed, comment with # when needed and make no comment when we don't need to.
- The bot can do random retweet to act more "human".
- The bot can work with 1,2,20 or even 100 accounts you just have to add them in the src folder.
- The bot is flexible you can modify most of its features on the configuration.yml file
- Redo a giveaway (Unlike,Like,Unretweet,Retweet a post) the day of the draw to maximise your chance to be the most recent participants.
- Run a script that checks if your accounts have won giveaways by looking through the search bar for all of them.
- Send key information to your own discord server to see what the bot is doing

## How does it works 

There is one account that search giveaways and random tweets to retweet then all the tweets found will be set inside .txt files.

Other account will be used to do those giveaways/random tweets to reetweet.

To avoid geting flaged accounts run every 3 days.

Account are divided into 3 groupes that run once a day. 

So there is a group of acccounts that run on day1 a group of accounts that run on day2 and on a day3 then it go back to day1 and so on.

So for example on day one it could do something like this:

- Account X search for giveaways/random tweets to retweet
- Store all the information into .txt files
- Loop through all account to do giveaway on those acccounts 1 by 1
- Run the script that checks if one of your accounts has won a giveaway.
- End

Since accounts run every 3 days you only need to run the code once a day and it's better to run it in the morning.

## .txt files

Some important data are stored on .txt files:

You can find all giveaway files on src/txt_files_folder folder to see all the giveaways url , comment , user to follow and more.

src/txt_files_folder/drawDate.txt stores all giveaway that have an end-date so the bot won't do those giveaway is the date is over.

account_of_groupe1_name.txt , account_of_groupe2_name.txt , account_of_groupe3_name.txt files contain account that will run on day1,day2 and day3.

Account on each files should be different and you should split account into a divider/close divider of 3.

If you have 6 accounts you should do 2-2-2 and if you have 11 you should do 4-4-3 that way it would take the same time everyday to run accounts.

account_to_tag.txt files is the file that handle account to @ on giveaway.

It works like that:

You can add 4 accounts per line split by a coma and each account on the same line will @ each other.

To avoid bot suspicion you should only put different account name on each line.

All account on the same line should be different otherwise the bot may @ himself or the same account twice.

Here is a simple example:
```txt
account_to_tag_name1,account_to_tag_name2,account_to_tag_name3,account_to_tag_name4
account_to_tag_name5,account_to_tag_name6,account_to_tag_name7,account_to_tag_name8
account_to_tag_name9,account_to_tag_name10,account_to_tag_name11,account_to_tag_name12
```

With real account names:

```txt
MrBeast,PewDiePie,CristianoRonaldo,Billieeilish
TaylorSwift,Ninja,Drake,KylianMbappe
KaiCenat,TheWeeknd,ErlingHaaland,SnoopDogg
```

otp_acc.txt file is used to store otp code for account that use OTP connexion.

If you account use otp code to connect just add your account name and the OTP code separate with a space like this:

```txt
account1	KXWJJFEFSS5V7REO
account2	REGFSFSEZ542WFLO
```

group_of_the_day.txt file just store the group_of_the_day number to see which group of account are going to run you don't need to change/touch it.


## Discord 

If you don't want to have information about the giveaway on your discord server skip this part.

First you need to create 5 discord webhooks and store their credentials into discord_data_dict.json file

There are 5 differents channels you should do:

- "list_of_giveaway_channel" this channel will store all the giveaways found by the bot so you can track them.

- "list_of_running_account_channel" this channel will list all the running accounts so you can see when they run.

- "list_of_account_time_statistics" this channel will list the current status of the running process and it will list number of accounts who have already run.
At the end of the running process it will do a summary of all the giveaways done today and all the giveaways done since day 1 and it will also display how long it took to run the whole thing.

- "new_dm_channel" this channel will send a picture of the dm of an account if he got a new dm and possibly won a new giveaway.

- "list_of_login_error_channel" this channel will send a message if an account failed to login with the name of the account.

- "giveaway_won_channel" this channel will send a message if one of your account have won a giveaway.




## How to add accounts?

To add new accounts just copy and paste src/bot_folder to src and it should make something like src/bot_folder_copy then just rename it with your twitter account name.

For exmple it could be src/bob458us

## Configuration file for each accounts

This configuration file is simple and small it contain only 2 parameters account username and account password.

To add account just fill account_username and account_password with the username and password of the account you want to add

```yml
#Account info write the username of all account
account_username:
  - "test1234"

#Account info write the password of all account
account_password:
  - "twitter1234"
```


## Global configuration file
The most important features can be adjust on the configuration.yml file on the root of the project.

This configuration file contain all the important parameters of the project.

Since all accounts to the same giveaway those parameters would be shared for all accounts.

Here are some parameters that need to be explained:

If you don't want to do giveaway about a certain "topic" just add the "topic" to the giveaway to blacklist

```yml
# We don't want to participate in giveaway with these words
giveaway_to_blacklist:
  - "crypto"
  - "bitcoin"
  - "nft"
```

If you don't want to do random tweet and retweet just set random_retweet_and_tweet to False but if you do want to do them just set the value to True and put the number of reetweet and tweet you want to do

```yml
# If the value is set to true the bot will make random retweet and tweet
random_retweet_and_tweet: True

# The number of random retweet to do
random_retweet_nb: 1
```

You can also specify the number of giveaways you want to do, the number of like and retweet the giveaway must have and the limit date of a giveaway to not participate on older and finished giveaway

```yml
# Minimum of like the tweet must have
minimum_like: 10

# Minimum of reetweet the tweet must have
minimum_rt: 500

#Maximum day for a giveaway to be done
maximum_day: 14

#Number of giveaway the bot can do
nb_of_giveaway: 50
```

You can also add date_keyword those word are words used to tell when a giveaway will end it would help the bot skip giveaway if the draw date is already over

```yml
# Keyword that will be used to check if a giveaway is alread over or no

date_keyword:

- "Contest ends on"
- "Announced in"
- "Contest ends"
- "Drawed on"
- "Draw"
```


There are more information on the configuration.yml file but those are easier to understand.

If you are not a french speaker or you want to do english, spanish or any language giveaways read this otherwise skip it.

If you set your configuration.yml well you will be able to do giveaways that are not necessarily french just do it like that:

for the exemple let's say you want to do english giveaways

Change the tweet_lang to en or any It will either search for english tweet only or tweet of any language

```yml
# The language of the tweet to search fr,en etc put any if you want to search tweet in any language
tweet_lang: "en"
```

After that add your own word to the words_to_search list like this it will search giveaways which contain those words

```yml
# Words to search for giveaway
words_to_search:
  - "giveaway"
  - "win"
  - "contest"

```

Then you just need to modify the comment/tag list

On this list add the words that are asked when you need to comment a certain thing like if giveaways often ask "comments Done or comments #Winner" then add the word comments to the list 

```yml
# Those are the words needed on the tweet for the bot to comment when the tweet ask to comment one thing in particular
word_list_to_check_for_special_comment:
  - "comments"
```

On this list add the same word as word_list_to_check_for_special_comment but only add words that will be skip if the bot need to check for a random comment


```yml
# Those are the word needed on the tweet for the bot to comment but we won't lookup for a random comment to copy for those words:
word_list_to_not_check_for_copy:
  - "+ #"
  - "with #"
  - "add #"
```

On this list add the word that are asked when you need to comment on the giveaway but not necessarily anything special like if the giveaway says "comments to enter the giveaway" then add the words comments to the list

```yml
# Those are the word needed on the tweet for the bot to comment when the tweet ask to comment random stuff
word_list_to_check_for_comment:
  - "comment"
```

This list do the same things that word_list_to_check_for_comment but for word shorter than 6 characters

```yml
# The same as word_list_to_check_for_comment but for word shorter than 6 characters
short_word_list_to_check_for_comment:
  - "say"
  - "tell"
```

On this list add the word that are asked when you need to tag one or more accounts to a giveaway 
```yml
# Those are the word needed on the tweet for the bot to tag one or more account
word_list_to_check_for_tag:
  - "tag"
  - "mention"
```

Add to this list word asked when you only need to tag 1 account to enter the giveaway

```yml
# Word list to check if we need to tag 1 account
one_poeple_list:
  - "one friend"
  - "a friend"
  - "@ someone"
  
```

Add to this list word asked when you only need to tag 2 accounts to enter the giveaway

```yml
# Word list to check if we need to tag 2 accounts
two_poeple_list:
  - "two friends"
  - "two persons"
```

Add to this list word asked when you need to tag 3 or more accounts to enter the giveaway

```yml
# Word list to check if we need to tag 3 accounts or more
three_or_more_poeple_list:
  - "three friends"
  - "three persons"
  - "some friends"
```

With all of that you will be able to do giveaway in english or any language you want

## Advices  

- Don't do more than 50 giveaways otherwise this could get your account locked for doing to much likes and retweets in short time

- To have the best answer possible when the bot need to comment you have to add as many keywords as possible in word_list_to_check_for_special_comment,word_list_to_check_for_comment,short_word_list_to_check_for_comment list

- To avoid getting blocked for ban it's better to do giveaways during day time and not the night to act more human
- Fell free to modify as you wish the configuration.yml file to have the best giveaway bot you want
- Fell free to update the code or even add more features to it.

Hope this code will help you win more giveaways on twitter.

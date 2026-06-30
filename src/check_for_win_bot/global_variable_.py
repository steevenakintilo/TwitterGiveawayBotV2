"""Global variable file"""

# pylint: disable-all

# List of url

TWITTER_LOGIN_PAGE_URL = "https://x.com"
TWEET_TO_SEE_AFTER_LOGIN = "https://x.com/Holtadjust/status/2063281449898274862"
DM_PAGE = "https://x.com/i/chat"
SEARCH_TWEET_URL = "https://x.com/explore"

# Element Attribute

USERNAME_OR_EMAIL_ATTRIBUTE = "#jf-input-username_or_email"
PASSWORD_ATTRIBUTE = "#jf-input-password"
BUTTON_SUBMIT_ATTRIBUTE = "button[type=submit]"
BUTTON_SUBMIT_ATTRIBUTE2 = 'xpath=//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/form/div[2]/div/button'
ACCEPT_COOKIE_ATTRIBUTE = 'xpath=//*[@id="layers"]/div/div[3]/div/div/div/div[2]/button[1]'
LIKE_A_TWEET_ATTRIBUTE = '[data-testid="like"]'
UNLIKE_A_TWEET_ATTRIBUTE = '[data-testid="unlike"]'
RETWEET_A_TWEET_ATTRIBUTE = '[data-testid="retweet"]'
UNRETWEET_A_TWEET_ATTRIBUTE = '[data-testid="unretweet"]'
RETWEET_CONFIRM_ATTRIBUTE = '[data-testid="retweetConfirm"]'
UNRETWEET_CONFIRM_ATTRIBUTE = '[data-testid="unretweetConfirm"]'
COMMENT_A_TWEET_ATTRIBUTE = '[data-testid="reply"]'
COMMENT_TEXTBOX_ATTRIBUTE = '[data-testid="tweetTextarea_0"]'
POST_A_TWEET_BUTTON_ATTRIBUTE = '[data-testid="tweetButton"]'
FOLLOW_AN_ACCOUNT_ATTRIBUTE = 'xpath=//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div[1]/div/div[1]/div[2]/div/div[1]/button/div/div/span/span'
UNFOLLOW_AN_ACCOUNT_ATTRIBUTE = 'xpath=/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/button[3]'
UNFOLLOW_AN_ACCOUNT_CONFIRM_ATTRIBUTE = 'xpath=//*[@id="layers"]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div'
EDIT_PROFILE_ATTRIBUTE = '[data-testid="editProfileButton"]'
MAKE_A_POST_ATTRIBUTE = '[data-testid="SideNav_NewTweet_Button"]'
FORGOT_PIN_ATTRIBUTE = '[data-testid="pin-forgot-pin"]'
CREATE_A_PASSCODE_ATTRIBUTE = '[data-testid="pin-onboarding-setup-now"]'
CODEPASS_TEXTBOX_ATTRIBUTE = '[data-testid="pin-code-input-container"]'
CODEPASS_BUTTON_ATTRIBUTE_LIST = [
    'xpath=//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]'
    'xpath=//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]',
    'xpath=//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]',
    'xpath=//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[4]',
]
NEW_DM_ATTRIBUTE = 'xpath=//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[4]/div/div/div'
OTP_CODE_TEXTBOX_ATTRIBUTE = 'xpath=//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/form/div[1]/div[2]/div[2]/div/div/div/div[2]/div/div/fieldset/div'
#UNLOCK_MORE_BUTTON_ATTRIBUTE = 'xpath=//*[@id="layers"]/div[3]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/button/div'
UNLOCK_MORE_BUTTON_ATTRIBUTE = 'xpath=//*[@id="layers"]/div[3]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/button'
COMMENT_A_POST_ATTRIBUTE = "input[data-testid='fileInput']"
SEARCHBOX_ATTRIBUTE = "input[data-testid='SearchBox_Search_Input']"
TWEET_ATTRIBUTE = "[data-testid='tweet']"

# Variable

WAIT_TIME_BEFORE_TIMEOUT = 1

# LIST_OF_WIN_KEYWORD = """remporte le concours
# remporte le concours
# Félicitations au gagnant
# Félicitations aux gagnants
# gagnants
# gagnant
# qui gagne
# il gagne
# tu gagnes
# congrats
# Félicitation
# Félicitations
# gg à
# twitterpicker
# winners 
# winner
# bravo
# lot
# remporte
# qui win 
# a win
# qui gagne
# Félicitation!
# Félicitation!!
# 🏆
# winners 🏆
# XPicker""".lower().split("\n")



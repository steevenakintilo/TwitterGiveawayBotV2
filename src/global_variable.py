"""Global variable file"""

# pylint: disable-all

# List of url

TWITTER_LOGIN_PAGE_URL = "https://x.com"
TWEET_TO_SEE_AFTER_LOGIN = "https://x.com/Holtadjust/status/2063281449898274862"

# Element Attribute

USERNAME_OR_EMAIL_ATTRIBUTE = "#jf-input-username_or_email"
PASSWORD_ATTRIBUTE = "#jf-input-password"
BUTTON_SUBMIT_ATTRIBUTE = "button[type=submit]"
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

# Variable

WAIT_TIME_BEFORE_TIMEOUT = 1

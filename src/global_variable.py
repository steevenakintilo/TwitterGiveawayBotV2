"""Global variable file"""

# pylint: disable-all

# List of url

TWITTER_LOGIN_PAGE_URL = "https://x.com"
TWEET_TO_SEE_AFTER_LOGIN = "https://x.com/Holtadjust/status/2063281449898274862"
DM_PAGE = "https://x.com/i/chat"

# ---
CHANGE_PASSWORD_PAGE = "https://x.com/settings/password"
CHANGE_USERNAME_PAGE = "https://x.com/settings/screen_name"
CHANGE_PROFILE_PAGE = "https://x.com/settings/profile"
CHECK_IF_ACCOUNT_IS_PRIVATE_PAGE = "https://x.com/settings/audience_and_tagging"
CHANGE_LANGUAGE_PAGE = "https://x.com/i/flow/uls_content_and_app_language_selector"

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


# ---
CONFIRM_PASSWORD_ATTRIBUTE = '[name="current_password"]'
CHOOSE_NEW_PASSWORD_ATTRIBUTE = '[name="new_password"]'
CONFIRM_NEW_PASSWORD_ATTRIBUTE = '[name="password_confirmation"]'
SAVE_SETTING_BUTTON_ATTRIBUTE = '[data-testid="settingsDetailSave"]'
SUBMIT_BUTTON_ATTRIBUTE = 'xpath=//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div[4]/button'
CHANGE_USERNAME_ATTRIBUTE = '[name="typedScreenName"]'
CHANGE_NAME_ATTRIBUTE = '[name="displayName"]'
CHANGE_BIO_ATTRIBUTE = '[name="description"]'
CHANGE_LOCATION_ATTRIBUTE = '[name="location"]'
SAVE_PROFILE_BUTTON_ATTRIBUTE = '[data-testid="Profile_Save_Button"]'
CHANGE_PICTURE_ATTRIBUTE = "input[data-testid='fileInput']"
CONFIRM_NEW_PICTURE_ATTRIBUTE = '[data-testid="applyButton"]'
PRIVATE_ACCOUNT_BUTTON_ATTRIBUTE = 'xpath=//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div[2]/div/div/label'
PRIVATE_ACCOUNT_BUTTON_OBJ = 'xpath=//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div/div/span/span[2]/span/span/div/button'
CHOOSE_LANGUAGE_INPUT_ATTRIBUTE = '[data-testid="ChoiceSelectionInput"]'
CHANGE_LANGUAGE_BUTTON_ATTRIBUTE = 'xpath=//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[3]/div[1]/label/div/div[1]'
CURRENT_LANGUAGE_ATTRIBUTE = 'xpath=//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div[1]/label/div/div[1]'
SUBMIT_NEW_LANGUAGE_ATTRIBUTE = '[data-testid="ChoiceSelectionNextButton"]'
# Variable

WAIT_TIME_BEFORE_TIMEOUT = 1

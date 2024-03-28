import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from time import sleep
from datetime import datetime

option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

option.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 2, 
    "profile.default_content_setting_values.notifications": 1 
  })


with open("config.json") as file:
    config = json.load(file)

driver = webdriver.Chrome(chrome_options=option, executable_path=config['chrome_driver_linux'])

email = config['fpt_email']
password = config['fpt_password']

def generate_meetings(filename):
    
    meeting_list = open(filename)
    meetings = meeting_list.readlines()
    meetings = meetings[1:]
    meetings = [link[:-1] for link in meetings]

    meeting_dict = dict()

    for info in meetings:
        info = info.split("|")
        time = info[0].strip()
        link = info[1].strip()
        meeting_dict[time] = link

    time_list = list(meeting_dict.keys())

    return time_list, meeting_dict

time_list, meeting_dict = generate_meetings(filename='meeting_list.txt')

def login_google_account(email, password):

    driver.get("https://accounts.google.com/signin/v2/identifier?service=accountsettings&continue=https%3A%2F%2Fmyaccount.google.com%3Futm_source%3Daccount-marketing-page%26utm_medium%3Dgo-to-account-button&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

    email_box = driver.find_element_by_id("identifierId")
    email_box.click()
    email_box.send_keys(email)
    
    next_button = driver.find_element_by_class_name("VfPpkd-vQzf8d")
    next_button.click()

    sleep(2)

    password_box = driver.find_element_by_xpath("//input[@class='whsOnd zHQkBf']")
    password_box.click()
    password_box.send_keys(password)

    next_button = driver.find_element_by_class_name("VfPpkd-vQzf8d")
    next_button.click()

    sleep(2)

def login_google_meet():

    driver.get("https://meet.google.com/vbo-bjbv-iwv")

    microphone_button = driver.find_element_by_xpath("//div[@class='U26fgb JRY2Pb mUbCce kpROve uJNmj QmxbVb HNeRed M9Bg4d']")
    microphone_button.click()

    webcam_button = driver.find_element_by_xpath("//div[@class='U26fgb JRY2Pb mUbCce kpROve uJNmj QmxbVb HNeRed M9Bg4d']")
    webcam_button.click()

    sleep(2)

    join_button = driver.find_element_by_xpath("//span[@class='NPEfkd RveJvd snByac']")
    join_button.click()

while True:
    now = datetime.now()
    dt_now = now.strftime("%H:%M:%S")
    for time in time_list:
        if time == dt_now:
            login_google_account(email=email, password=password)
            login_google_meet()
        else:
            continue

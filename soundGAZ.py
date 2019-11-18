# Imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

# user-defined URL of profile

# EXAMPLE: "https://soundgasm.net/u/USERNAME"
url = "<- Paste https://soundgasm.net/u/ user profile link here ->"

# username extraction for folder creation
userSplit = url.split("/")
user = userSplit[-1]

try:
    make_Command = "mkdir {0}".format(user)
    os.system(make_Command)
except Exception as e:
    print(e)
    pass

#  driver options boilerplate #

# options for webdriver
options = Options()
options.add_argument("--headless")
# options.add_argument("--window-size=192x108")
options.add_argument("user-data-dir=selenium")

# options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # automation detection evasion
options.add_experimental_option('useAutomationExtension', False)  # automation detection evasion

driver = webdriver.Chrome(options=options, executable_path="./sel_driver/chromedriver")
driver.set_page_load_timeout(60)
print("Loading...")

####################################################################################

# variable set up
name = "unspecified"
title = "unspecified"
link = "unspecified"
try:
    # profile get
    driver.get(url)
    # media posts extraction
    for sound_link in driver.find_elements_by_xpath('/html/body/div[*]/a'):
        sound_link.get_attribute("href")
        print(sound_link.get_attribute("href"))
        print(sound_link.get_attribute("href"), file=open("raw.txt", "a"))
except Exception as e:
    print(e)
    pass

##############################################################################
url = ""

f = open("raw.txt")
links = f.read().splitlines()

# content download Loop
for link_line in links:
    if link_line != "":

        print(link_line)
        url = link_line
        # variable Flushing
        name = ""
        title = ""
        link = ""

        # main driver get for media page
        try:
            driver.get(url)
            time.sleep(2)  # slow your roll let it load
        except Exception as e:
            print(e)
            pass
        # account name extraction
        try:
            name = driver.find_element_by_xpath('/html/body/div[1]/a', ).text.replace("'", "").replace('"', "").replace(
                '/', " ").replace('*', " ")
            print(name)
        except Exception as e:
            print(e)
            pass
        # Title creation
        # Using this method we leverage the websites title character stripping instead of doing it ourselves.
        try:
            url_split = url.split("/")
            title = url_split[-1].replace("-", " ")  # make pretty
            print(title)
        except Exception as e:
            print(e)
            pass
        # extracting media link
        try:
            link = driver.find_element_by_xpath('//*[@id="jp_audio_0"]').get_attribute("src")
            print(link)
        except Exception as e:
            print(e)
            pass
        # command generation and execution
        try:
            w_Get_command = "wget {0} -c -O './{1}/{2} {3}.m4a'".format(link, user, name, title)
            print(w_Get_command)
            os.system(w_Get_command)
        except Exception as e:
            print(e)
            pass

    else:
        pass


# clean up

driver.quit()
# zeroing out file
open("raw.txt", 'w').close()

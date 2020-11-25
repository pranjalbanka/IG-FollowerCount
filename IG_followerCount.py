'''
Made by Pranjal Banka (@banka.pranjal)

This is an instagram scrapper that returns the follower count of all profiles(stored in the profiles.txt file)

Enter the username of all profiles in the profiles.txt file.
Enter your login credentials into the login.txt file


Future Updates:
- Store data generated into xlsx or csv file.
- plot the data stored.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
from datetime import date

import pandas as pd
from openpyxl import Workbook

#instagram requires you to login, or you may not be able to scrape after a while
driver = webdriver.Chrome()
driver.get("https://www.instagram.com/accounts/login/")


#read from the login.txt file to get the username and password
loginTxt = open("login.txt", "r")
login = loginTxt.read().split('\n')
#remove any empty lines
while("" in login) : 
    login.remove("") 

loginUsername = login[0]
loginPassword = login[1]

#wait till the login input field is located
try:
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input")))
except TimeoutException:
	print("Loading took too much time!")

#input the login credentials 
inputUsername = driver.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input")
inputUsername.send_keys(loginUsername)

inputPassword = driver.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input")
inputPassword.send_keys(loginPassword)

#find the login button and click it
loginButton = driver.find_element_by_xpath("//*[@id='loginForm']/div/div[3]/button")
loginButton.click()

#wait till we are fully logged in. Else the program may quit prematurely.
try:
    myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]")))
except TimeoutException:
    print("Loading took too much time!")


#read the profiles from the profiles.txt file, whose follower count is to be deteremined
profilesTxt = open("profiles.txt", "r")
profiles = profilesTxt.read().split('\n')
while("" in profiles) : 
    profiles.remove("") 

#base url
base = "https://www.instagram.com/"

#loop through all profiles.
for profile in profiles:
	#link of each profile
	link = base+profile
	driver.get(link)
	followers = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title")
	#remove commas from the numbers
	followers = followers.replace(",","")
	#convert string to int[if any operations need to be carried out on it later]
	followers = int(followers)
	print(followers)

driver.close()

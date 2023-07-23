from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time
import pandas as pd

l = list()
o = {}

target_url = "https://www.glassdoor.com/Job/data-science-jobs-SRCH_KO0,12.htm?clickSource=searchBox"

options = webdriver.ChromeOptions()

driver = webdriver.Chrome()

driver.get(target_url)

driver.maximize_window()
time.sleep(2)

resp = driver.page_source

nextButton = driver.find_element(By.CLASS_NAME, "nextButton")
# ActionChains(driver)\
#     .scroll_to_element(nextButton)\
#     .perform()
# time.sleep(2)
nextButton.click()
time.sleep(2)

resp += driver.page_source


driver.close()

soup = BeautifulSoup(resp, 'html.parser')

allJobsContainer = soup.find("ul", {"class": "css-7ry9k1"})
allJobs = allJobsContainer.find_all("li")

for job in allJobs:
    try:
        o["name-of-company"] = job.find("div",
                                        {"class": "d-flex align-items-center"}).text
    except:
        o["name-of-company"] = None
    try:
        o["name-of-job"] = job.find("div", {"class": "job-title mt-xsm"}).text
    except:
        o["name-of-job"] = None
    try:
        o["location"] = job.find("div", {"class": "location mt-xxsm"}).text
    except:
        o["location"] = None
    try:
        o["salary"] = job.find("div", {"class": "salary-estimate"}).text
    except:
        o["salary"] = None
    l.append(o)
    o = {}

print(l)

df = pd.DataFrame(l)
df.to_csv('jobs.csv', index=False, encoding='utf-8')

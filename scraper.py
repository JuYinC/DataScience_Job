# -*- coding: utf-8 -*-
"""

author: Kenarapfaik
url: https://github.com/arapfaik/scraping-glassdoor-selenium
"""
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with
import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose, slp_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome()
    driver.set_window_size(1120, 1000)

    keyword = keyword.replace(" ", "-")
    key_len = len(keyword)

    url = f"https://www.glassdoor.com/Job/{keyword}-jobs-SRCH_KO0,{key_len}.htm"
    #url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    #url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    # If true, should be still looking for new jobs.
    while len(jobs) < num_jobs:

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        # Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(By.CLASS_NAME, "selected").click()
            #WebDriverWait(driver, 3).until(driver.find_element(By.CLASS_NAME,"actionBarMt0").click())
        except ElementClickInterceptedException:
            pass

        time.sleep(3)

        try:
            # clicking to the X.
            driver.find_element(By.CLASS_NAME, "e1jbctw80").click()
            print(' x out worked')
        except NoSuchElementException:
            print(' x out failed')
            pass

        # Going through each job in this page
        # jl for Job Listing. These are the buttons we're going to click.
        job_buttons = driver.find_elements(By.CLASS_NAME, "jobCard")

        for job_button in job_buttons:

            print("Progress: {}".format(
                "" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  # You might
            # driver.find_element(By.CLASS_NAME,'jobCard').click()
            time.sleep(5)
            #collected_successfully = False

            # while not collected_successfully:
            try:

                location = job_button.find_element(
                    By.CLASS_NAME, 'location').text
                job_title = job_button.find_element(
                    By.CLASS_NAME, 'job-title').text
                company_name = job_button.find_element(
                    By.CSS_SELECTOR, 'div[target="_blank"]').text
                #collected_successfully = True
            except:
                time.sleep(3)

            try:
                salary_estimate = job_button.find_element(
                    By.CLASS_NAME, 'salary-estimate').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            # try:
            #     rating = job_button.find_element(By.CLASS_NAME,'job-search-rnnx2x').text
            # except NoSuchElementException:
            #     rating = -1 #You need to set a "not found value. It's important."

            # Printing for debugging
            # if verbose:
            #     print("Job Title: {}".format(job_title))
            #     print("Salary Estimate: {}".format(salary_estimate))
            #     #print("Job Description: {}".format(job_description[:500]))
            #     print("Rating: {}".format(rating))
            #     print("Company Name: {}".format(company_name))
            #     print("Location: {}".format(location))

            # Going to the Company tab...
            # clicking on this:
            # <div class="tab" data-tab-type="overview"><span>Company</span></div>
            jdCol = driver.find_element(By.ID, 'JDCol')
            try:
                emp_info = jdCol.find_element(By.ID, 'EmpBasicInfo')

                try:
                    rating = jdCol.find_element(
                        By.CSS_SELECTOR, 'span[data-test="detailRating"]').text
                except NoSuchElementException:
                    rating = -1  # You need to set a "not found value. It's important."

                try:
                    size = emp_info.find_element(
                        By.XPATH, './/span[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = emp_info.find_element(
                        By.XPATH, './/span[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = emp_info.find_element(
                        By.XPATH, './/span[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = emp_info.find_element(
                        By.XPATH, './/span[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = emp_info.find_element(
                        By.XPATH, './/span[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = emp_info.find_element(
                        By.XPATH, './/span[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    # <div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    # </div>
                    jdCol.find_element(By.CLASS_NAME, 'e856ufb4').click()
                    time.sleep(5)
                    job_description = jdCol.find_element(
                        By.ID, 'JobDescriptionContainer').text
                except NoSuchElementException:
                    job_description = -1

            # Rarely, some job postings do not have the "Company" tab.
            except NoSuchElementException:
                job_description = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1

            # if verbose:
            #     print("Job Description: {}".format(job_description))
            #     print("Size: {}".format(size))
            #     print("Founded: {}".format(founded))
            #     print("Type of Ownership: {}".format(type_of_ownership))
            #     print("Industry: {}".format(industry))
            #     print("Sector: {}".format(sector))
            #     print("Revenue: {}".format(revenue))
            #     print("Competitors: {}".format(competitors))
            #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({
                "Job Title": job_title,
                "Salary Estimate": salary_estimate,
                "Company Name": company_name,
                "Location": location,
                "Job Description": job_description,
                "Rating": rating,
                "Size": size,
                "Founded": founded,
                "Type of ownership": type_of_ownership,
                "Industry": industry,
                "Sector": sector,
                "Revenue": revenue,
            })
            # add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element(By.CLASS_NAME, "nextButton").click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(
                num_jobs, len(jobs)))
            break

    # This line converts the dictionary object into a pandas DataFrame.
    return pd.DataFrame(jobs)

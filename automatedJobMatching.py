import os

import re

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Load login credentials from .env file, make sure to pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()
#put your own login credentials in the .env file 
#the 3 gloabal variables im this program that need customization
myUsername = os.getenv("MY_USERNAME")
myPassword = os.getenv("MY_PASSWORD")
regexPattern=r'\b(?:software|automat)\b' #

def initialize_driver():
    driver = webdriver.Chrome()
    driver.set_window_size(784, 816)
    driver.implicitly_wait(2)
    return driver

def login(driver, username, password):
    driver.get("https://mysuccess.carleton.ca/notLoggedIn.htm")
    time.sleep(2)
    
    driver.find_element(By.CSS_SELECTOR, "a:nth-child(4) strong").click()  # click students
    time.sleep(3)
    
    print(driver.title)
    
    userNameInput = driver.find_element(By.ID, "userNameInput")
    userNameInput.send_keys(username)
    
    driver.find_element(By.ID, "passwordInput").send_keys(password)
    driver.find_element(By.ID, "submitButton").click()
    
    time.sleep(2)


def navigate_to_coop_jobs(driver):
    driver.get("https://mysuccess.carleton.ca/myAccount/co-op/coopjobs.htm")
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "For My Program").click()
    time.sleep(2)


def navigate_to_job_page_number(driver, page_number):
    link_text = str(page_number)
    driver.find_element(By.XPATH, f"//a[@href='javascript:void(0)' and contains(text(), '{link_text}')]").click()
    time.sleep(3)


def open_job_links(driver):
    link_elements = driver.find_elements(By.XPATH, "//table[@id='postingsTable']//a[contains(@class, 'np-view-btn')]")
    return link_elements


def process_job_page(driver, link_element, pattern):
    ActionChains(driver).key_down(Keys.CONTROL).click(link_element).key_up(Keys.CONTROL).perform()
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    
    company_name = driver.find_element(By.XPATH,"//h2[contains(@class, 'h6') and contains(@class, 'mobile--small-font') and contains(@class, 'color--font--white') and contains(@class, 'margin--t--s') and contains(@class, 'align--start')]")
    position_title = driver.find_element(By.CLASS_NAME, "np-view-question--23")
    job_description = driver.find_element(By.CLASS_NAME, "np-view-question--32")
    applicationMethod= driver.find_element(By.XPATH,'//*[@id="postingDiv"]/div[2]/div[2]/table/tbody/tr[2]/td[2]')

    full_job_desc = f'{company_name.text} \n {position_title.text} \n {job_description.text} \n {applicationMethod.text}'
    
    result = re.search(pattern, full_job_desc, flags=re.IGNORECASE)
    
    #if result: saving all jobs for now
    save_job_description(full_job_desc, position_title.text)
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def save_job_description(description, file_name):
    folder_path = os.path.join(os.getcwd(), 'allJobs')  # Save in the current working directory
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Create the directory if it doesn't exist
    
    file_name = file_name.replace(' ', '_').replace('/', '')
    file_path = os.path.join(folder_path, f"{file_name}.txt")
    
    with open(file_path, 'w') as file:
        file.write(description)
    
    print(f"The job description has been saved to {file_path}")


def main():
    driver = initialize_driver()
    login(driver, myUsername, myPassword)
    navigate_to_coop_jobs(driver)
    
    # for page_number in range(1, 4):  # Assuming you want to navigate pages 1 to 3
    navigate_to_job_page_number(driver, 3)
    link_elements = open_job_links(driver)
    
    for link_element in link_elements:
        process_job_page(driver, link_element, regexPattern)  #change the regex patern global variable to tailor search
    
    print("All relevent jobs from page 1 have been searched and extracted successfully")
    driver.quit()

if __name__ == "__main__":
    main()

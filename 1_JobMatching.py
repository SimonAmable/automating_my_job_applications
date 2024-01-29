import os

import re

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Load login credentials from .env file, make sure to pip install python-dotenv
from dotenv import find_dotenv,load_dotenv
load_dotenv(find_dotenv())



#put your own login credentials in the .env file 
#the 3 gloabal variables im this program that need customization
myUsername = os.getenv("MY_USERNAME")
myPassword = os.getenv("MY_PASSWORD")
regexPattern=r'\b(?:devOPS|auto|Automation|java|web development|python|javascript)\b' #
#more user facing approad with input
def InputInfo():
    username=input("Please enter your Carleton username")
    password=input("Please enter your Carleton username")
    regexInput=input("Please enter the full regex expression you would like to use (do not include quotes ex. \")")
    return [username,password,regexInput]

def JobToID(job_position:str)->str:
    invalid_chars = set('/\\?%*:|"<>')#CREATE A SET FOR THE BAD WINDOWS FILE NAME CHARACTER
    jobWithValidCharacters= [char for char in job_position if char not in invalid_chars]

    returnString=""
    for s in jobWithValidCharacters:
        returnString +=s
    return returnString

   



# def get_valid_filename_chars(filename:str) ->str:
#     invalid_chars = set('/\\?%*:|"<>')
#     return [char for char in filename if char not in invalid_chars]

#     #invalid_chars.union(set([chr(i) for i in range(32)]))
#     #invalid_chars.union(set(['\x00']))


# def recursive_to_valid_characters(string:str)->str:
#     if string == "":
#         return ""
#     charCode=ord(string[0])

#     if  65 <= charCode <= 90 or (97 <= charCode <= 122 ) or (charCode == 32): #keep (uppercase, lower case, spaces, numbers)
#         return string[0] + recursive_to_valid_characters(string[1:])
    # else:
#       return recursive_to_valid_characters(string[1:])







def initialize_driver():
    driver = webdriver.Chrome()
    driver.set_window_size(784, 816)
    driver.implicitly_wait(10)
    return driver

def login(driver, username, password):
    driver.get("https://mysuccess.carleton.ca/notLoggedIn.htm")
    #time.sleep(2)
    
    #driver.find_element(By.CSS_SELECTOR, "a:nth-child(4) strong").click()  # click students
    studentLoginLink=WebDriverWait(driver,400).until(lambda x: x.find_element(By.CSS_SELECTOR, "a:nth-child(4) strong"))
    studentLoginLink.click()
    #time.sleep(3)
    
    print(driver.title)
    
    userNameInput=WebDriverWait(driver,400).until(lambda x: x.find_element(By.ID, "userNameInput"))
    userNameInput.send_keys(username)
    
    driver.find_element(By.ID, "passwordInput").send_keys(password)
    driver.find_element(By.ID, "submitButton").click()
    
    #time.sleep(2)


def navigate_to_coop_jobs(driver):
    driver.get("https://mysuccess.carleton.ca/myAccount/co-op/coopjobs.htm")
    JobPageSelectionChoosen=WebDriverWait(driver,400).until(lambda x: x.find_element(By.LINK_TEXT, "For My Program"))
    JobPageSelectionChoosen.click()
    #driver.find_element(By.LINK_TEXT, "For My Program").click()
    #time.sleep(2)

def navigate_to_job_page_number(driver, page_number):
    time.sleep(2)
    link_text = str(page_number)
    jobPageLink=WebDriverWait(driver,400).until(lambda x: x.find_element(By.XPATH, f"//a[@href='javascript:void(0)' and contains(text(), '{link_text}')]"))
    
    # Scroll to the element before clicking
    actions = ActionChains(driver)
    actions.move_to_element(jobPageLink).perform()
    #Click after scrolling
    jobPageLink.click()
    #driver.find_element(By.XPATH, f"//a[@href='javascript:void(0)' and contains(text(), '{link_text}')]").click()
    

def open_job_links(driver):
    time.sleep(2)
    link_elements = driver.find_elements(By.XPATH, "//table[@id='postingsTable']//a[contains(@class, 'np-view-btn')]")
    return link_elements

def process_job_page(driver, link_element, pattern):
    ActionChains(driver).key_down(Keys.CONTROL).click(link_element).key_up(Keys.CONTROL).perform()
    driver.switch_to.window(driver.window_handles[-1])
    company_name=WebDriverWait(driver,400).until(lambda x: x.find_element(By.XPATH,"//h2[contains(@class, 'h6') and contains(@class, 'mobile--small-font') and contains(@class, 'color--font--white') and contains(@class, 'margin--t--s') and contains(@class, 'align--start')]"))
    position_title = driver.find_element(By.CLASS_NAME, "np-view-question--23")
    job_description = driver.find_element(By.CLASS_NAME, "np-view-question--32")
    applicationMethod= driver.find_element(By.XPATH,'//*[@id="postingDiv"]/div[2]/div[2]/table/tbody/tr[2]/td[2]')

    full_job_desc = f'{company_name.text} \n {position_title.text} \n {job_description.text} \n {applicationMethod.text}'
    
    result = re.search(pattern, full_job_desc, flags=re.IGNORECASE)
    
    fileWillBeNamed=(position_title.text)#+company_name.text.replace(' ', '_').replace('/', '') ,we do replace in the save_job)description functiton
    if result:
    #saving all jobs for now
        save_job_description(full_job_desc, fileWillBeNamed)
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def save_job_description(description, position_title):
    folder_path = os.path.join(os.getcwd(), 'prospectJobs')  # Save in the current working directory
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Create the directory if it doesn't exist
    

    
    file_name = position_title.replace(' ', '_').replace('/', '').replace("-","_")
    fileNameID=JobToID(file_name)
    file_path = os.path.join(folder_path, f"{fileNameID}.txt")
    
    with open(file_path, 'w') as file:
        file.write(description)
    
    print(f"The job description has been saved to {file_path}")


def main():
    driver = initialize_driver()
    login(driver, myUsername, myPassword)
    navigate_to_coop_jobs(driver)
    
    # for page_number in range(1, 4):  # Assuming you want to navigate pages 1 to 3
    #page_number=1
    #we count page number and will loop
    tableNum=driver.find_elements(By.TAG_NAME, "table")
    print(f"number of tables: {len(tableNum)}")
    numberOfPages=len(tableNum)

    limit=0

    for page_number in range (1, numberOfPages+1):
        navigate_to_job_page_number(driver, page_number)
        link_elements = open_job_links(driver)
        
        for link_element in link_elements:
            process_job_page(driver, link_element, regexPattern)  #change the regex patern global variable to tailor search
    
        print(f"All relevent jobs from page {page_number} have been searched and extracted successfully")

    print("all coop jobs have been scrapped and saved succesfuly")
    driver.quit()

if __name__ == "__main__":
    main()

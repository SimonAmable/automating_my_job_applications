import os

import re

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Load login credentials from .env file, make sure to pip install python-dotenv
from dotenv import find_dotenv,load_dotenv
load_dotenv(find_dotenv())
#put your own login credentials in the .env file 
#the 4 gloabal variables im this program that may need customization
myUsername = os.getenv("MY_USERNAME")
myPassword = os.getenv("MY_PASSWORD")
#regexPattern=r'\b(?:software|automate|web|a)\b' #
# DIRECTORY CONTAINING FINISHED COVER LETTER FILES
finished_file_directory = "FinishedCoverLetters"



def JobToID(job_position:str)->str:
    invalid_chars = set('/\\?%*:|"<>')#CREATE A SET FOR THE BAD WINDOWS FILE NAME CHARACTER
    jobWithValidCharacters= [char for char in job_position if char not in invalid_chars]

    returnString=""
    for s in jobWithValidCharacters:
        returnString +=s
    return returnString



def initialize_driver():
    driver = webdriver.Chrome()
    driver.set_window_size(784, 816)
    driver.implicitly_wait(10)
    return driver

def login(driver, username, password):
    driver.get("https://mysuccess.carleton.ca/notLoggedIn.htm")
    
    studentLoginLink=WebDriverWait(driver,400).until(lambda x: x.find_element(By.CSS_SELECTOR, "a:nth-child(4) strong"))
    studentLoginLink.click()
    
    print(driver.title)
    
    #userNameInput = driver.find_element(By.ID, "userNameInput")
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
    time.sleep(1)
    link_text = str(page_number)
    jobPageLink=WebDriverWait(driver,400).until(lambda x: x.find_element(By.XPATH, f"//a[@href='javascript:void(0)' and contains(text(), '{link_text}')]"))
    
    # Scroll to the element before clicking
    actions = ActionChains(driver)
    actions.move_to_element(jobPageLink).perform()
    #Click after scrolling
    jobPageLink.click()
    #driver.find_element(By.XPATH, f"//a[@href='javascript:void(0)' and contains(text(), '{link_text}')]").click()
    

def open_job_links(driver):
    #link_elements=WebDriverWait(driver,400).until(lambda x: x.find_elements(By.XPATH, "//table[@id='postingsTable']//a[contains(@class, 'np-view-btn')]"))
    time.sleep(2)
    link_elements = driver.find_elements(By.XPATH, "//table[@id='postingsTable']//a[contains(@class, 'np-view-btn')]")
    return link_elements

def close_job_page(driver):
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2) #we should chnge this


def create_and_send_application_package(driver, job_name):
    print(f"create_application_package called for :{job_name}")

    #=================== click CREATE APPLICATION PACKAGE document
    #uploadDocBut=WebDriverWait(driver,400).until(driver.presence_of_element_located(By.XPATH,"//input[@value='customPkg']"))
    uploadDocBut2=WebDriverWait(driver,400).until(lambda x: x.find_element(By.XPATH,"//input[@value='customPkg']"))
       
    #uploadDocumentButton1=driver.find_element(By.XPATH,"//input[@value='customPkg']")
    uploadDocBut2.click()
    time.sleep(10)

    # ============ we are now on the CREATE APPLICATION page
    #  pakage name
    packageName=WebDriverWait(driver,400).until(lambda x: x.find_element(By.ID,"packageName"))
    #packageName=driver.find_element(By.ID,"packageName")
    packageName.send_keys(job_name)

    # ---- cover leter select ================TODO FIX THIS ONE
    coverLetterSelect=Select(driver.find_element(By.ID, "requiredInPackage4"))
    coverLetterSelect.select_by_index(1) #uploading the newest option in the select

    # ---- Resume select
    resumeSelect=Select(driver.find_element(By.ID, "requiredInPackage5"))
    resumeSelect.select_by_index(1)#uploading the newest option in the select

    # ---- Grades Page select
    gradePagesSelect=Select(driver.find_element(By.ID, "requiredInPackage6"))
    gradePagesSelect.select_by_index(1)#uploading the newest option in the select

    # ---SUBMIIT
    btnSubmit=driver.find_element(By.XPATH, "//input[@value='Submit Application']")
    btnSubmit.click()
    print (f"Application package has successufully SENT FOR : {job_name}, Good luck!")

    time.sleep(2)



def upload_cover_letter(driver, job_name, finished_file_directory):
    print(f"upload_cover_letter called on :{job_name} ")
    createNewPackageButton=WebDriverWait(driver,400).until(lambda x: x.find_element(By.XPATH,"//input[@value='customPkg']"))
    createNewPackageButton.click()
    time.sleep(3)

    upload_document_button = WebDriverWait(driver,400).until(lambda x: x.find_element(By.XPATH, "//a[normalize-space()='Click if you need to upload a new document']"))
    upload_document_button.click()
    time.sleep(3)

    doc_name_input = WebDriverWait(driver,400).until(lambda x: x.find_element(By.ID, "docName"))
    doc_name_input.send_keys(job_name)

    doc_type_select = Select(driver.find_element(By.ID, "docType"))
    doc_type_select.select_by_value("4")  # value 4 is cover letter

    file_upload = driver.find_element(By.ID, "fileUpload_docUpload")
    full_file_path = os.path.abspath(os.path.join(finished_file_directory, f"{job_name}.pdf"))
    file_upload.send_keys(full_file_path)
    time.sleep(5)

    submit_file_upload_form_btn = driver.find_element(By.ID, "submitFileUploadFormBtn")
    submit_file_upload_form_btn.click()
    print(f"upload_cover_letter SUCCESS FOR: {job_name}")
    print(f"Full file path of file upload from upload_cover_letter: {full_file_path}")

    time.sleep(3)

def handle_nokia_page(driver):
    #TODO you better beleive im getting the job
    driver.find_element()
    print("nokia page handles and closed")



def process_job_page(driver, link_element):
    ActionChains(driver).key_down(Keys.CONTROL).click(link_element).key_up(Keys.CONTROL).perform()
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(3)
    urlRegex= r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"
    company_name = driver.find_element(By.XPATH,"//h2[contains(@class, 'h6') and contains(@class, 'mobile--small-font') and contains(@class, 'color--font--white') and contains(@class, 'margin--t--s') and contains(@class, 'align--start')]")
    position_title = driver.find_element(By.CLASS_NAME, "np-view-question--23")
    job_description = driver.find_element(By.CLASS_NAME, "np-view-question--32")
    applicationMethod= driver.find_element(By.XPATH,'//*[@id="postingDiv"]/div[2]/div[2]/table/tbody/tr[2]/td[2]')

    full_job_desc = f'{company_name.text} \n {position_title.text} \n {job_description.text} \n {applicationMethod.text}'
    # ----turn jobs position into document name
    expectedDocumentName=(position_title.text).replace(' ', '_').replace('/', '').replace("-","_")
    documentName=JobToID(expectedDocumentName)
   
    #------------some conditionals to handle cases where we dont need to apply
    urlFound = re.search(urlRegex, full_job_desc, flags=re.IGNORECASE)

    if urlFound and not ("Use this system for applications" in applicationMethod.text):# if URL FOUND END , 
        print(f"url / External job application found")
        save_job_description(full_job_desc, documentName)
        close_job_page(driver)
        return
    #else we apply IF we find the appy button, 
    try:
        #time.sleep(5)
        #button_element = EC(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//body//main//div//div//div//div//div//div//button[@type='button'][normalize-space()='APPLY']"))))   
        button_element = WebDriverWait(driver,5).until(lambda x: x.find_element(By.XPATH, "//body//main//div//div//div//div//div//div//button[@type='button'][normalize-space()='APPLY']"))
        if button_element:
            print("WE FOUND A BUTTON !!")
        #button_element=driver.find_element(By.XPATH, "//body//main//div//div//div//div//div//div//button[@type='button'][normalize-space()='APPLY']")
    except :#handle no button
        print(f"NO apply button found for {documentName},  WE PROBABLY ALLREADY APPLIED")
        close_job_page(driver)
        return



    


    #TODO we should add a contains check for the applicationMethod to be more specific ""
    
    
    #check if we have cover letter and if we do, then apply
    allCoverLetters=os.listdir(finished_file_directory)

    allPdfCoverLetterFiles=[x for x in allCoverLetters if x.endswith(".pdf")]
    
    #print(allPdfCoverLetterFiles)
    pfddocName=f"{documentName}.pdf"
    if f"{documentName}.pdf" in allPdfCoverLetterFiles:
        print(f"A matching cover letter was found for : {pfddocName}")
        button_element.click() #Click Apply button 
        time.sleep(10)
        upload_cover_letter(driver, documentName,finished_file_directory)
        create_and_send_application_package(driver, documentName)
    else:#else we cancel and move on 
        print(f"document name ({documentName})  NOTTTTTT FOUNDD")
        close_job_page(driver)
        return

    
    if button_element:
        print ("we found a job we can apply for and we DID IT!")
    

    #APPLY TO JOB
        #TODO id job positions w company appended to end

    
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])






def save_job_description(description, file_title):
    folder_path = os.path.join(os.getcwd(), 'ExternalApplications')  # Save in the current working directory
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Create the directory if it doesn't exist
    
    file_name = file_title.replace(' ', '_').replace('/', '').replace("-","_")#just incase
    file_path = os.path.join(folder_path, f"{file_name}.txt")
    
    with open(file_path, 'w') as file:
        file.write(description)
    
    print(f"The job description has been saved to {file_path}")


def main():
    driver = initialize_driver() #initialize driver
    login(driver, myUsername, myPassword)# login to mySuccess
    navigate_to_coop_jobs(driver)
    #count pages
    tableNum=driver.find_elements(By.TAG_NAME, "table")
    print(f"number of tables: {len(tableNum)}")
    numberOfPages=len(tableNum)

    
    # for page_number in range(1, 4):  # Assuming you want to navigate pages 1 to 3
    for page_number in range (1, numberOfPages+1):
        navigate_to_job_page_number(driver, page_number)
        link_elements = open_job_links(driver)
        
        for link_element in link_elements:
            process_job_page(driver, link_element)#opens link and preforms operations on page, #change the regex patern global variable to tailor search
        
        print(f"All relevent jobs from page {page_number} have been searched and extracted successfully")
    
    print("Every job searched and saved successfully!!")
    driver.quit()

if __name__ == "__main__":
    main()

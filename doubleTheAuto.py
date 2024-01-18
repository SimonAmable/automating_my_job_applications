import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select 
#Expected conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


import time
from dotenv import load_dotenv


def filter_pdf_files(file_list):
    """
    Filter a list of filenames to include only those with a '.pdf' ending.

    Parameters:
    - file_list (list): List of filenames.

    Returns:
    - List containing only filenames ending with '.pdf'.
    """
    return [filename for filename in file_list if filename.lower().endswith('.pdf')]

def login_to_portal(driver,username, password):
    driver.get("https://mysuccess.carleton.ca/notLoggedIn.htm")
    time.sleep(2)
    driver.set_window_size(784, 816)
    driver.implicitly_wait(2)
    try:
        studentsButtons = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a:nth-child(4) strong')))
        studentsButtons.click()
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")
    
    #driver.find_element(By.CSS_SELECTOR, "a:nth-child(4) strong").click()
    #time.sleep(4)

    userNameInput = driver.find_element(By.ID, "userNameInput")
    userNameInput.send_keys(username)
    driver.implicitly_wait(2)

    driver.find_element(By.ID, "passwordInput").send_keys(password)
    driver.implicitly_wait(2)

    driver.find_element(By.ID, "submitButton").click()

    time.sleep(2)



def create_application_package(driver, job_name):
    print(job_name)

    #=================== click CREATE APPLICATION PACKAGE document
    time.sleep(1)

    uploadDocumentButton1=driver.find_element(By.XPATH,"//a[contains(text(), 'Create Application Package')]").click()
    driver.implicitly_wait(2)
    time.sleep(1)

    # ============ we are now on the CREATE APPLICATION page
    #  pakage name
    packageName=driver.find_element(By.ID,"name")
    packageName.send_keys(job_name)
    driver.implicitly_wait(2)

    # ---- cover leter select
    coverLetterSelect=Select(driver.find_element(By.ID, "4"))
    coverLetterSelect.select_by_visible_text(job_name)
    #allCoverLettersOnSite=coverLetterSelect.all_selected_options # CAN LOOP THROUGHT THIS list of cover letter on site already
    driver.implicitly_wait(2)

    # select by visible text allJobNames
    # print("all cover letters selections")
    # print (allCoverLetter)
    # ---- Resume select
    resumeSelect=Select(driver.find_element(By.ID, "5"))
    resumeSelect.select_by_visible_text("SimonAmableResumeV8")
    driver.implicitly_wait(2)

    # ---- Grades Page select
    gradePagesSelect=Select(driver.find_element(By.ID, "6"))
    gradePagesSelect.select_by_visible_text("RecordOfGradesV4")
    driver.implicitly_wait(2)
    # ---SUBMIIT
    btnSubmit=driver.find_element(By.ID, "btnSubmit")
    btnSubmit.click()
    print (f"Application package has successufully been created for : {job_name}")

    time.sleep(2)



def upload_cover_letter(driver, job_name, finished_file_directory):
    driver.get("https://mysuccess.carleton.ca/myAccount/co-op/coopdocs.htm")
    time.sleep(2)

    upload_document_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Upload Document')]").click()
    time.sleep(2)

    doc_name_input = driver.find_element(By.ID, "docName")
    doc_name_input.send_keys(job_name)
    driver.implicitly_wait(2)

    doc_type_select = Select(driver.find_element(By.ID, "docType"))
    doc_type_select.select_by_value("4")  # value 4 is cover letter
    driver.implicitly_wait(2)

    file_upload = driver.find_element(By.ID, "fileUpload_docUpload")
    full_file_path = os.path.abspath(os.path.join(finished_file_directory, f"{job_name}.pdf"))
    file_upload.send_keys(full_file_path)
    time.sleep(5)

    submit_file_upload_form_btn = driver.find_element(By.ID, "submitFileUploadFormBtn")
    submit_file_upload_form_btn.click()
    print(f"UPLOAD SUCCESS: {job_name}")
    print(f"Full file path: {full_file_path}")

    time.sleep(3)



def main():
    # CHANGE TO DOTENV BEFORE PUTTING ON GIT


    #DOT ENV for login credentials
    load_dotenv()
    my_username = os.getenv("MY_USERNAME")
    my_password = os.getenv("MY_PASSWORD")
    # ex of OPTION - IF YOU WANT TO OPEN WEBDRIVER WITH CHROME PROFILE, dont use with this script because we login
    # options = Options()
    # options.add_argument("user-data-dir=C:\\Users\\simon\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    driver = webdriver.Chrome()

    # MUST AUTHENTICATE AND SAVE LOGIN SESSION FOR YOUR ACCOUNT BEFORE RUNNING SCRIPT
    login_to_portal(driver, my_username, my_password)

    # DIRECTORY CONTAINING COVER LETTER FILES
    finished_file_directory = r"C:\Users\simon\Desktop\mycoolshit\SeleniumCoop\venvForSeleniumCoop\FinishedCoverLetters2"

    all_cover_letter_files = os.listdir(finished_file_directory)
    only_pdf_files = filter_pdf_files(all_cover_letter_files)
    all_job_names = [filename.replace(".pdf", "") for filename in only_pdf_files]

    print("All jobs with finished cover letter:")
    print(all_job_names)

    for job_name in all_job_names:
        upload_cover_letter(driver, job_name, finished_file_directory)
        create_application_package(driver, job_name)
        print(f"cover letter subbmitted and application package created successfully for {job_name}")


    print("ALLL successful!")
    driver.quit()


if __name__ == "__main__":
    main()

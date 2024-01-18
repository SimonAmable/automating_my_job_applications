import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv


class JobApplicationBot:
    def __init__(self):
        load_dotenv()
        self.myUsername = os.getenv("MY_USERNAME")
        self.myPassword = os.getenv("MY_PASSWORD")
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get("https://mysuccess.carleton.ca/notLoggedIn.htm")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(4) strong").click()
        time.sleep(3)
        self.driver.find_element(By.ID, "userNameInput").send_keys(self.myUsername)
        self.driver.implicitly_wait(1)
        self.driver.find_element(By.ID, "passwordInput").send_keys(self.myPassword)
        self.driver.implicitly_wait(1)
        self.driver.find_element(By.ID, "submitButton").click()
        self.driver.implicitly_wait(1)
        time.sleep(2)

    def navigate_to_jobs_page(self):
        self.driver.get("https://mysuccess.carleton.ca/myAccount/co-op/coopjobs.htm")
        time.sleep(3)
        self.driver.find_element(By.LINK_TEXT, "For My Program").click()
        time.sleep(2)

    def get_job_links(self):
        return self.driver.find_elements(By.XPATH, "//table[@id='postingsTable']//a[contains(@class, 'np-view-btn')]")

    def process_job(self, link_element):
        ActionChains(self.driver).key_down(Keys.CONTROL).click(link_element).key_up(Keys.CONTROL).perform()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(4)
        
        companyName = self.driver.find_element(By.XPATH,"//h2[contains(@class, 'h6') and contains(@class, 'mobile--small-font') and contains(@class, 'color--font--white') and contains(@class, 'margin--t--s') and contains(@class, 'align--start')]")
        positionTitle=self.driver.find_element(By.CLASS_NAME,"np-view-question--23")
        jobDescription= self.driver.find_element(By.CLASS_NAME,"np-view-question--32")
        applicationMethod= self.driver.find_element(By.XPATH,'//*[@id="postingDiv"]/div[2]/div[2]/table/tbody/tr[2]/td[2]')

        FullJobPostingInfo = f"{companyName} \n {positionTitle} \n {jobDescription.text} \n {applicationMethod} "

        #track list of jobs that need 2 step applications, there own company portals, may do those mannually or automate per site
        #get list of files from directory
        urlRegex= r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"

        urlRegexResult = re.search(urlRegex,FullJobPostingInfo,flags=re.IGNORECASE) 
        
        if urlRegex:
            return #end execultion
        
        






        # Your existing code for processing individual jobs goes here
        # ... all modified

    def apply_to_job(self, position_title, apply_button_xpath):
        # Your existing code for applying to jobs goes here
        # ...
        print("applying now")

    def teardown_method(self):
        self.driver.quit()

if __name__ == "__main__":
    job_bot = JobApplicationBot()
    job_bot.login()
    job_bot.navigate_to_jobs_page()

    job_links = job_bot.get_job_links() 
    print(f"Number of job positions found: {len(job_links)}")

    for link in job_links:
        job_bot.process_job(link)

    job_bot.teardown_method()

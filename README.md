# Automate-The-Job
# AutomateYourJobSearch
## Automating THE ENTIRE job applicaciton proccess on Carleton MySuccess with python, Selenium, OPENAI, and a few other libraries.

## Inspiration/Motivation:
- I was overwhelmed with the number of jobs listings avalible on the coop board at the start of this term and needed a solution. While suffering from too much imposter syndrome for me to send job applications efficiently i decided to code this instead.
-  To overcome this these 4 scripts will help you select your jobs based on keyword matching with regex, create custom cover letters, and of course apply to them faster than any human on earth! 
- If your struggling to get a job right now just keep working hard and it'll pay off eventually, I now have my first coop internship and it was worth it! :D
## Files:
- 1_JobMatching.py : This script will scape  all jobs on the MySuccess Coop board and extract all jobs matching a regex search into the directory "prospectJobs" for later use.
- 2_CoverLetterCustomization.py : This script uses the OPENAI api to resplace company name and job position in my cover letter. #Promt can be changed to anything.
- 3_CustomizeWordDocuments.py : This script uses the files from "TailoredCoverLetters" direcotry and outouts well typed/formated word documents, and their pdf counterparts into the  "FinishedCoverLetters" directory 
- 4_AutoApply.py  : This scirpt uses the finshed pdf cover letter in the "FinishedCoverLetters" directory and goes through all jobs on the coop board to find matching positions so that the file can be uploaded and the application package send. Edge cases where private comapny site was needed for registration handled manually, currenly Private application pages go into the "ExternalApplicaiton" directory 

## Paramaters to Customize:
- regexPattern
- MY_USERNAME (.env)
- MY_PASSWORD (.env)
- OPEN_AI_API_KEY (.env)
- coverLetter.txt    (# your own cover letter)

## Features:
- Automated login to university portal
- Navigation through co-op job pages
- Extraction of job information based on specified criteria, currently using regex but many alternative methods avalible
- Storage of relevant job information in text files

## Usage:
  - Set up a virtual environment, activate it,  and install dependencies from requirements.txt.
  - Create a .env file with your login credentials and OPENAI api key.
  - change the regex expression to match jobs you want to target
  - Run the scripts in order 1-4 and thats it!

## how to setup venv:
- python -m venv venv               # or python3, depending on your setup
- venv/bin/activate                 # or activate.bat on Windows
- pip install -r requirements.txt 
# Make sure you create a .env file with your information and can start with: 1_JobMatching.py


## Dependencies:
  - Python
  - Selenium
  - WebDriver (Chrome)
  - python-dotenv
  - python-docx
  - docx2pdf
    # 
  


## Note/Requirements:
  - global variables that need customization are at the top of the file
  - Make sure to customize the criteria(REGEX) in the first script to match your job preferences.
  - Job position name for files is changed to replace invalid characters 
  - global variables that need customization are at the top of the file
  - please enter your login credentionals into a dont env file with approriate varibles before running
  - regexPattern is a gloabal variable that will be used to file matching jobs
  - DO NOT OVER RELY ON GPT + doc formating without testing because gpt is not that good 


## Contributing:
Contributions are more that welcome! Feel free to open issues, submit pull requests, or suggest enhancements to make this tool more effective and user-friendly.
  -neccasary improvements:
    - fix jobs page navigation to scrapper each page (currently only does first 100 listing on page 1 of job board)
    - 



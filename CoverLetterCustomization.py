import os
import openai
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPEN_AI_API_KEY")


openai.api_key=api_key
# this code will replace all occurences of job poition and company name in my cover letter with an appropriate one from the prospectJobsDirectory
# 
# 
# 

# Function to send a request to ChatGPT API
def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(

    model=model,

    messages=messages,

    temperature=0,

    )

    return response.choices[0].message["content"]






def get_unique_elements(list1, list2):
    # Convert the lists to sets for efficient set operations
    set1 = set(list1)
    set2 = set(list2)

    # Get elements that are unique to each list
    unique_elements = list(set1.symmetric_difference(set2))

    return unique_elements



# Function to read a file and extract company name and job position
# Simple parse to get rid of job desciption
def extract_info_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        lines = content.split('\n')
        company_name = lines[0].strip()
        job_position = lines[1].strip()
        return company_name, job_position
        

# Function to replace content in the cover letter
# def replace_content(cover_letter, company_name, job_position):
#     cover_letter = cover_letter.replace("Ceridian Canada Ltd.", company_name)
#     cover_letter = cover_letter.replace("Software Developer Co-op - C++ (Switchers)", job_position)
#     return cover_letter


# Path to the directory containing .txt job files 
files_directory = r'C:\Users\simon\Desktop\mycoolshit\SeleniumCoop\venvForSeleniumCoop\prospectJobs'
out_directory=r"C:\Users\simon\Desktop\mycoolshit\SeleniumCoop\venvForSeleniumCoop\TailoredCoverLetters3"
# Path to your cover letter file
cover_letter_path = r'venvForSeleniumCoop\coverLetter.txt'



# Read the cover letter
with open(cover_letter_path, 'r') as cover_letter_file:
    cover_letter_content = cover_letter_file.read()

#filter for non created files
allTxtFiles=os.listdir(files_directory)
allAlreadMadeFiles=os.listdir(out_directory)


allPreviousCL=os.listdir(r"C:\Users\simon\Desktop\mycoolshit\SeleniumCoop\venvForSeleniumCoop\TailoredCoverLetters2")


allAlreadMadeFiles.extend(allPreviousCL)
# for name in allTxtFiles:
#     name=name.replace(".txt","")
for name in allAlreadMadeFiles:
    name=name.replace("modified_","")

NeedToBeMade=get_unique_elements(allAlreadMadeFiles,allTxtFiles)

absolute_paths = [os.path.abspath(file_path) for file_path in NeedToBeMade]




# Iterate through .txt files in the specified directory
for filename in NeedToBeMade: #get list of files from directory
    if filename.endswith('.txt') and not filename.startswith("modified"): 
        file_path = os.path.join(files_directory, filename)
        company_name, job_position = extract_info_from_file(file_path)

        prompt = f"""<can you replace all occurrences of company name and job position in my cover letter to the appropriate ones from this i will provide Job posting.
            Try to make the company name and position sound natural. 
            Please provide the output as only the input cover letter modified as asked in plain text with nothing else, Start at the first "Simon Amable" and end and the last "Simon Amable".
            But please DO NOT change any of the formatting, spacing, or newlines. only replace the content i asked for which is: ( Job Posting: Company name: {company_name} , job position:{job_position} ), Cover letter: {cover_letter_content}>"""

        response = get_completion(prompt)

        print(f"respose: {response}")

        # # Replace content in the cover letter
        # modified_cover_letter = replace_content(cover_letter_content, company_name, job_position)

        # # Send a request to ChatGPT API to further modify the cover letter
        # modified_cover_letter = chatgpt_request(modified_cover_letter)

        # # Save the modified cover letter to a new file
        # output_file_path = os.path.join(files_directory, f'modified_{filename}')
        # with open(output_file_path, 'w') as output_file:
        #     output_file.write(modified_cover_letter)

        # print(f'Modified cover letter for {company_name} - {job_position} saved to {output_file_path}')
        output_folder_path = r"C:\Users\simon\Desktop\mycoolshit\SeleniumCoop\venvForSeleniumCoop\TailoredCoverLetters3"
        file_name = job_position.replace(' ', '_').replace('/', '') #replace invalid caractors
        # Combine the folder path and file name to get the full file path
        file_path = os.path.join(output_folder_path, f'{file_name}.txt')
        os.makedirs(output_folder_path, exist_ok=True)  # Ensure the directory exists
        with open(file_path, 'w') as output_file:
            output_file.write(response)


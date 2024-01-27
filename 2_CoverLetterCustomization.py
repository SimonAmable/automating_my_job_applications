import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPEN_AI_API_KEY")

from openai import OpenAI

client = OpenAI(api_key=api_key)
#client.api_key=api_key#TODO IDK ABOUT THIS 

def get_completion(prompt):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0,#0 most specific/determinictic , 2 is most creative/random
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{prompt}"}
    ]
    )
    print(f"API Response: {completion}")

    print(completion.choices[0].message)
    return (completion.choices[0].message.content)
    


#This program should be used after automatedJobMatching.py, from the same directory
#This program will replace all occurences of job poition and company name in my cover letter with an specified one from the prospectJobsDirectory
# 
#TODO change to newer release of chatGPT api
#TODO modularize docx->pdf and run on txt file right away

# Function to send a request to ChatGPT API





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
prospect_files_directory = "prospectJobs" #prospect jobs txt colected previously
out_directory="TailoredCoverLetters" #output folder
# Path to your cover letter file
cover_letter_path = r'coverLetter.txt'



# Read the cover letter
with open(cover_letter_path, 'r') as cover_letter_file:
    cover_letter_content = cover_letter_file.read()

#--------------filter for non created files, if running for the first time you can remove this OPTIONAL
# allTxtFiles=os.listdir(prospect_files_directory)
# allAlreadMadeFiles=os.listdir(out_directory)


# allPreviousCL=[]
# allAlreadMadeFiles.extend(allPreviousCL)
# # for name in allTxtFiles:
# #     name=name.replace(".txt","")
# for name in allAlreadMadeFiles:
#     name=name.replace("modified_","")

# NeedToBeMade=get_unique_elements(allAlreadMadeFiles,allTxtFiles)

# absolute_paths = [os.path.abspath(file_path) for file_path in NeedToBeMade]
#----------------------------

allTxtFiles=os.listdir(prospect_files_directory)
print(f"all file names :{allTxtFiles}")

# Iterate through .txt files in the specified directory
for filename in allTxtFiles:
    if filename.endswith('.txt') : 
        file_path = os.path.join(prospect_files_directory, filename)
        company_name, job_position = extract_info_from_file(file_path)

        prompt = f"""<can you replace all occurrences of company name and job position in my cover letter to the appropriate ones from this i will provide Job posting,
            Try to make the company name and position sound natural by using abriviations in the body paragraphs when appropriate. 
            Please provide the output as only the input cover letter modified as asked in plain text with nothing else, Start at the first "Simon Amable" and end and the last "Simon Amable".
            But please DO NOT change any of the formatting, spacing, or newlines. only replace the content i asked for which is: ( Job Posting: Company name: {company_name} , job position:{job_position} ), Cover letter: {cover_letter_content}>"""

        response = get_completion(prompt)

        print(f"respose: {response}")

      

        # print(f'Modified cover letter for {company_name} - {job_position} saved to {output_file_path}')
        #output_folder_path = "TailoredCoverLetters"

        #file_name = (job_position).replace(' ', '_').replace('/', '').replace("-","_") #replace invalid caractors
        # Combine the folder path and file name to get the full file path
        file_path = os.path.join(out_directory, f'{filename}.txt')
        os.makedirs(out_directory, exist_ok=True)  # Ensure the directory exists
        with open(file_path, 'w') as output_file:
            output_file.write(response)


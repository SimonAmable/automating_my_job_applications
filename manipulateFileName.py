# #PROGRAM TO MANIPULATE FILE NAME FOR All CONTENTS OF A FOLDER

# import os

# # Path to the directory containing files
# directory_path = r'C:\Users\simon\Desktop\mycoolshit\SeleniumCoop\venvForSeleniumCoop\TailoredCoverLetters3'

# # Iterate through files in the directory
# for filename in os.listdir(directory_path):
#     # Check if the file doesn't already have the ".txt" extension
#     if filename.startswith('modified_'):
#         # Rename the file by adding the ".txt" extension
#         new_filename = filename.replace("modified_","")
#         old_filepath = os.path.join(directory_path, filename)
#         new_filepath = os.path.join(directory_path, new_filename)
#         os.rename(old_filepath, new_filepath)
#         print(f'Renamed: {filename} to {new_filename}')

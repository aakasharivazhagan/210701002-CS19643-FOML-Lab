# import g4f
# import sys
# import json

# def read_file_content(file_path):
#     print(file_path)
#     try:
#         with open(file_path, 'r') as file:
#             return file.read()
#     except FileNotFoundError:
#         print(f"Error: File not found at {file_path}")
#         sys.exit(1)
#     except Exception as e:
#         print(f"Error reading file: {e}")
#         sys.exit(1)

# # Hardcoded path to the external text file
# external_text_file_path_1 = './preprompts/preprompt_1.txt'
# external_text_file_path_2 = './preprompts/preprompt2.txt'

# # User-provided JSON data/
# user_json_data = sys.argv[1];
# # user_json_data = "[{\"role\": \"user\",\"content\": \"is there any age restriction to annal gandhi memorial award?\"}]"

# try:
#     # Parse the user-provided JSON string into a Python data structure
#     user_data = json.loads(user_json_data)
# except json.JSONDecodeError as e:
#     print(f"Error decoding user-provided JSON: {e}")
#     sys.exit(1)


# g4f.debug.logging = True  # Enable debug logging
# g4f.debug.version_check = False  # Disable automatic version checking
# print(g4f.Provider.Bing.params)  # Print supported args for Bing
# print(type(user_data))  # Ensure user_data is of the correct type

# # Read the content from the external text file
# external_content_1 = read_file_content(external_text_file_path_1)
# external_content_2 = read_file_content(external_text_file_path_2)
# # Create a new element to prepend to the user-provided list
# external_element_1 = {"role": "user", "content": external_content_1}
# external_element_2 = {"role": "user", "content" : external_content_2}
# # Combine the external element with the user-provided data
# data = [external_element_1] + [external_element_2] + user_data

# # Using automatic a provider for the given model
# ## Streamed completion
# response = g4f.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=data,
#     stream=True,
# )

# for message in response:
#     print(message, flush=True, end='')




import g4f
import sys
import json
import os

def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

# Hardcoded path to the folder containing external text files
external_files_folder = './preprompts'

# User-provided JSON data as a command line argument
user_json_data = sys.argv[1]

try:
    # Parse the user-provided JSON string into a Python data structure
    user_data = json.loads(user_json_data)
except json.JSONDecodeError as e:
    print(f"Error decoding user-provided JSON: {e}")
    sys.exit(1)

g4f.debug.logging = False  # Enable debug logging
g4f.debug.version_check = False  # Disable automatic version checking
# print(g4f.Provider.Bing.params)  # Print supported args for Bing
# print(type(user_data))  # Ensure user_data is of the correct type

# Iterate over each external file in the folder
for file_name in os.listdir(external_files_folder):
    file_path = os.path.join(external_files_folder, file_name)

    # Read the content from the external file
    external_content = read_file_content(file_path)

    # Create a new element to prepend to the user-provided list
    external_element = {"role": "user", "content": external_content}

    # Add the external element to the user_data
    user_data.append(external_element)

user_data.append({"role": "user", "content": user_json_data})
# Combine the user-provided data with the additional external elements
data = user_data

# Using automatic a provider for the given model
## Streamed completion
response = g4f.ChatCompletion.create(
    # model="gpt-3.5-turbo",
    model = "gpt-4",
    provider = g4f.Provider.Bing, 
    messages=data,
    stream=True,
)

for message in response:
    print(message, flush=True, end='')

# import json

# # Read the JSON file
# json_file_path = './Datasets/raw_data.json'

# with open(json_file_path, 'r') as json_file:
#     json_data = json.load(json_file)

# # Convert JSON object to string
# json_string = json.dumps(json_data)

# # Escape double quotes in the string
# escaped_string = json_string.replace('"', '\\"')
# final_string = f'"{escaped_string}"'
# # Write the escaped string to a text file
# txt_file_path = './preprompts/preprompt2.txt'

# with open(txt_file_path, 'w') as txt_file:
#     txt_file.write(final_string)

# print('Conversion complete. Check the output file at', txt_file_path)


import os
import json

def process_json_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    json_string = json.dumps(json_data)
    escaped_string = json_string.replace('"', '\\"')
    final_string = f'"{escaped_string}"'

    with open(output_file_path, 'w') as txt_file:
        txt_file.write(final_string)

def convert_json_files(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            process_json_file(input_file_path, output_file_path)

    print('converted and stored ---->>', output_folder)

input_folder_path = '../Datasets'
output_folder_path = '../preprompts'

convert_json_files(input_folder_path, output_folder_path)

import json
import os

with open('../Datasets/raw_data.json', 'r') as file:
    data = json.load(file)

chunk_size = 50
chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]


for i, chunk in enumerate(chunks):
    new_filename = f'../Datasets/preprompt_ds_{i + 1}.json'
    with open(new_filename, 'w') as new_file:
        json.dump(chunk, new_file, indent=2)

print(f"split into {len(chunks)} chunkas.")

os. remove(f'../Datasets/raw_data.json') 
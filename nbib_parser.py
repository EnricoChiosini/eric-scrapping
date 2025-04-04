import os
import pandas as pd


def parse_nbib(file_path):
    data = {"TI": [], "AU": [], "DP": [], "JT": [], "LA": [], "LID": [], "AB": []}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        current_entry = {key: "" for key in data.keys()}
        for line in file:
            if line.strip() == "":
                if any(current_entry.values()):
                    for key in data.keys():
                        data[key].append(current_entry[key].strip())
                    current_entry = {key: "" for key in data.keys()}
                continue
            
            for key in data.keys():
                if line.startswith(key + " - ") or line.startswith(key + "  - "):
                    if key == "AU":
                        current_entry[key] += line[len(key) + 3:].strip() + "; "
                    else:
                        current_entry[key] += line[len(key) + 3:].strip() + " "
                    break
    
    if any(current_entry.values()):
        for key in data.keys():
            data[key].append(current_entry[key].strip())
    
    return pd.DataFrame(data)

folder_path = 'temp'
concatenated_filename = 'concatenated.nbib'
concatenated_path = os.path.join(folder_path, concatenated_filename)

with open(concatenated_path, 'w', encoding='utf-8') as outfile:
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.nbib') and file_name != concatenated_filename:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write("\n")  # Adiciona quebra de linha entre os arquivos

for file_name in os.listdir(folder_path):
    if file_name.endswith('.nbib') and file_name != concatenated_filename:
        os.remove(os.path.join(folder_path, file_name))

df = parse_nbib(concatenated_path)

excel_output_path = os.path.join(folder_path, 'nbib_data.xlsx')
df.to_excel(excel_output_path, index=False)

csv_gz_output_path = os.path.join(folder_path, 'nbib_data.csv.gz')
df.to_csv(csv_gz_output_path, index=False, compression='gzip')
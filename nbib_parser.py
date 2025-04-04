import pandas as pd
import os

def parse_nbib(file_path):
    data = {"TI": [], "AU": [],"DP": [], "JT": [], "LA": [], "LID": [], "AB": []}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        current_entry = {key: "" for key in data.keys()}
        for line in file:
            if line.strip() == "":  
                if any(current_entry.values()):  
                    for key in data.keys():
                        data[key].append(current_entry[key].strip())
                    current_entry = {key: "" for key in data.keys()}
                continue
            
            # Verifica se a linha começa com um dos campos desejados
            for key in data.keys():
                if line.startswith(key + " - ") or line.startswith(key + "  - "):
                    if key == "AU":
                        current_entry[key] += line[len(key) + 3:].strip() + "; "
                    else:
                        current_entry[key] += line[len(key) + 3:].strip() + " "
                    break
    
    # Adiciona a última entrada, se necessário
    if any(current_entry.values()):
        for key in data.keys():
            data[key].append(current_entry[key].strip())
    
    return pd.DataFrame(data)

# Caminho da pasta contendo os arquivos .nbib
folder_path = 'scrap1'

# Lista para armazenar os DataFrames
dataframes = []

# Itera sobre todos os arquivos na pasta
for file_name in os.listdir(folder_path):
    if file_name.endswith('.nbib'):  # Verifica se o arquivo tem a extensão .nbib
        file_path = os.path.join(folder_path, file_name)
        df = parse_nbib(file_path)  # Faz o parse do arquivo e cria o DataFrame
        dataframes.append(df)

# Concatena todos os DataFrames em um único DataFrame
df = pd.concat(dataframes, ignore_index=True)

# Salva os dados em um arquivo CSV na mesma pasta 'scrap1'
# Salva os dados em um arquivo Excel na mesma pasta 'scrap1'
excel_output_path = os.path.join(folder_path, 'nbib_data.xlsx')
df.to_excel(excel_output_path, index=False)

# Salva os dados em um arquivo CSV compactado (.csv.gz) na mesma pasta 'scrap1'
csv_gz_output_path = os.path.join(folder_path, 'nbib_data.csv.gz')
df.to_csv(csv_gz_output_path, index=False, compression='gzip')
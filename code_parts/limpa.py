import pandas as pd

# Caminhos para os arquivos
caminho_arquivo = '/Users/enricochiosini/Documents/eric scrapping/temp/nbib_data.csv.gz'

# Importa o arquivo nbib_data.csv.gz
df = pd.read_csv(caminho_arquivo, compression='gzip')

palavras_or_2 = ['teach', 'educat', 'learn']
palavras_or_1 = [
    'physic',   # physics
    'chem',     # chemistry
    'biolog',   # biology
    'astronom', # astronomy
    'geolog',   # geology
    'scien',    # science
    'ecolog',   # ecology
]

def verifica_texto(row):
    # Concatena TI e AB e converte para minúsculas
    texto = (str(row['TI']) + " " + str(row['AB'])).lower()
    tokens = texto.split()
    # Percorre os tokens procurando por pares consecutivos em que um
    # inicia com uma palavra de palavras_or_1 e o outro com uma de palavras_or_2,
    # em qualquer ordem.
    for i in range(len(tokens) - 1):
        t1, t2 = tokens[i], tokens[i+1]
        if (any(t1.startswith(p) for p in palavras_or_1) and 
            any(t2.startswith(p) for p in palavras_or_2)):
            return True
        if (any(t1.startswith(p) for p in palavras_or_2) and 
            any(t2.startswith(p) for p in palavras_or_1)):
            return True
    return False

df_filtrado = df[df.apply(verifica_texto, axis=1)]

df_filtrado.to_csv('temp/eric_filtered.csv.gz', index=False, compression='gzip')
df_filtrado.to_excel('temp/eric_filtered.xlsx', index=False)

print(f"Total de artigos filtrados: {len(df_filtrado)}")

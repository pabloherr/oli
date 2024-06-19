import pandas as pd
import json

# Leer el archivo de Excel
df = pd.read_excel('output.xlsx')

# Filtrar las filas que contienen 'Not found/case 1'
df_filtered = df[df[df.columns[1]].str.contains('Not found/case 1')]
# Crear una lista vacía para almacenar los valores de la primera columna
first_column_values = []

# Iterar sobre las filas del DataFrame filtrado
for index, row in df_filtered.iterrows():
    # Agregar el valor de la primera columna a la lista
    first_column_values.append(row[df.columns[0]])


# Leer el diccionario desde el archivo
with open('dic.txt', 'r') as f:
    dic_str = f.read()
dic = json.loads(dic_str)

# Crear un nuevo diccionario para almacenar los elementos coincidentes
matching_elements = {}

# Iterar sobre los elementos en first_column_values
for element in first_column_values:
    # Si el elemento es una clave en el diccionario, agregarlo a matching_elements
    if element in dic:
        matching_elements[element] = dic[element]
print(matching_elements)
#guardamos el json, en forma de diccionario en un archivo txt con los elementos del json ordenamdos en filas
with open('matching_elements.txt', 'w') as f:
    f.write(json.dumps(matching_elements, indent=4))
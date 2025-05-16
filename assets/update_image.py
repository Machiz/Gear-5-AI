import json

file_path = r"c:\Users\marce\Gear-5-AI\assets\JSON\Battle_log\log2.JSON"

# Cargar el archivo JSON
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Crear un nuevo diccionario con claves renombradas
updated_data = {}
for key, value in data.items():
    if key.startswith("log3-"):
        new_key = key.replace("log3-", "log2-")
        updated_data[new_key] = value
    else:
        updated_data[key] = value  # conservar otras claves si las hay

# Guardar el nuevo archivo JSON
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(updated_data, file, indent=2, ensure_ascii=False)

print("Claves actualizadas de 'log7' a 'log6' correctamente.")

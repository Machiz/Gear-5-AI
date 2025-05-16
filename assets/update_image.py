import json

file_path = r"c:\Users\marce\Gear-5-AI\assets\JSON\Battle_log\log1.JSON"

# Cargar el archivo JSON
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Eliminar attacker_name y defender_name de cada entrada
for key, value in data.items():
    value.pop("attacker_name", None)
    value.pop("defender_name", None)

# Guardar el archivo actualizado
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

print("Campos 'attacker_name' y 'defender_name' eliminados correctamente.")

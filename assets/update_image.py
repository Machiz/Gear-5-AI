import json

file_path = r"c:\Users\marce\Gear-5-AI\assets\JSON\OP09.json"

# Load the JSON file
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Update the images attribute
for key, value in data.items():
    if "images" in value:
        value["images"] = value["images"].replace(".png", ".jpg")

# Save the updated JSON file
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

print("Images updated successfully!")
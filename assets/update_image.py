import json

file_path = r"c:\Users\marce\Gear-5-AI\assets\JSON\Battle_log\log10.JSON"

# Load the JSON file
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Create a new dictionary to store the data in the desired format
updated_data = {}

# Add ID to each action with the format log1-001, log1-002, etc.
action_id = 1  # Starting ID
for item in data:
    if isinstance(item, dict):  # Assuming each item in the list is a dictionary representing an action
        item_id = f"log10-{action_id:03d}"
        updated_data[item_id] = item  # Set the ID as the key in the dictionary
        action_id += 1  # Increment the ID for the next action

# Save the updated JSON file in the desired format
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(updated_data, file, indent=2, ensure_ascii=False)

print("Actions updated with IDs successfully!")

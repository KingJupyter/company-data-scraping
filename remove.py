import json

# Function to remove duplicates from a list of dictionaries based on a specific key
def remove_duplicates_by_key(items, key):
    seen = set()
    result = []
    for item in items:
        value = item[key]
        if value not in seen:
            seen.add(value)
            result.append(item)
    return result

# Step 1: Load the JSON data from the file
with open('system.json', 'r') as file:
    data = json.load(file)

# Step 2: Remove duplicates (assuming each item is a dictionary and 'id' is the key to check for duplicates)
unique_data = remove_duplicates_by_key(data, 'name')

print(len(unique_data))
# Step 3: Save the processed data back to another JSON file
with open('remove_system.json', 'w') as file:
    json.dump(unique_data, file, indent=4)

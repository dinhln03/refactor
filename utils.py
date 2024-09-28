import json

# Load the JSON file
with open('image_paths_new.json', 'r') as file:
    data = json.load(file)
print(data)
# Modify the image_path values
for key in data:
    if 'image_path' in data[key]:
        data[key]['image_path'] = data[key]['image_path'].replace('/home/dinhln/Desktop/MLOPS/AIC/keyFrameLarge/', 'keyFrameLarge/')

# Save the modified JSON back to the file
with open('image_paths_new1.json', 'w') as file:
    json.dump(data, file, indent=4)


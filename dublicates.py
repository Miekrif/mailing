import json

with open("users.json" , "r") as read_file:
    users = json.load(read_file)
    users = users['users']

dublicates = users.keys()

list_of_files = [*{*dublicates}]

new_dict = {}

new_dict["users"] = dict.fromkeys(list_of_files, '')

print(new_dict)

with open("new_file.json", "w") as new_file:
    json.dump(new_dict, new_file)



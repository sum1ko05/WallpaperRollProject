import json


def load_config():
    with open("config.json", 'r') as json_file:
        data = json.load(json_file)
    return data


def save_config(data):
    with open("config.json", 'w') as json_file:
        json.dump(data, json_file)
    return 

#with open("config.json", 'r') as json_file:
#    data = json.load(json_file)

#print(data)
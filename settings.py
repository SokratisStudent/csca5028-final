import os
import json

settings_filename = os.path.dirname(os.path.abspath(__file__)) + "/settings.json"

with open(settings_filename, "r") as jsonfile:
    settings_data = json.load(jsonfile)

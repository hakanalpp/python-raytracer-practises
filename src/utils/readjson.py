# CENG 488 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# April 2022

import json

# Opening JSON file
def readJson(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

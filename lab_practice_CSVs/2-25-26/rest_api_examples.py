#############################################################################################
# APIs and JSON
import json # package to work with JSON data https://docs.python.org/3/library/json.html
import requests # for making HTTP requests, install with: conda install requests
import time
import pandas as pd


# API procedure:
# 1. Find an API you're interested in.
#    - Here's a fun list to get you started: https://github.com/public-api-lists/public-api-lists
# 2. Read the documentation, licenses, permissions information, etc.
#    - Some APIs may be free/open
#    - Some may require a (free) registration
#    - Some may require a paid account
#    - Respect the guidelines!
# 3. For most REST APIs:
#    - use GET requests
#    - the API reads those requests in a way unique to that API
#    - you get back data, usually in JSON format
# 4. Work with the data in Python
#    - JSON can get very "nested"
#    - json package converts to lists, dictionaries, etc.
#    - use your knowledge of these Python structures to navigate 
#      the JSON and find the values you want
#    - use type(), dict.keys(), len() to help figure out the structure 
#      as you go
#    - json.dumps(obj, indent = 4) can make raw JSON easier to read

# https://www.fbi.gov/wanted/api
fbi_wanted_response = requests.get("https://api.fbi.gov/wanted/v1/list")
fbi_wanted_data = json.loads(fbi_wanted_response.content)
# fbi_wanted_data = fbi_wanted_response.json() # also works
type(fbi_wanted_data)
fbi_wanted_data.keys()
fbi_wanted_data["total"]
len(fbi_wanted_data["items"])
fbi_wanted_data["items"][0]
print(fbi_wanted_data["items"][0])
print(json.dumps(fbi_wanted_data["items"][0], indent = 2))


fbi_results = {"sex" : [],
                "height_max" : [],
                "reward_max" : []
}

fbi_wanted_data["items"][19]["sex"]

for page in range(1, 58):
    time.sleep(.3)
    if (page-1) % 10 == 0:
        print(f"starting {page=}")

    fbi_wanted_response = requests.get("https://api.fbi.gov/wanted/v1/list",
                                    params = {"page" : page})
    fbi_wanted_data = json.loads(fbi_wanted_response.content)

    for record in range(20):
        fbi_results["sex"].append(fbi_wanted_data["items"][record]["sex"])
        fbi_results["height_max"].append(fbi_wanted_data["items"][record]["height_max"])
        fbi_results["reward_max"].append(fbi_wanted_data["items"][record]["reward_max"])

fbi_results
fbi_df = pd.DataFrame(fbi_results)
fbi_df
fbi_df.describe()

# https://pokeapi.co/
pikachu_resp = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")
pikachu_data = json.loads(pikachu_resp.content)


# https://beta.umd.io/
umd_resp = requests.get("https://api.umd.io/v1/courses?dept_id=INST&semester=202601")
umd_data = json.loads(umd_resp.content)


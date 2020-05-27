import json
from pkg_resources import resource_filename

def ivp_a1():
    filepath = resource_filename(__name__, 'ivp_a1.json')

    # Read the data from file
    # We now have a Python dictionary
    with open(filepath) as f:
        data = json.load(f)
        properties = data['properties']
        ivp_a1 = {}
        # Read each property
        for (k1, v1) in properties.items():
            # Find the property that has enum
            for (k2, v2) in v1.items():
                if k2 == "enum":
                    # Find if the enums is a dictionary
                    # If the enums are just numbers then it will not be added
                    # to the dictionary
                    isDict = False
                    for i in v2:
                        if i.isnumeric() == False:
                            isDict = True
                            break
                    # add enums to dictionary
                    if isDict:
                        ivp_a1[k1] = {}
                        for value in v2:
                            key = value[0]
                            # If the first char is not digit then
                            # don't add it in dictionary
                            if key.isnumeric():
                                ivp_a1[k1][key] = value[2:]



    return ivp_a1

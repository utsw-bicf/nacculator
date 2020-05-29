import json

def ivp_a1():
    # get row headers of for ivp_a1 from redcap
    headersIvp_a1 = ["ptid", "redcap_event_name", "initials1", "reason", "refersc",	"learned", "prestat", "prespart", "source", "birthmo", "birthyr", "sex", "hispanic", "hispor", "hisporx", "race", "racex", "racesec", "racesecx", "raceter", "raceterx", "primlang", "primlanx", "educ", "educ_type", "maristat", "livsitua", "independ", "residenc", "zip", "handed", "ivp_a1_complete"]

    # Read the data from json schema file
    # We now have a Python dictionary
    with open('ivp_a1.json') as f:
        data = json.load(f)
        properties = data['properties']
        ivp_a1 = {}
        for header in properties.keys():
            ivp_a1[header] = {}
        # Read each property in properties
        for (k1, v1) in properties.items():
            # Find the property that has enum
            for (k2, v2) in v1.items():
                if k2 == "enum":
                    # find out if k1 is the form ivp_a1 header
                    if k1 in headersIvp_a1:
                        # Find if the enums is a dictionary
                        # If the enums are just numbers then it will 
                        # be an empty dictionary
                        hasDict = False
                        for i in v2:
                            if str(i).isnumeric() == False:
                                hasDict = True
                                break
                        # add enums to dictionary
                        if hasDict:
                            for value in v2:
                                key = value[0]
                                # If the first char is not digit then 
                                # don't add it in dictionary
                                if key.isnumeric():
                                    ivp_a1[k1][key] = value[2:]
    ivp_a1["status"] = {"0":"deleted", "1":"in progress", "2":"released"}
    ivp_a1.pop("schema_version")           
    return ivp_a1

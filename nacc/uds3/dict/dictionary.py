import json
from pkg_resources import resource_filename

# get row headers of for ivp_a1 from redcap
ivp_a1 = ["ptid", "redcap_event_name", "initials1", "reason", "refersc", "learned", "prestat", "prespart", "source", "birthmo", "birthyr", "sex", "hispanic", "hispor", "hisporx", "race", "racex", "racesec", "racesecx", "raceter", "raceterx", "primlang", "primlanx", "educ", "educ_type", "maristat", "livsitua", "independ", "residenc", "zip", "handed", "ivp_a1_complete"]
fvp_a1 = ["ptid", "redcap_event_name", "initials17", "fu_birthmo", "fu_birthyr", "fu_maristat",	"fu_sex", "fu_livsitua", "fu_independ",	"fu_residenc", "fu_zip", "fvp_a1_complete"]
master_id = ["ptid", "redcap_event_name", "utsw_mrn", "pic", "first", "mi",	"last",	"gender", "dob", "ssnmed", "edu", "retard",	"occ", "lang", "ethn", "racial", "racial_other", "tribe", "tribe_other", "percent",	"p_addr1", "p_addr2", "p_city",	"p_state", "p_zip",	"p_phone", "p_phoneext", "p_email",	"c_name", "c_relat", "c_addr1",	"c_addr2", "c_city", "c_state", "c_zip", "c_phone",	"c_phoneext", "c_email", "alt_name", "alt_relation", "alt_addr", "alt_city", "alt_state", "alt_zip", "alt_phone", "alt_altphone", "alt_email", "lar", "larrelation", "laraddr",	"larcity", "larstate", "larzip", "larphone", "laraltphone",	"laremail",	"master_id_complete"]
header = ["ptid", "redcap_event_name", "formver", "adcid", "visitmo", "visitday", "visityr", "visitnum", "initials", "header_complete"]

formHeaders = {}
formHeaders["ivp_a1"] = ivp_a1
formHeaders["fvp_a1"] = fvp_a1
formHeaders["master_id"] = master_id
formHeaders["header"] = header

def getDict(dictName):
    
    dictionary = {}
    
    if dictName in formHeaders:
        # Read the data from json schema file
        # We now have a Python dictionary
        if dictName == "header":
            schemaFile = "mixins.json" 
        else :
            schemaFile = dictName + ".json"
        
        headers = formHeaders[dictName]
        for header in headers:
            dictionary[header] = {}
        filepath = resource_filename(__name__, schemaFile)
        with open(filepath) as f:
            data = json.load(f)
            if dictName == "header":
                properties = data["header"]
            else:
                properties = data['properties']
            
            
            # Read each property in properties
            for (k1, v1) in properties.items():
                # Find the property that has enum
                for (k2, v2) in v1.items():
                    if k2 == "enum":
                        addToDict(k1, v2, headers, dictionary)
                    elif k2 == "type" and v2 =="object":
                        for (k2, v2) in v1.items():
                            if k2 == "properties":
                                for (k3, v3) in v2.items():
                                    for (k4, v4) in v3.items():
                                        if k4 == "enum":
    
                                            addToDict(k3, v4, headers, dictionary)
                                    
        dictionary[dictName + "_complete"] = {"0":"incomplete", "1":"unverified", "2":"complete"}
        if "schema_version" in dictionary:
            dictionary.pop("schema_version")
    else:
        print("No such dictionary!")
    

    return dictionary

def getTypes(dictName):
    types = {}
    if dictName in formHeaders:
        if dictName == "header":
            schemaFile = "mixins.json" 
        else :
            schemaFile = dictName + ".json"
        
        
        filepath = resource_filename(__name__, schemaFile)
        with open(filepath) as f:
            data = json.load(f)
            if dictName == "header":
                properties = data["header"]
            else:
                properties = data['properties']
            for (k1, v1) in properties.items():
                # Find the key "type:
                for (k2, v2) in v1.items():
                    if k2 == "type":
                        types[k1] = {k2: v2}
                        if v2 == "object":
                            for (k2, v2) in v1.items():
                                if k2 == "properties":
                                   types[k1][k2]  = {}
                                   for (k3, v3) in v2.items():
                                      
                                      for (k4, v4) in v3.items():
                                          if k4 == "type":
                                             types[k1][k2][k3] = {k4: v4} 
                            
        types[dictName + "_complete"] = {"type": "string"}
    else:
        print("No such schema!")
    
    return types

def addToDict(k1, v2, headers, dictionary):
    
    if k1 in headers:
        # Find if the enums is a dictionary
        # If the enums are just numbers then it will
        # be an empty dictionary
        hasDict = False
        for i in v2:

            #print(str(i).split())
            if str(i).split()[0].isnumeric() and len(str(i).split()) > 1:
                hasDict = True
                break
        # add enums to dictionary
 
        if hasDict:
            for value in v2:
                key = str(value).split()[0]
                
                # If the key is not digit then
                # don't add it in dictionary
                if key.isnumeric():
                    dictionary[k1][key] = value[len(key) + 1:]


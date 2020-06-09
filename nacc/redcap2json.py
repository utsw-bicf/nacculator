#!/usr/bin/env python

# Sample execution command (requires python >= 3.7.0):
# python3 redcap2json.py --fileIn REDCap_export.csv

import os
import sys
import json
import argparse
import pandas as pd
from nacc.uds3.dict.dictionary import getDict
from nacc.uds3.dict.dictionary import getTypes

def parse_args():
    parser = argparse.ArgumentParser(
        description = "process redcap form output to json."
    )

    parser.add_argument(
        "--fileIn", action = "store", dest = "fileIn", required = True,
        help = "Path of the CSV file to convert to JSON.")

    options = parser.parse_args()

    return options

def convert_to_json(options, schema_name):
    """
    Parses the content matching the given schema_name out of the .CSV and converts it to JSON format.
    """

    # Read in CSV
    all_csv = pd.read_csv(
        filepath_or_buffer = options.fileIn,
        dtype = str
    )

    # Replace each row/column value (cell) to the corresponding schema value for that header.
    schema_dict = getDict(schema_name)
    print(json.dumps(schema_dict, indent = 2))
    for headerIndex, header in enumerate(all_csv):
        for valueIndex, value in enumerate(all_csv[header]):
            # Ensure header exists in dictionary.
            if schema_dict.get(header) is not None:
                # Map the '<schema_name>_complete' header values without the raw-value appended to the mapped value
                if str(value) != "nan" and "_complete" in header:
                    all_csv.iat[valueIndex, headerIndex] = str(schema_dict[header][value])
                # Ensure the current value for the current header is valid.
                elif str(value) != "nan" and schema_dict[header].get(value) is not None:
                    all_csv.iat[valueIndex, headerIndex] = str(value + " " + schema_dict[header][value])

    # Create a list of subset headers using the form's schema headers (dictionary.py).
    form_subset_headers = list(schema_dict.keys())

    # Create the subset dataframe for the specific form.
    form_csv = all_csv[form_subset_headers]

    # Drop all fully empty records (rows).
    # Runs .dropna on all columns except the '<schema_name>_complete' header b/c '<schema_name>_complete' makes empty records not empty.
    columns_to_check_to_drop = form_subset_headers
    columns_to_check_to_drop.remove(schema_name + "_complete")
    form_csv = form_csv.dropna(how = "all", subset = columns_to_check_to_drop)

    # Fill any remaining empty cells with empty strings.
    # These would be cells in which its entire row was not empty.
    # Makes it simple to remove specific key/value pairs later on.
    form_csv = form_csv.fillna(value = "")

    # Rename the '<schema_name>_complete' header
    form_csv = form_csv.rename(columns = {schema_name + "_complete": "form_status"})

    # Convert form to JSON
    form_json = form_csv.to_json(
        orient = "records",
        indent = 2
    )

    # 1. Remove key/value pairs that have empty strings as values.
    #    Using the included .dropna in the pandas library doesn't allow for records to vary in size.
    #    Dropped key/value pairs will reappear with null values.
    # 2. Map each value to the correct schema type (string or integer)
    # 3. Manage key/value pairs that need to be apart of a nested group (master_id)
    form_dict = form_csv.to_dict(orient = "records")
    to_delete = []
    groups_to_add = {}
    schema_types = getTypes(schema_name)
    for index, record in enumerate(form_dict):
        for key, value in form_dict[index].items():
            # Drop empty key/value pairs that have empty values
            if form_dict[index][key] == "":
                to_delete.append((index, key))
            # If key/value isn't to be removed, cast the appropriate type to the value
            elif key in schema_types:
                if schema_types.get(key).get("type") == "string":
                    form_dict[index][key] = str(form_dict[index][key])
                elif schema_types.get(key).get("type") == "integer":
                    form_dict[index][key] = int(form_dict[index][key])

            # If key should be nested, nest it
            if schema_name == "master_id":
                # TODO: Parse these from schema in seperate dictionary function. Determine return type (lists of lists??)
                nested_groups = {
                    "p_info": ["p_addr1", "p_addr2", "p_city", "p_state", "p_zip", "p_phone", "p_phoneext", "p_email"],
                    "c_cont1": ["c_name", "c_relat", "c_addr1", "c_addr2", "c_city", "c_state", "c_zip", "c_phone", "c_altphone", "c_altphoneext2", "c_email"],
                    "alt_cont2": ["alt_name", "alt_relation", "alt_addr", "alt_addr2", "alt_city", "alt_state", "alt_zip", "alt_hmphone", "alt_hmphoneext", "alt_phone", "alt_altphone", "alt_email"],
                    "lar_auth_repr": ["lar", "larrelation", "laraddr", "laraddr2", "larcity", "larstate", "larzip", "lar_hmphone", "lar_hmext", "larphone", "laraltphone", "laremail"]
                }

                # Check if key matches any group
                for group_name, group_keys in nested_groups.items():
                    if key in group_keys:
                        # Check if key/value can be added to groups_to_add
                        if group_name not in groups_to_add and form_dict[index][key] != "":
                            groups_to_add[group_name] = {key: form_dict[index][key]}
                            to_delete.append((index, key))
                        elif form_dict[index][key] != "":
                            groups_to_add[group_name][key] = form_dict[index][key]
                            to_delete.append((index, key))

        # For every index, insert the groups_to_add object
        for group_name in groups_to_add.keys():
            form_dict[index][group_name] = groups_to_add[group_name]

        # Reset groups_to_add for next index (record)
        groups_to_add = {}

    # Remove key/value pairs from form_dict
    for pair in to_delete:
        del form_dict[pair[0]][pair[1]]

    # Create and write to output JSON file
    form_json = json.dumps(form_dict, indent = 2)
    output_file_path = os.path.join(os.getcwd(), "output_" + schema_name + ".json")
    form_json_file = open(output_file_path, "w")
    form_json_file.write(form_json)
    form_json_file.close()

def main():
    """
    Converts a REDCap exported CSV (raw data) file to a JSON file.
    """
    options = parse_args()

    # List of every schema name possible in the .CSV file
    schema_names = ["ivp_a1", "fvp_a1", "master_id", "header"]

    convert_to_json(options, "master_id")

    # Output each schema to its own JSON file.
    # for schema in schema_names:
    #     try:
    #         print("[STATUS] Parsing: " + schema)
    #         convert_to_json(options, schema)
    #         print("[STATUS] Completed: " + schema, "\n")
    #     except Exception as e:
    #         print("[SKIP] Could not parse: " + schema, "\n", e, "\n")

    print("Done.")

if __name__ == "__main__":
    main()

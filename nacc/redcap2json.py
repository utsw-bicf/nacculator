#!/usr/bin/env python

# Sample execution command (requires python >= 3.7.0):
# python3 redcap2json.py --fileIn REDCap_export.csv

import os
import sys
import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(
        description = 'process redcap form output to json.'
    )

    parser.add_argument(
        '--fileIn', action = 'store', dest = 'fileIn', required = True,
        help = 'Path of the CSV file to convert to JSON.')

    options = parser.parse_args()

    return options

def convert_to_json(options):
    # Read in CSV
    all_csv = pd.read_csv(
        filepath_or_buffer = options.fileIn,
        dtype = str,
        nrows = 10  # TODO: Remove nrows param when done testing
    )

    # Map each column's values to the corresponding schema values for that header
    # TODO: Replace this dictionary with actual keys and values
    schema_dict = {
        'formver': {
            '3': 'This is option 3.',
            'nan': 'Hello World.'
        },
        'reason': {
            '1': 'This is a 1.',
            '3': 'This is a 3.',
            'nan': 'This is a NaN replacement test.'
        }
    }
    for headerIndex, header in enumerate(all_csv):
        for valueIndex, value in enumerate(all_csv[header]):
            # Ensure header exists in dictionary
            if schema_dict.get(header) is not None:
                # Ensure the current value for the current header is valid
                if str(value) == 'nan' or schema_dict[header].get(value) is None:
                    all_csv.iat[valueIndex, headerIndex] = schema_dict[header]['nan']
                else:
                    all_csv.iat[valueIndex, headerIndex] = schema_dict[header][value]

    # Create subset dataframes for each form using their respective headers
    form_a1_headers = [
        'initials1',
        'reason',
        'refersc',
        'learned',
        'prestat',
        'prespart',
        'source',
        'birthmo',
        'birthyr',
        'sex',
        'hispanic',
        'hispor',
        'hisporx',
        'race',
        'racex',
        'racesec',
        'racesecx',
        'raceter',
        'raceterx',
        'primlang',
        'primlanx',
        'educ',
        'educ_type',
        'maristat',
        'livsitua',
        'independ',
        'residenc',
        'zip',
        'handed',
        'ivp_a1_complete'
    ]
    form_a1_csv = all_csv[form_a1_headers]

    # Convert each form to JSON
    form_a1_json = form_a1_csv.to_json(
        orient = 'records',
        indent = 2
    )

    # Convert entire CSV to JSON
    all_json = all_csv.to_json(
        orient = 'records',
        indent = 2
    )

    # Create and write to output JSON file
    json_file_path = os.path.join(os.getcwd(), 'output.json')
    json_file = open(json_file_path, 'w')
    json_file.write(form_a1_json)
    json_file.close()

def main():
    """
    Converts a REDCap exported CSV (raw data) file to a JSON file.
    """
    options = parse_args()

    convert_to_json(options)

    print('Done.')

if __name__ == '__main__':
    main()

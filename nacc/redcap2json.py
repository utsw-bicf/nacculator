#!/usr/bin/env python

# Sample execution command (requires python >= 3.7.0):
# python3 redcap2json.py --fileIn REDCap_export.csv

import os
import sys
import argparse
import pandas as pd
from nacc.uds3.dict.dictionary import ivp_a1

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

    # Replace each row/column value (cell) to the corresponding schema value for that header
    ivp_a1_schema_dict = ivp_a1()
    for headerIndex, header in enumerate(all_csv):
        for valueIndex, value in enumerate(all_csv[header]):
            # Ensure header exists in dictionary
            if ivp_a1_schema_dict.get(header) is not None:
                # Ensure the current value for the current header is valid
                if str(value) != 'nan' and ivp_a1_schema_dict[header].get(value) is not None:
                    all_csv.iat[valueIndex, headerIndex] = str(value + ' ' + ivp_a1_schema_dict[header][value])

    # Create a list of subset headers using the form schema headers (dictionary)
    ivp_a1_headers = list(ivp_a1_schema_dict.keys())

    # Ensure all headers from dictionary exist in the CSV file
    # If not, remove them from the headers subset list
    for header in ivp_a1_headers:
        if all_csv.get(header) is None:
            ivp_a1_headers.remove(header)

    # Create the subset dataframe for the specific form
    ivp_a1_csv = all_csv[ivp_a1_headers]

    # Drop all fully empty records (rows)
    ivp_a1_csv = ivp_a1_csv.dropna(how = 'all')

    # Fill any remaining empty cells with empty strings
    # These would be cells in which its entire row was not empty
    ivp_a1_csv = ivp_a1_csv.fillna(value = "")

    # Convert form to JSON
    ivp_a1_json = ivp_a1_csv.to_json(
        orient = 'records',
        indent = 2
    )

    # Create and write to output JSON file
    output_file_path = os.path.join(os.getcwd(), 'output_ivp_a1.json')
    ivp_a1_json_file = open(output_file_path, 'w')
    ivp_a1_json_file.write(ivp_a1_json)
    ivp_a1_json_file.close()

def main():
    """
    Converts a REDCap exported CSV (raw data) file to a JSON file.
    """
    options = parse_args()

    convert_to_json(options)

    print('Done.')

if __name__ == '__main__':
    main()

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

    parser.add_argument(
        '--fileOut', action = 'store', dest = 'fileOut', required = True,
        help = 'Path to output JSON file.')

    options = parser.parse_args()

    return options

def convert_to_json(options):
    csv = pd.read_csv(
        filepath_or_buffer = options.fileIn,
        dtype = str,
        nrows = 2,
    )
    json_data = csv.to_json(
        orient = 'records',
        indent = 2
    )

    json_file_path = os.path.join(os.getcwd(), 'output.json')
    json_file = open(json_file_path, 'w')
    json_file.write(json_data)
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

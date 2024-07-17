#!/usr/bin/env python3

import argparse
import csv
import re
import sys
import pandas as pd

# VCF regex matches
RE_VCF_BEGIN = r'^BEGIN:VCARD$'
RE_VCF_END = r'^END:VCARD$'
RE_VCF_FIELD = r'^(.*):(.*)'

def parse_vcf(vcf_file):
    data = []
    line_data = {}
    for line in vcf_file:
        line = line.strip()
        # Handle lines that are beginnings and ends of cards
        if re.match(RE_VCF_BEGIN, line):
            # if there is a begin line, start a new empty line_data dict
            line_data = {}
        elif re.match(RE_VCF_END, line):
            # if there is a end line and there are information in the data dict
            if line_data != {}:
                data = data + [line_data]
        # Extract vcf field
        else:
            vcf_field = re.match(RE_VCF_FIELD, line)
            if vcf_field:
                field = vcf_field.group(1).strip()
                value = vcf_field.group(2).strip()
                # if the field is a photho, just set a flagavoid capture photo field because it is a multiline base64 string
                if re.search("photo", field.lower()): value = "Yes"
                line_data[field] = value
    return data

def write_csv(data, csv_file_name):
    df = pd.DataFrame.from_dict(data)
    df.to_csv(csv_file_name, index=False, header=True)

def main(input_file, output_file):
    with open(input_file, 'r') as vcf_file:
        data = parse_vcf(vcf_file)
    write_csv(data, output_file)
    return 0

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Convert VCF file to CSV.')
    parser.add_argument('input_file', type=str, help='vcf file to process')
    parser.add_argument('output_file', type=str, help='csv file to output')
    args = parser.parse_args()

    sys.exit(main(args.input_file, args.output_file))

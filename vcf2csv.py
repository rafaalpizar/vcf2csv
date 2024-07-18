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

def phone_number_clenaup(phone_number):
    bad_chars = re.compile(r'[- ]')
    ok_country_code = re.compile(r'\+?506')
    clean_phone_number = re.sub(bad_chars, '', phone_number)
    if (len(clean_phone_number) == 8) or (re.match(ok_country_code, clean_phone_number)):
        return clean_phone_number
    else:
        return phone_number

def decode_quoted_hex(hex_data):
    clean_hex_data = hex_data.replace(';', '=20').split('=')
    text_decoded = ''
    char_decoded = ''
    to_be_decoded = ''
    for item in clean_hex_data:
        try:
            if to_be_decoded:
                char_decoded = bytes.fromhex(to_be_decoded).decode()
                to_be_decoded = ''
            else:
                char_decoded = ''
                char_decoded += bytes.fromhex(item).decode()
                text_decoded += char_decoded
        except:
            to_be_decoded += item
    return text_decoded

def add_vcf_field(line_data, vcf_field, vcf_value, index=0):
    # add field to dictionary with recursive alg
    if vcf_field in line_data:
        index += 1
        # get field base name to append later append new index
        vcf_field = vcf_field.split('-')[0]
        # recursive call to with new index append
        add_vcf_field(line_data,f'{vcf_field}-{index}', vcf_value, index)
    else:
        line_data[vcf_field] = vcf_value

def extract_vcf_field(line_data, vcf_field, vcf_value):
    # clenaup field values
    # if the field is a photho, just set a flagavoid capture photo field because it is a multiline base64 string
    if re.search("photo", vcf_field.lower()): vcf_value = "Yes"
    if re.search("tel", vcf_field.lower()): vcf_value =  phone_number_clenaup(vcf_value)
    if re.search('encoding=quoted-printable', vcf_field.lower()): vcf_value = decode_quoted_hex(vcf_value)
    add_vcf_field(line_data, vcf_field, vcf_value)

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
            # if there is a end line and there are information in the data dict add it to the array
            if line_data != {}:
                data = data + [line_data]
        # Extract vcf field
        else:
            vcf_field = re.match(RE_VCF_FIELD, line)
            if vcf_field:
                field = vcf_field.group(1).strip()
                value = vcf_field.group(2).strip()
                extract_vcf_field(line_data, field, value)
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

VCF2CSV
=======

VCF2CSV is a full Vcard to CSV converter.

This tool extract all the fields from the vcf file and
it creates an HTML file with photos if available.


Usage:

```
usage: vcf2csv.py [-h] input_file output_file

Convert VCF file to CSV.

positional arguments:
  input_file         vcf file to process
  output_file        csv file to output

optional arguments:
  -h, --help         show this help message and exit
  --ignore_no_email  ignore entries with no email
```

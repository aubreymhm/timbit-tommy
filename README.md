# eform-conversion

This takes a "raw" CSV file as downloaded from the Government of Manitoba's EForm retrieval tool, runs some conversions on it using `pandas`, and spits out a csv in the format we need

We're using this to pull immunization record form submissions from the public and convert them into the format/schema for our big spreadsheet (you read that right)

Not a lot that can go wrong aside from *maybe* the encoding; the EForm retrieval tool encodes using UTF-16-BE... mostly. It doesn't handle accents well and sometimes someone will toss in a character it doesn't like. The script ignores errors and moves on.

The script takes one command-line argument, which is the CSV of the file it should convert. No flags needed.

eg. `python converter.py 12934130423.csv`

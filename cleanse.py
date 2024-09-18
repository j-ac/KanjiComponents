#! /usr/bin/env python3
# Removes junk from the start of lines in the Tatoeba dataset sourced from: https://tatoeba.org/en/downloads
from sys import argv

if len(argv) < 2 or len(argv) > 3:
    print("Usage: cleanse.py [input file] [output file]")
    quit()

with open(argv[1], 'r', encoding='utf-8') as infile, open(argv[2], 'w', encoding='utf-8') as outfile:
    for line in infile:
        new_line = line.split("	")[-1]
        outfile.write(new_line)
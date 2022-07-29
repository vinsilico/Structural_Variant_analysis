#!/usr/bin/env python

# Script gets a imput samfile with "N" in the CIGAR string, replace "N" with "D"

import sys

input_sam = sys.argv[1]

output_sam = open("output_splice_cigar.sam", "w")
output_txt = open("output_splice_cigar.txt", "w")

for line in open(input_sam):
        if line[0] == "@":
                output_sam.write(line)
                pass
        else:
                split_line = line.split()
                output_txt.write(split_line[5]+"\n")
                cigar2 = split_line[5].replace("N","D")
                split_line[5] = cigar2
                output_txt.write(cigar2+"\n"+"\n")
                output_sam.write("\t".join(split_line))
                output_sam.write("\n")

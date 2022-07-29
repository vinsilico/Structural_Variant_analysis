#!/usr/bin/env python

# when splice option is used with minimap2, minimap2 uses N in the Cigar string, which wont work with SV caller.
# so, N in the CIGAR string need to be changed to D
# This script gets a samfile with "N" in the CIGAR string, and writes a new sam file with "D" instead of "N"
# This script also writes the original and modified CIGAR string in a text file, for reference.

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

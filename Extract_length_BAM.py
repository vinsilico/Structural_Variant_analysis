#!/usr/bin/env python

# Extract mapped read length from bam file and remove duplicates, sort , calculate length (3rd column) and convert to bed file.

import pysam
import sys
import os.path
import pandas as pd

input_bam = sys.argv[1]
ip_bam_file = os.path.splidataset(input_bam)[0]

print(ip_bam_file)

op_txt_file = ip_bam_file + "_mapped_region.txt"
op_txt_file2 = ip_bam_file + "_mapped_region_uniq.txt"

output_txt = open(op_txt_file, "w")

output_txt2 = open(op_txt_file2, "w")

bam = pysam.AlignmentFile(input_bam)
for read in bam.fetch():
    output_txt.write("{}\t{}\t{}\n".format(read.reference_name, read.reference_start+1, read.reference_end))

uniq_lines = set(open(op_txt_file).readlines())
out = open(op_txt_file2, 'w').writelines(uniq_lines)

dataset2 = pd.read_csv(op_txt_file, sep = '\t', header=None)
dataset2.columns = ["ref_ID", "start_coord", "end_coord"]
dataset2 = dataset2.sort_values(by=['start_coord','end_coord'],ascending=True)
dataset2['length'] = (dataset2['end_coord'] - dataset2['start_coord'])+1
dataset3 = dataset2.sort_values(by=['length'],ascending=True)
dataset4  = dataset3[(dataset3['start_coord'] != 1) & (dataset3['end_coord'] != 644)]  
print(dataset4) 

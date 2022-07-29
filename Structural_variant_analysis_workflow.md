# Structural_Variant_analysis

#Identifiction of structural variants from (targeted) amplicon sequenced samples (ONT MinION dataset).

#Dataset: Oxford Nanopore dataset (DNA)

#AWS Instance: Analysis was done in AWS EC2 instance c5a.8xlarge (32vCPU and 64 GB RAM)

#Basecalling : Guppy basecaller (fast mode)
guppy_basecaller -i <PATH/TO/INPUT/> -s <PATH/TO/OUTPUT/> --cpu_threads_per_caller INT --num_callers INT -c dna_r9.4.1_450bps_fast.cfg

#Concatenate all the fastq sequences
cat  *.fastq > combined.fastq

#Check the quality of reads using FastQC /PyoQC
fastqc -f fastq -t 26 -o <output_folder> combined.fastq
pycoQC -f sequencing_summary.txt -o pycoQC_output.html

#Trim adapter and demultiplexing of reads using porechop
porechop -i combined.fastq -o combined_porechop.fastq –verbosity 0 –threads 30
porechop -i combined.fastq -b output_folder/ –verbosity 0 –threads 30

#combine all the reads from demultiplexed barcode bins, number of bins, depends on the number of barcodes used.

#Map the reads with minimap2, with splice option and preset parameters for ONT dataset (recommended)
minimap2 -k -splice -ax map-ont reference.fasta combined.fastq > combined_splice.sam


#Run the cigar_edit.py script to change the “N” in the CIGAR string to “D”. 
#This scripts outputs two files (1) sam file with corrected cigar string and (2) text file with original and modified CIGAR string

python cigar_edit_pb.py combined_splice.sam

#Convert the sam file to sorted, indexed bam file using samtools

samtools view -Sb combined_splice_cigar.sam > combined_splice_cigar.bam
samtools sort combined_splice_cigar.bam -o combined_splice_cigar.sorted.bam
samtools index combined_splice_cigar.sorted.bam

#Run cuteSV variant caller with absolute minimal values with parameters.

cuteSV /
--max_cluster_bias_INS 1 /
--diff_ratio_merging_INS 0.3 /
--max_cluster_bias_DEL 1 /
--diff_ratio_merging_DEL 0.3 / 
--max_split_parts -1 /
--min_mapq 7 / 
--min_read_len 1 /
--min_support 1 /
--max_size -1 /
--max_cluster_bias_INV 1 / 
--max_cluster_bias_DUP 1 /
--max_cluster_bias_TRA 1 /
output_splice_cigar.sorted.bam /
reference.fasta /
output.vcf /
working_folder

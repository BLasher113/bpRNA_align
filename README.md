## bpRNA_align
bpRNA_align is a RNA tool used to identify similarity between RNA structures.

#bpRNA-align scripts
bpRNA_align has two python scripts, one that processees the input files and plots the results, and one that performs the alignment algorithm. 

#bpRNA_align.py: This script takes two inputs and has multiple flag options and one output. The output consists of a file where each line contains the alignment information of one pair. input 1) -f, a list of files in either "st" format or "dbn" format. input 2) -w the bandwidth, which is typically set to 1/8 - 1/4 the length of the longest sequence. flag options include -a (to include alignments in the output file), -p (plot M, X, and Y matrices for the aligned structures), -o (specify the name of the output file)

#bpRNA_align_module.py: This module performs the aligning task, once the files are processed and the key information is retreived. 
This module includes the gap penalties and the substitution matrix for scoring. 

An example run file is available, "run_bpRNA_align.sh", and can be run using the following command: "bash run_bpRNA_align.sh"

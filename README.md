# bpRNA-align
bpRNA_align is a novel secondary structure alignment method, involving a customized global structural alignment approach. This method utilizes an inverted (gap extend costs more than gap open) and context-specific affine gap penalty along with a structural, feature-specific substitution matrix to provide structural similarity scores. bpRNA-align shows alignment peformace increases over a broad range of structure types.

## bpRNA-align scripts
bpRNA_align has two python scripts, one that processees the input files and plots the output results (bpRNA_align.py), and one that performs the alignment algorithm (bpRNA_align_module.py). 

## bpRNA_align.py: 
This script takes two inputs, has multiple flag options and outputs the results. The output consists of a file where each line contains the alignment information of one pair of structures (ex. name_1, name_2, score, or ex. name_1, name_2, alignment_1, alignment_2, score). input 1) -f, a file containing the structural file locations, where the structural files are either in "st" format or "dbn" format (ex. file_list.txt). input 2) -w the bandwidth, which is typically set to 1/4 the length of the longest sequence, but is designed to be tuned by the user for the specific data set being analyzed. flag options include -a (to include alignments in the output file), -p (plot M, X, and Y matrices for the aligned structures), -o (specify the name of the output file)

## bpRNA_align_module.py: 
This module performs the aligning task, once the files are processed and the key information is retreived. 
This module includes the gap penalties and the substitution matrix for scoring. 

An example run file for bpRNA-align is available, "run_bpRNA_align.sh", and can be run using the following command: "bash run_bpRNA_align.sh"

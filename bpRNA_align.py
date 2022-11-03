import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import os, sys
import argparse
import bpRNA_align_module as alignment
import numpy as np

def plot_matrix(middle_matrix, X_matrix, Y_matrix, name_1, name_2):
    M = list(set(np.partition(middle_matrix.flatten(), 1)))[1]
    X = list(set(np.partition(X_matrix.flatten(), 1)))[1]
    Y = list(set(np.partition(Y_matrix.flatten(), 1)))[1]
    min_range = min(M,X,Y)
    fig, axes = plt.subplots(ncols=3, sharey=True)
    axes[0].imshow(X_matrix, vmin = min_range)
    axes[0].set_xlabel(name_1)
    axes[0].set_ylabel(name_2)
    axes[0].set_title("X Matrix")
    axes[1].imshow(middle_matrix, vmin = min_range)
    axes[1].set_xlabel(name_1)
    axes[1].set_title("M Matrix")
    axes[2].imshow(Y_matrix, vmin = min_range)
    im = axes[2].imshow(Y_matrix, vmin = min_range)
    axes[2].set_xlabel(name_1)
    axes[2].set_title("Y Matrix")
    clb = fig.colorbar(im, ax=axes.ravel().tolist(), shrink= 0.4)
    clb.ax.set_title('Score')
    plt.savefig(name_1 + "_" + name_2 + "_alignment_matrices.pdf")
    plt.clf()
       
def get_struct_info(st_file):
    # Get structure array and db information
    with open(st_file, 'r') as st_info:
        count = 0
        for i, line in enumerate(st_info):
            if line[0] != "#":
                count += 1
            if count == 2:
                db = line.strip()
            if count == 3:
                ss = line.strip()
    return ss, db

def pair_files(file_list_file):
    # Determine unique pairs to align
    files = []
    with open(file_list_file, 'r') as file_list:
        for line in file_list:
            files.append(line.strip())
    pairs = []
    for name_i in files:
        for name_j in files:
            if name_j != name_i and (name_j, name_i) not in pairs and (name_i, name_j) not in pairs:
                pairs.append((name_j, name_i))
    return pairs 

def get_align_results(file_pairs):
    # Align structure pairs
    with open(output_file, 'w') as output:
        if show_alignment == True:
            output.write("name_1\tname_2\talignment_1\talignment_2\tscore")
        elif show_alignment == False:
            output.write("name_1\tname_2\tscore")
        for file_pair in file_pairs:
            file_1 = file_pair[0]
            file_2 = file_pair[1]
            name_1 = file_1.split("/")[-1].split(".")[0]
            name_2 = file_2.split("/")[-1].split(".")[0]
            type_1 = file_1.split("/")[-1].split(".")[1]
            type_2 = file_2.split("/")[-1].split(".")[1]
        # Check file type and create st file type if given DBN
            if type_1 != "st":
                if type_1 == "dbn" or type_1 == "DBN":
                    os.system("perl bpRNA.pl " + file_1)
                    file_1 = name_1 + ".st"
                else:
                    print("Incorrect file type used, try dbn or st instead")
            if type_2 != "st":
                if type_2 == "dbn" or type_2 == "DBN":
                    os.system("perl bpRNA.pl " + file_2)
                    file_2 = name_2 + ".st"
                else:
                    print("Incorrect file type used, try dbn or st instead")
            str_1, db_1 = get_struct_info(file_1) 
            str_2, db_2 = get_struct_info(file_2)
            if len(db_1) <= len(db_2):
                y_label = name_1
                x_label = name_2
                align_str_1, align_str_2, dist, score, X_matrix, Y_matrix, middle_matrix = alignment.score_alignment(str_1, str_2, db_1, db_2, w)
            elif len(db_2) < len(db_1):
                y_label = name_2
                x_label = name_1
                align_str_1, align_str_2, dist, score, X_matrix, Y_matrix, middle_matrix = alignment.score_alignment(str_2, str_1, db_2, db_1, w)
            if plot_matrices == True:
                plot_matrix(middle_matrix, X_matrix, Y_matrix, x_label, y_label)
            
            if show_alignment == True:
                output.write("\n" + y_label +"\t" + x_label + "\t" + align_str_1 + "\t" + align_str_2 + "\t" + str(score))
            elif show_alignment != True:
                output.write("\n" + y_label +"\t" + x_label + "\t" + str(score))
            
########
##MAIN##
########

# Add argument flags and required inputs
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file_list_file", required=True, help="A text file containing a list of .st files or .dbn files", type=str)
parser.add_argument("-w","--bandwidth", required=True, help="The band width", type=int)
parser.add_argument("-a", "--show_alignment", required=False, help="Output alignments (True, False)", choices=[True, False], default=False, type=bool)
parser.add_argument("-p","--plot_matrices", required=False, help="plot_matrices (True, False)", type=bool, choices=[True, False], default=False)
parser.add_argument("-o", "--output_file", required = False, default = "align_output.txt", help="Output file name containing alignment score results", type=str)
args = parser.parse_args()

# Asign variables from input arguments
file_list_file = args.file_list_file
w = args.bandwidth
show_alignment = args.show_alignment
plot_matrices = args.plot_matrices
output_file = args.output_file

# Function calls
file_pairs = pair_files(file_list_file)
get_align_results(file_pairs)

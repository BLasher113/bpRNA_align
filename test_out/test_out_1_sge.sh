#!/bin/bash
# BEGIN SGE OPTIONS DECLARATIONS
# Export all environment variables
#$ -V
#
#$ -v TMPDIR=/data
# Your job name
#$ -N test_out
#
# Shell Environment
#$ -S /bin/bash
#
# Use current working directory
#$ -cwd
#
# Set queue to use
#$ -q nucleotide@uracil.cgrb.oregonstate.local
#
#Output files for stdout and stderr
#$ -o test_out
#$ -e test_out
#
# END SGE OPTIONS DECLARATIONS
#
PATH=/local/cluster/sge/bin/lx-amd64:/local/cluster/sge/bin:/local/cluster/sge/bin/lx-amd64:/home/bb/lasherb/scripts:/home/bb/lasherb/bin:/local/cluster/jdk1.8.0_71/jre/bin:/bin:/usr/bin:/local/cluster/ncbi-blast+/bin:/local/cluster/bin:/usr/local/bin:/local/cluster/mpich/bin:/usr/local/share/ncbi/bin:/local/cluster/hdf5-1.8.12/bin:/local/cluster/genome/bin:/local/cluster/RECON/bin:/local/cluster/RECON/scripts:/local/cluster/mummer/bin:/local/cluster/amos/bin:/local/cluster/velvet/velvet:/local/cluster/oases:/local/cluster/mira/bin:/local/cluster/abyss/bin:/local/cluster/edena2.1.1_linux64:/local/cluster/MAKER/bin:/local/cluster/mcl/bin:/local/cluster/YASRA/bin:/local/cluster/miRanda/bin:/local/cluster/ea-utils/bin:/local/cluster/RAxML/bin:/local/cluster/MOSAIK/bin:/local/cluster/hmmer/bin:/local/cluster/meme/bin:/local/cluster/tmhmm/bin:/local/cluster/wgs/Linux-amd64/bin:/local/cluster/amber16/bin:/local/cluster/mpich2-1.2.1p1/bin:/usr/lib64/lam/bin:/local/cluster/mockler/bin:/local/cluster/carrington/bin:/local/cluster/variscan-2.0.3/bin/Linux-i386:/local/cluster/Roche/454/bin:/local/cluster/shore:/local/cluster/SHOREmap:/local/cluster/BEAST2/bin:/local/cluster/BEDTools/bin:/local/cluster/genomemapper:/local/cluster/iprscan/bin:/local/cluster/trinityrnaseq:/local/cluster/Cerulean/bin:/local/cluster/Quake/bin:/local/cluster/glimmer/bin:/local/cluster/samtools/bin:/local/cluster/SPAdes/bin:/local/cluster/RAPSearch2.16_64bits/bin:/local/cluster/last-418/bin:/local/cluster/rnammer:/local/cluster/SHRiMP/bin:/local/cluster/homer/bin:/local/cluster/cd-hit/bin:/local/cluster/ProtHint/bin:/local/cluster/augustus/bin:/local/cluster/structure_linux_console/bin:/local/cluster/stampy:/local/cluster/infernal/bin:/local/cluster/rtax:/local/cluster/pandaseq/bin:/local/cluster/htsjdk/dist:/local/cluster/GARM:/local/cluster/AmpliconNoise/ampliconnoise/Scripts:/local/cluster/AmpliconNoise/ampliconnoise:/local/cluster/pplacer-v1.1:/local/cluster/microbiomeutil/WigeoN:/local/cluster/microbiomeutil/TreeChopper:/local/cluster/microbiomeutil/NAST-iEr:/local/cluster/microbiomeutil/ChimeraSlayer:/local/cluster/AmosCmp16Spipeline:/local/cluster/Tisean_3.0.0/bin:/local/cluster/allpathslg/bin:/local/cluster/NAMD:/local/cluster/vcf/bin:/local/cluster/iRODS/clients/icommands/bin:/local/cluster/SVMerge/bin:/local/cluster/pindel/bin:/local/cluster/breakdancer-1.1.2/bin:/local/cluster/cnD/bin:/local/cluster/nextclip/bin:/local/cluster/prokka/bin:/local/cluster/CEGMA_v2.5/bin:/local/cluster/jnet/bin:/local/cluster/mongodb/bin:/local/cluster/gsl/bin/:/local/cluster/sratoolkit/bin:/local/cluster/wise2.2.3-rc7/src/bin:/local/cluster/CEGMA_v2.5/bin:/local/cluster/freebayes/bin:/local/cluster/stacks/bin:/local/cluster/PhyloTreePruner:/local/cluster/glpk/bin:/local/cluster/metaphlan/bin:/local/cluster/SOAPdenovo-Trans/bin:/local/cluster/ruby/bin:/local/cluster/fastqc:/local/cluster/PBSuite_15.8.24/bin:/local/cluster/detonate-1.10/bin:/local/cluster/canu/bin:/local/cluster/Blast2GO/bin:/local/cluster/JAGS-4.2.0/bin:/local/cluster/capnproto-c++/bin:/local/cluster/ucsc_genome:/local/cluster/vcflib/bin:/local/cluster/tre/bin:/local/cluster/MaSuRCA/bin:/local/cluster/bib/active/bin:/local/cluster/Platypus/bin:/local/cluster/rMATS/bin:/local/cluster/sox/bin:/local/cluster/hisat2:/local/cluster/bbmap:/local/cluster/mirdeep2/bin:/local/cluster/groff-1.22.3/bin:/local/cluster/EPACTS/bin:/local/cluster/percolator/bin:/local/cluster/gmap/bin:/local/cluster/discovardenovo/bin:/local/cluster/BRAKER/bin:/local/cluster/ngsTools/bin:/local/cluster/MATLAB/R2018a/bin:/local/cluster/berkeley_upc/bin:/local/cluster/metaWRAP/bin:/local/cluster/snp-sites/bin:/local/cluster/mafft/bin:/local/cluster/rust/bin:/local/cluster/rocm/bin:/local/cluster/fastx_toolkit_0.0.13:/local/cluster/phast:/local/cluster/gmes_linux_64:/local/cluster/OrthoFinder:/local/cluster/phyloFlash/bin:/local/cluster/edirect/bin:/local/cluster/ITSx/bin:/local/cluster/pheniqs:/local/cluster/sanger-pathogens-Roary-v3.13.0-7-g12a726e/bin:/local/cluster/LTR_retriever:/local/cluster/go/bin:/local/cluster/anchorwave/bin:/local/cluster/ViennaRNA-2.3.5/bin:/local/cluster/nco-5.1.1-alpha09/bin:/local/cluster/meryl/bin:/local/cluster/centrifuge/bin:/local/cluster/smalt/bin:/local/cluster/links/bin:/local/cluster/polypolish:/local/cluster/RSEM/bin:/local/cluster/tRNAscan-SE/bin:/local/cluster/meme/bin:/local/cluster/bifrost/bin:/local/cluster/metabat2/bin:/usr/X11R6/bin:/usr/X/bin:./:/local/cluster/dowser/bin:/local/cluster/dowser/bin/linux:/home/bb/lasherb/RNAz/bin
export PATH
#
#
#The following auto-generated commands will be run by the execution node.
#We execute your command via /usr/bin/time with a custom format
#so that the memory usage and other stats can be tracked; note that
#GNU time v1.7 has a bug in that it reports 4X too much memory usage
echo "  Started on:           " `/bin/hostname -s` 
echo "  Started at:           " `/bin/date` 
/usr/bin/time -f " \\tFull Command:                      %C \\n\\tMemory (kb):                       %M \\n\\t# SWAP  (freq):                    %W \\n\\t# Waits (freq):                    %w \\n\\tCPU (percent):                     %P \\n\\tTime (seconds):                    %e \\n\\tTime (hh:mm:ss.ms):                %E \\n\\tSystem CPU Time (seconds):         %S \\n\\tUser   CPU Time (seconds):         %U " \
bash run_bpRNA_align.sh
echo "  Finished at:           " `date` 

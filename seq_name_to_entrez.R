library("org.Ce.eg.db")
ls("package:org.Ce.eg.db")
seq.names <- readLines("unique_sequence_names.txt")

# entrezg -> ensembl_trans(s)
x <- org.Ce.egENSEMBLTRANS
mapped_genes <- mappedkeys(x)
entrez2trans <- as.list(x[mapped_genes])

#For the reverse map ENSEMBLTRANS2EG:
# Convert to a list
trans2entrez <- as.list(org.Ce.egENSEMBLTRANS2EG)

zz <- mget(seq.names, org.Ce.egENSEMBLTRANS2EG, ifnotfound=NA)
# this does not work.
# e.g., ZK867.1 is NA, but maps to syd-9 gene in
# http://useast.ensembl.org/Caenorhabditis_elegans/Gene/Summary?g=ZK867.1;r=X:7218109-7226045

# BioMart: ensembl genes, Caenorhabitis elegans genes
#

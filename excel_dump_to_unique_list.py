#!/usr/bin/python
"""Includes transcription factors, histone encoding genes, and "chromatic remoding, general transcription, and DNA/RNA binding factors in C. elegans."""
seq_names = set()
for line in open("celegans_genelist.txt", 'rU'):
  line = line.strip()
  if line and line[0]=="#": continue
  seq_names.add(line.partition('\t')[0])
for s in sorted(seq_names):
  print s

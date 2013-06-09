# list of ensembl sequence names
seq_names = set((s.strip() for s in open("unique_sequence_names.txt", "rU") if s.strip()))

# Parse ensembl_biomart query
# Ensembl Gene ID,Ensembl Transcript ID,EntrezGene ID,Associated Gene Name,Associated Transcript Name,WikiGene Name,WormBase Sequence Name
ensembld = {}
all_ensembl = set()
for line in open("ensembl_query_all.csv","rU"):
  row = line.strip().split(',')
  ensembl_gene_id = row[0]
  d = ensembld.setdefault(ensembl_gene_id,{})
  d.setdefault('Ensembl Transcript ID',set()).add(row[1])
  d.setdefault('EntrezGene ID',set()).add(row[2])
  d.setdefault('Associated Gene Name',set()).add(row[3])
  d.setdefault('WikiGene Name',set()).add(row[5])
  all_ensembl.update((ensembl_gene_id, row[1]))

print len(seq_names), len(all_ensembl), len(seq_names&all_ensembl)
ensembl_ids = set(ensembld.keys())
print len(seq_names), len(ensembl_ids), len(seq_names&all_ensembl)
print seq_names - ensembl_ids
#set(['R13.1', 'F57G4.6', 'T05C3.1', 'Y26D4A.9', 'T07G12.13', 'Y77E11A.5', 'R05D3.1', 'Y95B8A.7', 'C39E6.3', 'T11A5.1', 'Y17D7A.2', 'F26H11.3', 'Y37A1B.1a', 'T01C1.3', 'K08A2.7', 'Y48G8AL.9', 'F29D10.5', 'C11G6.3'])
# seq_names not found in ensembl_ids. Manually searched in wormbase.org for explanations...
MANUAL_REMAP = {
  'R13.1': 'R13.4', # http://www.wormbase.org/species/c_elegans/gene/WBGene00011256?query=R13.1#0-9e-3
  'F57G4.6': None, # http://www.wormbase.org/species/c_elegans/gene/WBGene00010211?query=F57G4.6#0-9e-3
  'T05C3.1': 'C24G6.4', # http://www.wormbase.org/species/c_elegans/gene/WBGene00020253?query=T05C3.1#0-9e-3
  'Y26D4A.9': None, # http://www.wormbase.org/species/c_elegans/gene/WBGene00012506#0-9e-3
  'T07G12.13': 'T07G12.6', # http://www.wormbase.org/species/c_elegans/gene/WBGene00011603?query=T07G12.13#0-9e-3
  'Y77E11A.5': 'Y104H12A.1', # http://www.wormbase.org/species/c_elegans/gene/WBGene00003631?query=Y77E11A.5#0-9e-3
  'R05D3.1': 'R05D3.12', # http://www.wormbase.org/species/c_elegans/gene/WBGene00019876?query=R05D3.1#0-9e-3
  'Y95B8A.7': 'Y95B8A.8', # http://www.wormbase.org/species/c_elegans/gene/WBGene00022387?query=Y95B8A.7#0-9e-3
  'C39E6.3': None, # http://www.wormbase.org/species/c_elegans/gene/WBGene00043185?query=C39E6.3#0-9e-3
  'T11A5.1': 'R07B5.9', # http://www.wormbase.org/species/c_elegans/gene/WBGene00011700?query=T11A5.1#0-9e-3
  'Y17D7A.2': 'Y17D7A.1', # http://www.wormbase.org/species/c_elegans/gene/WBGene00012447?query=Y17D7A.2#0-9e-3
  'F26H11.3': 'F26H11.2', # http://www.wormbase.org/species/c_elegans/gene/WBGene00009181?query=F26H11.3#0-9e-3
  'Y37A1B.1a': 'Y37A1B.1', # http://www.wormbase.org/species/c_elegans/gene/WBGene00003085#0-9e-3
  'T01C1.3': 'T01C1.2', # http://www.wormbase.org/species/c_elegans/gene/WBGene00011316?query=T01C1.3#0-9e-3
  'K08A2.7': None, # http://www.wormbase.org/species/c_elegans/gene/WBGene00043420?query=K08A2.7#0-9e-3
  'Y48G8AL.9': 'Y48G8AL.10', # http://www.wormbase.org/species/c_elegans/gene/WBGene00009181?query=F26H11.3#0-9e-3
  'F29D10.5': 'F55H12.6', # http://www.wormbase.org/species/c_elegans/gene/WBGene00009253?query=F29D10.5#0-9e-3
  'C11G6.3': 'C11G6.1', # http://www.wormbase.org/species/c_elegans/gene/WBGene00007524?query=C11G6.3#0-9e-3
}
  
# remap and filter problematic sequence names
seq_names_filt = filter(None, map(lambda x: MANUAL_REMAP.get(x,x), seq_names))
print len(seq_names_filt)
seq_names_filt = set(seq_names_filt)
print len(seq_names_filt)

for s in sorted(seq_names_filt):
  print "%s\t%s" % (s, "|".join(sorted(ensembld[s]['EntrezGene ID'])))
print


print "Entrez To Ensembl: Transcription factors, histones, etc."
print "------------------------------"
fp = open("entrez_transcriptome_list.tab", "w")
fp.write("EntrezID\tEnsemblTranscriptID\tGeneSymbols\n")
eids = set()
for s in sorted(seq_names_filt):
  for eid in sorted(ensembld[s]['EntrezGene ID']):
    if eid:
      line = "\t".join((eid, s, "|".join(ensembld[s]["Associated Gene Name"] | ensembld[s]["WikiGene Name"])))
      print line
      print >>fp, line
      eids.add(eid)

fp.close()
print "Wrote entrez_transcriptome_list.tab"
print
print "Total number of unique entrezIDs to consider: ", len(eids)

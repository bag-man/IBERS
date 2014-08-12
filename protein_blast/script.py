from rjv.fasta import next_fasta

barleyFile = "barley_HighConf_genes_MIPS_23Mar12_ProteinSeq.fa"
brachyFile = "Bdistachyon_192_protein_primaryTranscriptOnly.fa"
oatFile = "tg7_proteins_high.fa"

def createList(fileName):
  resultList = []
  for record in next_fasta(fileName):
    resultList.append({'header':record['header'], 'length':record['len']})

  return resultList

barleyData = createList(barleyFile)
brachyData = createList(brachyFile)
oatData = createList(oatFile)

print oatData[0]

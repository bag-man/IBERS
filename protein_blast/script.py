from rjv.fasta import next_fasta
import csv

barleyFile = "barley_HighConf_genes_MIPS_23Mar12_ProteinSeq.fa"
brachyFile = "Bdistachyon_192_protein_primaryTranscriptOnly.fa"
oatFile = "tg7_proteins_high.fa"

oatsBlast = open("oatsBlast.tsv",'r')
oatsBlast = csv.reader(oatsBlast, delimiter='\t')

def createList(fileName):
  resultList = {}
  for record in next_fasta(fileName):
    resultList[record['header']] = record

  return resultList

brachyData = createList(brachyFile)

def testBlastFile(fileName, source):
  bestHits = {}

  for line in fileName:
    if line[0] not in bestHits:
      bestHits[line[0]] = line
    elif int(line[4]) > int(bestHits[line[0]][4]):
      bestHits[line[0]] = line
      
  for key, value in bestHits.items():
    print "Key: ", bestHits[key][1], "Percent Align.: " , ((float(bestHits[key][4]) / brachyData[bestHits[key][1]]['len']) * 100)

testBlastFile(oatsBlast, "oats")

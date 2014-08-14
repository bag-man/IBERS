from rjv.fasta import next_fasta
from numpy.random import normal
import matplotlib.pyplot as plt
import csv, sys

blastFiles=\
	  '''
	    inputs/oatsBarleyBlast.tsv
	    inputs/oatsBrachyBlast.tsv
	    inputs/oatsSbiBlast.tsv
	    inputs/oatsOstaviaBlast.tsv
	  '''.split()

dataBaseFiles=\
	    '''
	      inputs/barley_HighConf_genes_MIPS_23Mar12_ProteinSeq.fa
	      inputs/Bdistachyon_192_protein_primaryTranscriptOnly.fa
	      inputs/Sbicolor_79_protein_primaryTranscriptOnly.fa
	      inputs/Osativa_204_protein_primaryTranscriptOnly.fa
	    '''.split()

def createList(fileName):
  resultList = {}
  for record in next_fasta(fileName):
    resultList[record['header']] = record

  return resultList

def testBlastFile(fileName):
  bestHits = {}
  outputList = []
  scoreField = 4

  for line in fileName:
    if line[0] not in bestHits:
      bestHits[line[0]] = line
    elif int(line[scoreField]) > int(bestHits[line[0]][4]):
      bestHits[line[0]] = line
      
  for key, value in bestHits.items():
    oatsID = bestHits[key][0]
    dataBaseID = bestHits[key][1]
    bestHits[key][11] = bestHits[key][11].strip()
    alignLength = float(bestHits[key][scoreField])
    brachyGeneLength = float(inputData[bestHits[key][1]]['len'])
    percentAlign = (alignLength / brachyGeneLength) * 100
    bestHits[key].append(str(percentAlign))
    outputList.append(bestHits[key])

  return outputList

output = []
for blast in blastFiles:
  inputData = createList(dataBaseFiles[blastFiles.index(blast)])
  blastFile = open(blast,'r')
  blastFile = csv.reader(blastFile, delimiter='\t')
  output = testBlastFile(blastFile)
  myfile = open("outputs/output.csv", 'a')
  wr = csv.writer(myfile)
  wr.writerows(output)

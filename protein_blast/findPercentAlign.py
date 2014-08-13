from rjv.fasta import next_fasta
import matplotlib.pyplot as plt
from numpy.random import normal
import csv

# blastFile = "oatsBarleyBlast.tsv"
# blastFile = "oatsBrachyBlast.tsv"
# blastFile = "oatsSbiBlast.tsv"
# blastFile = "oatsOstaviaBlast.tsv"

# dataBaseFile = "Sbicolor_79_protein_primaryTranscriptOnly.fa"
# dataBaseFile = "barley_HighConf_genes_MIPS_23Mar12_ProteinSeq.fa"
# dataBaseFile = "Bdistachyon_192_protein_primaryTranscriptOnly.fa"
# dataBaseFile = "Osativa_204_protein_primaryTranscriptOnly.fa"

oatsBlast = open(blastFile,'r')
oatsBlast = csv.reader(oatsBlast, delimiter='\t')

scoreField = 4

"""
Field 	  	Description
0 	  	Query label.
1 	  	Target (database sequence or cluster centroid) label.
2 	  	Percent identity.
3 	  	Alignment length.
4 	  	Number of mismatches.
5 	  	Number of gap opens.
6 	  	1-based position of start in query. For translated searches (nucleotide queries, protein targets), query start<end for +ve frame and start>end for -ve frame.
7 	  	1-based position of end in query.
8 	  	1-based position of start in target. For untranslated nucleotide searches, target start<end for plus strand, start>end for minus strand.
9 	  	1-based position of end in target.
10 	  	E-value calculated using Karlin-Altschul statistics.
11 	  	Bit score calculated using Karlin-Altschul statistics.
"""

def createList(fileName):
  resultList = {}
  for record in next_fasta(fileName):
    resultList[record['header']] = record

  return resultList

inputData = createList(dataBaseFile)

def testBlastFile(fileName):
  bestHits = {}
  percAlignList = []

  for line in fileName:
    if line[0] not in bestHits:
      bestHits[line[0]] = line
    elif int(line[scoreField]) > int(bestHits[line[0]][4]):
      bestHits[line[0]] = line
      
  for key, value in bestHits.items():
    oatsID = bestHits[key][0]
    dataBaseID = bestHits[key][1]
    alignLength = float(bestHits[key][scoreField])
    brachyGeneLength = float(inputData[bestHits[key][1]]['len'])
    percentAlign = (alignLength / brachyGeneLength) * 100
    percAlignList.append(percentAlign)
    print oatsID + "," + dataBaseID + "," + str(percentAlign)

  return percAlignList

data = testBlastFile(oatsBlast)

import sys,sqlite3,glob
from os import walk 
from rjv.sql import *
from rjv.fasta import *

dbFile = "../atlantica_database/database/main.db"
tableName = "grass_genes"

columnNames = "spp_id/prot/seq/species"

order = {
  'Bdistachyon_192_transcript_primaryTranscriptOnly.fa': 'Brachy', 
  'barley_HighConf_genes_MIPS_23Mar12_CDSSeq.fa':'Barley', 
  'Sbicolor_79_transcript_primaryTranscriptOnly.fa':'Sorgum',
  'Osativa_204_transcript_primaryTranscriptOnly.fa':'Osativa'
}
files = []
transcripts = []
proteins = {}
sequences = {}

for (dirpath, dirnames, filenames) in walk("proteinSequences"):
  files.extend(filenames)

for (dirpath, dirnames, filenames) in walk("transcripts"):
  transcripts.extend(filenames)

def createDictionary(file, species, seq):
  records = {}
  first = True
  sequence = ""
  for line in file:
    if line[0] == ">": 
      if first is not True:

        if seq == True:
	  records[header] = [sequence, order[species]]
	else:
	  records[header] = [sequence]
        
      header = line.rstrip('\n')[1:]
      sequence = ""
      first = False
      continue
    else:
      sequence += line.rstrip('\n')
      continue
  if seq == True:
    records[header] = [sequence, order[species]]
  else:
    records[header] = [sequence]
  return records
  
for file in files:
  f = open("proteinSequences/" +  file)
  proteins.update(createDictionary(f, file, False))
  f.close()

for file in transcripts:
  t = open("transcripts/" + file)
  sequences.update(createDictionary(t, file, True))
  t.close()

for key in proteins.iterkeys():
  seqkey = key.split('|',1)[0]
  if seqkey in sequences:
    proteins[key].append(sequences[seqkey][0])
    proteins[key].append(sequences[seqkey][1])
  else:
    print key, " ", seqkey
    #sys.exit(0)

con = sql_connect(dbFile)
cur = con.cursor()

create_table(cur,tableName, columnNames)
for key,value in proteins.iteritems():
  try: 
    insert_row(cur,tableName,[key, value[0], value[1], value[2]])
  except:
    print key, " ", value[0], " ", value[1], " ", value[2]

con.commit()
con.close()


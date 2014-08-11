import os
import gzip

def getData(file): 
  source = os.path.basename(file)
  file = open(file, 'r')
  dataList = []

  for line in file:
    filename = line.rstrip()
    size = os.path.getsize(filename)
    gzFile = gzip.open(filename, 'r')
    headerLine = gzFile.readline().rstrip()
    dataList.append({'filePath': filename, 'header': headerLine,  'size': size, 'source': source})
  
  return dataList

quoatsFiles = getData("/ibers/ernie/home/owg1/data/quoats")
repoFiles = getData("/ibers/ernie/home/owg1/data/repo")
commonFiles = []

for record in repoFiles:
  for record2 in quoatsFiles:
    if record['header'] == record2['header']: #or record['size'] == record2['size']: 
      commonFiles.append(record2)

for record in commonFiles:
  print record['header']

quoatsFiles.close()
repoFiles.close()

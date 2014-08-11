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

  file.close()
  gzFile.close()
      
  return dataList

def humanSize(num):
  for x in ['bytes','KB','MB','GB','TB']:
    if num < 1024.0:
      return "%3.1f %s" % (num, x)
    num /= 1024.0

quoatsFiles = getData("/ibers/ernie/home/owg1/IBERS/data/quoats")
repoFiles = getData("/ibers/ernie/home/owg1/IBERS/data/repo")
commonFiles = []

for record in repoFiles:
  for record2 in quoatsFiles:
    if os.path.basename(record['filePath']) == os.path.basename(record2['filePath']) and record['size'] != record2['size']:
      commonFiles.append(record2)
      commonFiles.append(record)

for record in commonFiles:
  print record['filePath'] , " ", humanSize(record['size'])

import os
import sys
import gzip
import sqlite3 as lite
from subprocess import Popen, PIPE

con = lite.connect('data/fileData.db')

with con:
  cur = con.cursor()    
  cur.execute("CREATE TABLE if not exists Files(ID INTEGER PRIMARY KEY AUTOINCREMENT, filePath TEXT, fileName TEXT, sha256 TEXT, headerLine TEXT, size TEXT, source TEXT)")

def humanSize(num):
  for x in ['bytes','KB','MB','GB','TB']:
    if num < 1024.0:
      return "%3.1f %s" % (num, x)
    num /= 1024.0

def hashFile(file):
  proc = Popen(["sha256sum", file], stdout=PIPE, stderr=PIPE)
  out, err = proc.communicate()
  return out.split(' ', 1)[0]


def getData(file): 
  source = os.path.basename(file)
  file = open(file, 'r')
  dataList = []

  for line in file:
    filePath = line.rstrip()
    fileName = os.path.basename(filePath)
    size = humanSize(os.path.getsize(filePath))
    gzFile = gzip.open(filePath, 'r')
    headerLine = gzFile.readline().rstrip()

    sha256 = hashFile(filePath)

    dataList.append({'filePath': filePath, 'filename': fileName, 'sha256': sha256, 'header': headerLine,  'size': size, 'source': source})

    cur.execute("INSERT INTO Files (filePath, fileName, sha256, headerLine, size, source) VALUES (?, ?, ?, ?, ?, ?)"
    , (filePath, fileName, sha256, headerLine, size, source))
    con.commit()

  file.close()
  gzFile.close()
  
  return dataList

#quoatsFiles = getData("/ibers/ernie/home/owg1/IBERS/data/test")
quoatsFiles = getData("/ibers/ernie/home/owg1/IBERS/data/quoats")
repoFiles = getData("/ibers/ernie/home/owg1/IBERS/data/repo")


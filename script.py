#!/bin/bash/python
import os
import gzip


def getData(file): 
  file = open(file, 'r')
  dataList = []

  for line in file:
      filename = line.rstrip()
      gzFile = gzip.open(filename, 'r')
      headerLine = gzFile.readline().rstrip()
      dataList.append([filename, headerLine, os.path.getsize(filename)])
  
  return dataList

quoatsFiles = getData("/ibers/ernie/home/owg1/data/quoats")
repoFiles = getData("/ibers/ernie/home/owg1/data/repo")

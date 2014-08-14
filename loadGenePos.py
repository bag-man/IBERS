#!/usr/bin/python

'''
load gene genetic map positions
'''

import sys,sqlite3,glob
sys.path.append('../../python_lib')
from rjv.sql import *
from rjv.fasta import *

#positioning information in decreasing order of priority
inp =\
'''../gene_posn/gene_snppav_posn_all.csv
../gene_posn/gene_rad_posn_all.csv
../gene_posn/gene_wgs_posn_all.csv
../gene_posn/gene_synteny_posn.csv'''.split()

types = ['dart','rad','wgs', 'syn']
tables = {'dart':{}, 'rad':{}, 'wgs':{}, 'syn':{}}
posn = {}

db = '../database/main.db'

for i,fname in enumerate(inp):
  f = open(fname)
  for line in f:
    tok = line.strip().split(',')
    gene = tok[0]
    lg = int(tok[1])  
    cm = float(tok[2]) 
      
    if not gene in posn:
      posn[gene] = [i,lg,cm]
    
    for key in tables:
      tables[types[i]][gene] = [i, lg, cm] 

  f.close()
                       
con = sql_connect(db)
cur = con.cursor()

create_table(cur,"gposn", 'gene/lg integer/cm real/type')

tableNames = ["gposn_d","gposn_r","gposn_w","gposn_s"]
for table in tableNames:
  create_table(cur,table, 'gene/lg integer/cm real/type')
  i=0
  name = types[tableNames.index(table)]
  for gene,rec in tables[name].iteritems():
      i+=1
      _type = types[rec[0]]
      lg = rec[1]
      cm = rec[2]
      
      insert_row(cur,table,[gene,lg,cm,_type])
		 
      if i%100 == 0: print i

i=0
for gene,rec in posn.iteritems():
    i+=1
    _type = types[rec[0]]
    lg = rec[1]
    cm = rec[2]
    
    insert_row(cur,"gposn",[gene,lg,cm,_type])
               
    if i%100 == 0: print i

f.close()

print 'indexing...'
cur.execute("create unique index %s_indx on %s(gene);"%(table,table))

con.commit()
con.close()


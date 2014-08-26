import os,sys
sys.path.append('/ibers/ernie/groups/quoats/python_lib')
from rjv.fasta import *
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--cluster", dest="cluster", action="store_true", default=False)
parser.add_option("--running", dest="running", action="store_true", default=False)
parser.add_option("--no-split", dest="nosplit", action="store_true", default=False)
parser.add_option("--qprot", dest="qprot")
parser.add_option("--sprot", dest="sprot")
parser.add_option("--qnuc", dest="qnuc")
parser.add_option("--snuc", dest="snuc")
parser.add_option("--subject", dest="subject")
parser.add_option("--query", dest="query")
parser.add_option("--chunks", dest="chunks")
parser.add_option("--threads", dest="threads")

(opt, args) = parser.parse_args()

opt.qprot = "query.fa"
opt.sprot = "subject.fa"
opt.cluster = True
opt.chunks = 4

if opt.qprot and opt.sprot:
  blast = "blastp"
  query = opt.qprot
  subject = opt.sprot
elif opt.qnuc and opt.snuc:
  blast = "blastn"
  query = opt.qnuc
  subject = opt.sprot
elif opt.qprot and opt.snuc:
  blast = "blastx"
  query = opt.qprot
  subject = opt.snuc
elif opt.sprot and opt.qnuc:
  blast = "tblastx"
  query = opt.qnuc
  subject = opt.sprot

if opt.threads is None:
  opt.threads = 2

if opt.chunks:
  opt.chunks = int(opt.chunks)

blastbin="/cm/shared/apps/BLAST/ncbi-blast-2.2.28+/bin/"

dbExists = os.path.isfile("database/" + subject + ".pin")
if dbExists == False:
  if opt.cluster == False: 
    os.system("makeblastdb -in " + subject + " -dbtype prot")
  else:
    os.system(blastbin + "makeblastdb -in " + subject + " -dbtype prot")
  os.system("mv " + subject + ".p* database/")

def split():
  base = "queries/" + query + '.%03d'
  f = [open(base%i,'wb') for i in xrange(opt.chunks)]

  for i,fa in enumerate(next_fasta(query)):
    write_fasta(fa,f[i%opt.chunks])
  
  for x in f: x.close()

if opt.running == False: 

  if opt.chunks > 1 and opt.cluster == True:
    print "Splitting into ", opt.chunks, " chunks"
    split()

  if opt.cluster == False:
    print "Running blast..."
    hostname = os.popen("hostname").read().rstrip('\n')
    if hostname == "bert":
      sys.exit("Oi! Don't run blast on the log in node!")
    os.system("blastp -db database/" + subject + " -query " + query + " -out results/results.tsv -evalue 1e-40 -outfmt 6 -num_threads " + str(opt.threads))
  else:
    hostname = os.popen("hostname").read().rstrip('\n')
    if hostname == "bert":
      if opt.chunks > 1:
	scriptCommand = "python " + sys.argv[0] + " --sprot database/" + subject + " --qprot " + query  + " --running"
	os.system("echo " + scriptCommand + " | qsub -N " + blast + " -cwd -t 1-"+ str(opt.chunks) + " -o logs/log.out -e logs/log.err ")
      else:
	scriptCommand = "python " + sys.argv[0] + " --sprot database/" + subject + " --qprot " + query  + " --running --no-split"
	os.system("echo " + scriptCommand + " | qsub -N " + blast + " -cwd -o logs/log.out -e logs/log.err ")
    else:
      sys.exit("Log in to bert!")
else:
  # This runs on the cluster
  taskId = os.popen("printf '%03d' $((SGE_TASK_ID-1))").read().rstrip('\n')
  if opt.nosplit == True:
    os.system(blastbin + blast + " -db database/" + subject + " -query " + query + " -out results/results.tsv -evalue 1e-40 -outfmt 6")
  else:
    os.system(blastbin + blast + " -db database/" + subject + " -query queries/" + query + "." + str(taskId) + " -out results/results." + str(taskId) + ".tsv -evalue 1e-40 -outfmt 6")



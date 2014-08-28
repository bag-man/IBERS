import os,sys
from optparse import OptionParser

usage =\
"""
	%prog --qprot query.fa --sprot subject.fa --threads 32
	blast.py --qprot query.fa --sprot subject.fa --cluster --threads 64 --memory 10G --runtime '01:00:00' --email 'abc@aber.ac.uk' """


parser = OptionParser(usage=usage)
parser.add_option("--cluster", dest="cluster", action="store_true", default=False, help="Run on the cluster")
parser.add_option("--qprot", dest="qprot", help="Query a protein")
parser.add_option("--sprot", dest="sprot", help="Create a protein subject")
parser.add_option("--qnuc", dest="qnuc", help="Query a nucleotide")
parser.add_option("--snuc", dest="snuc", help="Create a nucleotide subject")
parser.add_option("--email", dest="email", help="Add your email address to get notified when job is done")
parser.add_option("--threads", dest="threads", help="How many cores/threads to use", default=4)
parser.add_option("--memory", dest="memory", help="How much memory to allocate on the cluster")
parser.add_option("--runtime", dest="runtime", help="How much runtime to allocate on the cluster")
parser.add_option("--running", dest="running", action="store_true", default=False)

(opt, args) = parser.parse_args()

"""
opt.qprot = "query.fa"
opt.sprot = "subject.fa"
opt.cluster = True
opt.email = "garland.owen@gmail.com"
opt.threads = 4
"""
  
if opt.qprot is None and opt.qnuc is None:
  parser.print_help()
  sys.exit("Error: No query provided")

if opt.sprot is None and opt.snuc is None:
  parser.print_help()
  sys.exit("Error: No subject provided")

if opt.cluster:
  if not opt.threads or not opt.memory or not opt.runtime:
    parser.print_help()
    sys.exit("Error: Cluster requires threads, memory and runtime")

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

dbExists = os.path.isdir("database/")
if dbExists == False:
  if opt.sprot:
    type = "prot"
    t = "T"
  elif opt.snuc:
    type = "nucl"
    t = "F"

  os.makedirs("database")
  if opt.cluster == False: 
    os.system("makeblastdb -in " + subject + " -dbtype " + type)
    os.system("mv " + subject + ".* database/")
  else:
    blastbin = "/cm/shared/apps/mpiblast/current/bin/"
    os.system(blastbin + "mpiformatdb -i " + subject + " -p " + t + " -n database/ --nfrags=" + str(opt.threads))

if opt.running == False: 
  if opt.cluster == False:
    print "Running blast..."
    hostname = os.popen("hostname").read().rstrip('\n')
    if hostname == "bert":
      sys.exit("Oi! Don't run blast on the log in node!")
    os.system("blastp -db database/" + subject + " -query " + query + " -out results.tsv -evalue 1e-40 -outfmt 6 -num_threads " + str(opt.threads))
  else:
    hostname = os.popen("hostname").read().rstrip('\n')
    if hostname == "bert":
      if opt.email:
	scriptCommand = "python " + sys.argv[0] + " --sprot " + subject + " --qprot " + query + " --threads " + str(opt.threads) + " --memory " + opt.memory + " --runtime " + opt.runtime + " --email " + opt.email + " --running"
	os.system("echo " + scriptCommand + " | qsub -N " + blast + " -M " + opt.email + " -m e -cwd -o log -R y -l h_vmem=" + opt.memory + ",h_rt=" + opt.runtime + " -e log -pe mpich " + str(opt.threads))
      else:
	scriptCommand = "python " + sys.argv[0] + " --sprot " + subject + " --qprot " + query + " --threads " + str(opt.threads) + " --memory " + opt.memory + " --runtime " + opt.runtime + " --running"
	os.system("echo " + scriptCommand + " | qsub -N " + blast + " -cwd -o log -R y -l h_vmem=" + opt.memory + ",h_rt=" + opt.runtime + " -e log -pe mpich " + str(opt.threads))
    else:
      sys.exit("Log in to bert!")
else:
  # This runs on the cluster
  mpiblast = "/cm/shared/apps/mpiblast/current/bin/mpiblast"
  mpiexec = "/cm/shared/apps/openmpi/open64/64/1.4.4/bin/mpiexec"
  os.environ["BLASTMAT"] = "/cm/shared/apps/BLAST/blast-2.2.28/data/" 
  os.system(mpiexec + " -n " + str(opt.threads) + " " + mpiblast + " -p " + blast + " -d " + subject + " -i " + query + " -e 1e-40 -o results.tsv -m 8")

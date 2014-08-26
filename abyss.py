import os, sys, time, subprocess
from optparse import OptionParser
os.environ['PATH'] += os.pathsep + '/cm/shared/apps/abyss/1.3.7/bin/'
os.environ['PATH'] += os.pathsep + '/cm/shared/apps/openmpi/open64/64/1.4.4/bin/'

parser = OptionParser()
parser.add_option("--cluster", dest="cluster", action="store_true", default=False)
parser.add_option("--running", dest="running", action="store_true", default=False)
parser.add_option("--cores", dest="cores")
parser.add_option("--kmer", dest="kmer")
parser.add_option("--name", dest="name")
parser.add_option("--file1", dest="file1")
parser.add_option("--file2", dest="file2")

(opt, args) = parser.parse_args()

opt.file1 = "ERR580964_1.fastq"
opt.file2 = "ERR580964_2.fastq"
opt.kmer = 33
opt.cores = 2
opt.name = "Test"
opt.cluster = True

if opt.running == False: 
  if opt.cluster == False:
    hostname = os.popen("hostname").read().rstrip('\n')
    if hostname == "bert":
      sys.exit("Oi! Don't run abyss on the log in node!")
    print "Running abyss..."
    os.system("abyss-pe k=" + str(opt.kmer) + " name='" + opt.name + "'in='" + opt.file1 + " " + opt.file2 + "' np='" + str(opt.cores) + "'")
  else:
    hostname = os.popen("hostname").read().rstrip('\n')
    if hostname == "bert":
      scriptCommand = "python " + sys.argv[0] + " --name " + opt.name + " --cores " + str(opt.cores)  + " --file1 " + opt.file1 + " --file2 " + opt.file2  + " --kmer " + str(opt.kmer) + " --running"
      os.system("echo " + scriptCommand + " | qsub -N " + opt.name + " -cwd -o log -e log -l h_vmem=4G,h_rt=01:00:00 -R y -pe openmpi " + str(opt.cores)) # I will add memory and run time options
    else:
      sys.exit("Log in to bert!")
else:
  # This runs on the cluster
  os.system("abyss-pe k='" + str(opt.kmer) + "' in='" + opt.file1 + " " + opt.file2 + "'")  


#$ -S /bin/sh
#$ -N blastn
#$ -o ../scr/logs/$JOB_NAME.$JOB_ID.$TASK_ID.out
#$ -e ../scr/logs/$JOB_NAME.$JOB_ID.$TASK_ID.err
#$ -cwd
#$ -l h_vmem=1G
###$ -q amd.q
#$ -t 1-10

#
# blastn hexaploid GBS against atlantica transcriptome
#

# makeblastdb -in ./Bdistachyon_192_protein_primaryTranscriptOnly.fa -dbtype prot

taskid=`printf "%03d" $((SGE_TASK_ID-1))`
query="../scr/ahoy_map/ahoy2_final-${taskid}.fa"

db='../../annotation_2013-11-05/scr/atlantica_annotation_20140226/tg7_unspliced.fa'
output="../scr/blastn_ahoy/fwd_${taskid}.tsv"

blastn='/cm/shared/apps/BLAST/ncbi-blast-2.2.28+/bin/blastn'
blastp='/cm/shared/apps/BLAST/ncbi-blast-2.2.28+/bin/blastp'
outfmt='6'
ops='-evalue 1e-40'

#blastp -db Bdistachyon_193_protein_primaryTranscriptOnly.fa -query tg7_proteins_high.fa -out output.tsv -evalue 1e-40 -outfmt 6
${blastp} -db ${db} -query ${query} -out ${output} ${ops} -outfmt ${outfmt}

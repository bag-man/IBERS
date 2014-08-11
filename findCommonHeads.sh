#!/bin/bash
rm repo* quoats*
find  /ibers/repository/sequencer/illumina/tt* -name *.gz | grep -v rawfastq > repo # Filter out rawfastq subdirs
find  /ibers/ernie/groups/quoats/archival-fastqs/IlluminaData/ -name *.gz > quoats

for filename in `cat quoats`; do
  zcat $filename | head -n 1 >> quoatsheads
  #zcat $filename | head -n 1 | awk -F ":" '{print $1":"$2":"$3":"$4":"$5}' >> quoatsheads # Get just the first 5 params of the head
done

for filename in `cat repo`; do
  zcat $filename | head -n 1 >> repoheads
  #zcat $filename | head -n 1 | awk -F ":" '{print $1":"$2":"$3":"$4":"$5}' >> repoheads # Get just the first 5 params of the head
done

sort repoheads > reposort
sort quoatsheads > quoatssort

comm -12 reposort quoatssort | nl
echo "finished"
rm repo* quoats*

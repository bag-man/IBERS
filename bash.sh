#!/bin/bash
find  /ibers/repository/sequencer/illumina/tt* -name *.gz > repo
find  /ibers/ernie/groups/quoats/archival-fastqs/IlluminaData/ -name *.gz > quoats

for filename in `cat quoats`; do
  zcat $filename | head -n 1 >> quoatsheads
done

for filename in `cat repo`; do
  zcat $filename | head -n 1 >> repoheads
done

sort repoheads > reposort
sort quoatsheads > quoatssort

comm -12 reposort quoatssort | nl
rm repo* quoats*

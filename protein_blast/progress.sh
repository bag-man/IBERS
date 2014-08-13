inFile=$1
outFile=$2
inFileTotal=$(wc -l < $inFile)
outPos=$(tail -1 $2| awk -F " " '{print $1}')
outPos=$(grep -n $outPos $1 | cut -f1 -d:)
while [[ ${percent%.*} -ne "100" ]]; do
  percent=$(echo "scale=2; $outPos / $inFileTotal * 100" | bc)
  echo ${percent%.*} | dialog --gauge "Please wait" 10 70 0
  sleep 5
done


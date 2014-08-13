inFile=$1
outFile=$2
inFileTotal=$(wc -l < $inFile)
outPos=$(tail -1 $2| awk -F " " '{print $1}')
outPos=$(grep -n $outPos $1 | cut -f1 -d:)
percent=$(echo "scale=2; $outPos / $inFileTotal * 100" | bc)
echo -n $percent "%"


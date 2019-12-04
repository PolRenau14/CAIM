#!/bin/sh

echo "ExtractData.py --index $1 --minfreq $2 --maxfreq $3 --numwords $4" > Output/Exp1/outputMRK$5.txt
python3 ExtractData.py --index $1 --minfreq $2 --maxfreq $3 --numwords $4
python3 GeneratePrototypes.py --nclust 20
echo "MRK MEANS: " >> Output/Exp1/outputMRK$5.txt
python3 MRKmeans.py >> Output/Exp1/outputMRK$5.txt
echo "PROCESS RESULTS: " >> Output/Exp1/outputMRK$5.txt
python3 ProcessResults.py >> Output/Exp1/outputMRK$5.txt

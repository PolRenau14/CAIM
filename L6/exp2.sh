#!/bin/sh

echo "Experimento jugando con los valores para iter y ncores" > Output/Exp2/200/outputMRK$1.$2.txt
echo "20 clases, iter: $1, ncores: $2" >> Output/Exp2/200/outputMRK$1.$2.txt

echo "MRK MEANS: " >> Output/Exp2/200/outputMRK$1.$2.txt
python3 MRKmeans.py --iter $1 --ncores $2 >> Output/Exp2/200/outputMRK$1.$2.txt
echo "PROCESS RESULTS: " >> Output/Exp2/200/outputMRK$1.$2.txt
python3 ProcessResults.py >> Output/Exp2/200/outputMRK$1.$2.txt

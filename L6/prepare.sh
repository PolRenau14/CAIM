#!/bin/sh

python3 ExtractData.py --index arxiv --minfreq 0.01 --maxfreq 0.05 --numwords 200
python3 GeneratePrototypes.py --nclust 10
python3 ProcessResults.py --prot prototypes.txt

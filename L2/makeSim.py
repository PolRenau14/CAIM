import os
import subprocess
import struct
import numpy as np
import matplotlib.pyplot as plt
import argparse
import random

"""
:Description: MakeSim

    This script make the similarity between texts

:Authors:
    pol
    Victor

:Version:

:Date: 04/10/2019
"""

def getListOfFiles(path):
    lfiles = []
    for lf in os.walk(path):
        if lf[2]:
            for f in lf[2]:
                lfiles.append(lf[0]  + f)
    return lfiles




if __name__ == '__main__':

    parser=argparse.ArgumentParser()
    parser.add_argument('--path',required=True, default=None, help='Path to the files')
    parser.add_argument('--tam',required=False, default=10, help='Number of documents')
    parser.add_argument('--index',required=True, default = None, help= ' el index en el que hem fet index search')
    args = parser.parse_args()

    path = args.path
    tam = int(args.tam)
    index = args.index
    sum = 0
    cont = 0
    lfiles = getListOfFiles(path)

    lfiles = random.choices(lfiles,k = tam)
    for l in lfiles:
        print(l)

    for i in range(len(lfiles)) :
        for j in range(i+1,len(lfiles)):
            command = "python3 TFIDFViewer.py --index "+ index+ " --files " +lfiles[i] +" " +lfiles[j]

            var = subprocess.check_output(command,shell=True)
            varlist = var.split()
            k = varlist[2]
            sum += float(k.decode("utf-8"))
            cont +=1

    print("La puta merda de outut mitjana es ",sum/cont)

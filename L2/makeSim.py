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


def simSameDirectory(path,tam,index):
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
    return sum,cont


def compareDifDirecto(path,path2,tam,index):
    sum = 0
    cont = 0
    lfiles1 = getListOfFiles(path)
    lfiles2 = getListOfFiles(path2)

    lfiles1 = random.choices(lfiles1,k = tam)
    lfiles2 = random.choices(lfiles2,k = tam)
    for l1,l2 in zip(lfiles1,lfiles2):
        l1 = l1.split('/')
        l2 = l2.split('/')
        print( l1[len(l1)-1]+ " Segona llista   " + l2[len(l2)-1])

    for i in range(len(lfiles1)) :
        for j in range(len(lfiles2)):
            command = "python3 TFIDFViewer.py --index "+ index+ " --files " +lfiles1[i] +" " +lfiles2[j]

            var = subprocess.check_output(command,shell=True)
            varlist = var.split()
            k = varlist[2]
            sum += float(k.decode("utf-8"))
            cont +=1
    return sum, cont


if __name__ == '__main__':

    parser=argparse.ArgumentParser()
    parser.add_argument('--path',required=True, default=None, help='Path to the files')
    parser.add_argument('--path2',required=False, default=None, help='Segon path a comparar')
    parser.add_argument('--tam',required=False, default=10, help='Number of documents')
    parser.add_argument('--index',required=True, default = None, help= 'Index-name used to search in to this files')
    args = parser.parse_args()

    path = args.path
    tam = int(args.tam)
    index = args.index
    path2 = args.path2
    sum = 1
    cont = 1
    if (path2 == None):
        sum,cont = simSameDirectory(path,tam,index)
    else:
        sum,cont = compareDifDirecto(path,path2,tam,index)
    print("La puta merda de outut mitjana es ",sum/cont)

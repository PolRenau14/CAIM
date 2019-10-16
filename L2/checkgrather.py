import os
import subprocess
import struct
import numpy as np
import matplotlib.pyplot as plt
import argparse

import plotly.graph_objects as go

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

def getNames(lfiles):
    names = []
    for l in lfiles:
        aux = l.split("/")
        aux = aux[len(aux)-1]
        aux = aux[:-4]
        names.append(aux)
    return names





def makeTable(noms,d):
    headerColor = 'blue'
    rowEvenColor = 'lightgrey'
    rowColor = 'lightgrey'

    aux = []
    aux.append(noms)
    for l in d:
        aux.append(l)

    fig = go.Figure(data=[go.Table(

      header=dict(
        values=['<b>TITOLS</b>']+noms,
        line_color='darkslategray',
        fill_color=headerColor,
        align=['left','center'],
        font=dict(color='white', size=8)
      ),
      cells=dict(
        values= aux,
        line_color='darkslategray',
        # 2-D list of colors for alternating rows
        fill_color = [[headerColor,headerColor,headerColor,headerColor,headerColor], [rowColor,rowColor,rowColor,rowColor,rowColor]*4],
        align = ['left', 'center'],
        font = dict(color = 'darkslategray', size = 8)
        ))
    ])

    fig.show()



if __name__ == '__main__':

    parser=argparse.ArgumentParser()
    parser.add_argument('--path',required=True, default=None, help='Path to the files')
    parser.add_argument('--index',required=True, default = None, help= 'Index-name used to search in to this files')
    args = parser.parse_args()

    path = args.path
    index = args.index
    lfiles = getListOfFiles(path)

    total =  np.zeros((len(lfiles),len(lfiles)))
    for i in range(len(lfiles)) :
        for j in range(i,len(lfiles)):
            command = "python3 TFIDFViewer.py --index "+ index+ " --files " +lfiles[i] +" " +lfiles[j]
            var = subprocess.check_output(command,shell=True)
            varlist = var.split()
            k = varlist[2]
            val = float(k.decode("utf-8"))
            total[i,j] = val


    print("###############################")
    print("printarem tot")
    h = getNames(lfiles)
    makeTable(h,total)

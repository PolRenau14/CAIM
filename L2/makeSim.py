import os
import subprocess
import struct
import numpy as np
import matplotlib.pyplot as plt

"""
:Description: MakeSim

    This script make the similarity between texts

:Authors:
    pol
    Victor

:Version:

:Date: 04/10/2019
"""




if __name__ == '__main__':
    path = "~/FIB/CAIM/Entrada/20_newsgroups/soc.religion.christian/00150"
    sum = 0
    cont = 0
    for i in range(10) :
        s0 = ""
        if ( i < 10):
            s0= "0"
        s0 += str(i)
        for j in range(i+1,11):
            s1 = ""
            if( j < 10):
                s1 = "0"
            s1 += str(j)
            command = "python3 TFIDFViewer.py --index news --files " + path+s0 +" " +path + s1
            var = subprocess.check_output(command,shell=True)
            varlist = var.split()
            k = varlist[2]
            sum += float(k.decode("utf-8"))
            cont +=1
    print("La puta merda de outut mitjana es ",sum/cont)

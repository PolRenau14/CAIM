import os

import numpy as np
import matplotlib.pyplot as plt

"""
:Description: Makebarplot

    This script make the barplot that compare diferent filter and token to the same index.

:Authors:
    pol

:Version:

:Date: 04/10/2019
"""

__author__ ='pol'

def getlastNumber(file):
    with open(file, 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
        l = last_line.split()
        return int(l[0])






if __name__ == '__main__':
    getlastNumber("./Output/CompFilter/snowball.txt")
    path = "./Output"
    lfiles = []
    words = []
    for lf in os.walk(path):
        if lf[2]:
            for f in lf[2]:
                lfiles.append(lf[0] + '/' + f)
                words.append(getlastNumber(lf[0] + '/' + f))

    y_pos = np.arange(4)
    plt.bar(y_pos, words[0:4], align='center', alpha=0.75)
    plt.xticks(y_pos,["letter","standard","classic","whitespace"])
    plt.ylabel("Different words")
    plt.title("Tokens")
    plt.savefig("./Grafics/token.png")
    plt.close()



    y_pos = np.arange(6)
    plt.bar(y_pos, words[4:10],align='center', alpha=0.75)
    plt.xticks(y_pos,["porter_stem","asciifolding","kstem","stop","snowball","lowercase"])
    plt.ylabel("Different words")
    plt.title("Filter")
    plt.savefig("./Grafics/filter.png")
    plt.close()

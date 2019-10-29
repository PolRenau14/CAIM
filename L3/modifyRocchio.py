"""
.. module:: modifyRocchio
modifyRocchio
:Description: modifyRocchio

:Authors: Pol Renau
:Created on: 29/10/2019 08:53

"""

import os
import argparse

def list_To_Str(list):
    str=""
    for l in list:
        str += l +" "
    return str

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #Variables del Rocchio
    parser.add_argument('--index', default=None, help='Index to search')
    parser.add_argument('--nhits', default=10, type=int, help='Number of hits to return')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')
    parser.add_argument('--nrounds', default=1, type=int, help='Number of iterations for applicate Rocchio formula')
    parser.add_argument('-R', default=None, type=int, help='Maximum number of new terms to be kept in the new query')
    parser.add_argument('--alpha', default=None, type=int, help='Alpha parameter for Rocchio rule')
    parser.add_argument('--beta', default=None, type=int, help='Beta parameter for Rocchio rule')
    #VARIABLES afegides
    parser.add_argument('--change',default=None,choices=['alpha','beta','nrounds','nhits','R'], help='Variable to change value')
    parser.add_argument('--increment',default=1,type=int,help='Increment of change variable value.')
    parser.add_argument('--roundsinc',default=3, type=int, help='Number of iterations where inc variable.')


    args = parser.parse_args()

    index = args.index
    query = args.query
    nhits = args.nhits
    nrounds = args.nrounds
    r = args.R
    alpha = args.alpha
    beta = args.beta

    change = args.change
    inc = args.increment
    rinc = args.roundsinc

    comand = ""
    comand = "python3 Rocchio.py --index "+index+ " --nhits " + str(nhits) + " --nrounds " + str(nrounds) + " -R " + str(r) + " --alpha " + str(alpha) + " --beta " + str(beta) + " --query " + list_To_Str(query)
    os.system(comand)
    for i in range(0,rinc):
        if change == "alpha":
            alpha += inc
        elif change == "beta":
            beta += inc
        elif change == "nrounds":
            nrounds += inc
        elif change == "nhits":
            nhits += inc
        elif change == "R":
            r += inc
        print("#####################################")

    comand = ""
    comand = "python3 Rocchio.py --index "+index+ " --nhits " + str(nhits) + " --nrounds " + str(nrounds) + " -R " + str(r) + " --alpha " + str(alpha) + " --beta " + str(beta) + " --query " + list_To_Str(query)
    os.system(comand)

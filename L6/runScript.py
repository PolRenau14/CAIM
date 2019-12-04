import os

__author__='pol'

if __name__ == '__main__':
    index = "arxiv"
    numwords = str(200)
    min = [0.01, 0.1, 0.2 ,0.3,0.5,0.6]
    max = [0.05,0.3, 0.5,0.4,0.7,0.9]
    for i in range(1,7):
        comand = "./exp.sh " + index + " " + str(min[i-1]) + " " + str(max[i-1]) + " " + numwords + " " +str(i)
        os.system(comand)

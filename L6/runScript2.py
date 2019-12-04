import os

__author__='pol'

if __name__ == '__main__':
    os.system("./prepare.sh")
    for i in range(5,7):
        for j in range(5,10):
            comand = "./exp2.sh " + str(i) + " " + str(j)
            os.system(comand)

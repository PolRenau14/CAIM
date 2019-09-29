import pandas as pd
import json
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np


def es_palabra_valida(palabra):
  if palabra.isalpha():
    return True
  else:
    if '-' in palabra:
      partes_palabra = palabra.split('-')
      for parte in partes_palabra:
        if not parte.isalpha():
          return False
      return True

def palabras_validas(archivo):
  frecuencias = []
  rangos = []

  with open('output/{}'.format(archivo), 'r') as archivo:
    i = 1
    for line in archivo.readlines():
      if ',' in line:
        palabra = line.split()
        if es_palabra_valida(palabra[1]):
            frecuencias.append(int(palabra[0].split(',')[0]))
            rangos.append(i)
            i += 1

  return frecuencias,rangos

def func(x,a,b,c):
    a = 1.05
    return c/((x+b)**a)

def make_fitPlot(rangos,frecuencias):
    popt, pcov = curve_fit(func, rangos, frecuencias)
    print(popt)
    plt.plot(rangos,func(rangos,*popt),'r--',linewidth=0.8,label='fit')

def make_plot(ARCHIVO):
    frecuencias,rangos = palabras_validas(ARCHIVO)
    frecuencias.reverse()

    maxI = 10000

# Gráfico

    # Datos Reales
    plt.plot(rangos[0:maxI], frecuencias[0:maxI],'b',label='data')

    # Fitting curve
    make_fitPlot(rangos[0:maxI],frecuencias[0:maxI])

    # Configuramos el plot
    plt.grid(b=True,color="black",linestyle="--")
    plt.legend()
    plt.xlabel("x = Rango de las palabras")
    plt.ylabel("y = Frecuencia de la palabra")


    plt.savefig(ARCHIVO[0:len(ARCHIVO)-3]+"png")
    plt.close()

if __name__ == '__main__':
  make_plot("novels.txt")
 # Aquest conjunt de dades no troba un optim per una a fixada = 1
 # make_plot("arxivs.txt")
 # make_plot("news.txt")

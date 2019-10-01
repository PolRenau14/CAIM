import pandas as pd
import json, os
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

def coger_palabras_validas(archivo):
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
  frecuencias.reverse()
  return frecuencias,rangos

def zipsLaw(x,a,b,c):
    """ Función de la ley de zipf """
    a = 1.05
    return c/((x+b)**a)

def heapsLaw(numeroPalabras, k , beta):
  return k * (numeroPalabras**beta)

def make_fitPlot(rangos, frecuencias, funcion_fit):
    popt, pcov = curve_fit(funcion_fit, rangos, frecuencias)
    plt.plot(rangos,funcion_fit(rangos,*popt),'g--', linewidth = 0.8, label='fit')
    return popt

def make_plot(frecuencias, rangos, funcion_fit = zipsLaw, archivo_a_guardar = ''):
    maxI = 10000

# Gráfico
    # Datos Reales
    plt.plot(rangos[0:maxI], frecuencias[0:maxI], 'b', label='data')

    # Fitting curve
    valuesFound = make_fitPlot(rangos[0:maxI], frecuencias[0:maxI], funcion_fit)

    # Configuramos el plot
    plt.grid(b = True,color = "black",linestyle = "--")
    plt.legend()
    plt.xlabel("x = Rango de las palabras")
    plt.ylabel("y = Frecuencia de la palabra")

    if archivo_a_guardar != '':
      plt.savefig(archivo_a_guardar+".png")
      # Se guardan los valores de las funciones.
      # c,b,alpha para zips. k y beta para heaps
      with open(archivo_a_guardar + 'Values.txt', 'w+') as archivo:
        archivo.write(np.array2string(valuesFound))
      plt.close()
    else:
      plt.show()

if __name__ == '__main__':
  frecuencias, rangos = coger_palabras_validas('novels.txt')
  """make_plot(
    frecuencias = frecuencias,
    rangos = rangos,
  )"""
  path_novel_heaps = 'output/novel_heaps'
  for index in os.listdir(path_novel_heaps):
    frecuencias, rangos = coger_palabras_validas('novel_heaps/' + index)
    make_plot(
      frecuencias = frecuencias,
      rangos = rangos,
      funcion_fit = heapsLaw,
      archivo_a_guardar = 'images/' + index.split('.')[0]
    )

  
 # Aquest conjunt de dades no troba un optim per una a fixada = 1
 # make_plot("arxivs.txt")
 # make_plot("news.txt")

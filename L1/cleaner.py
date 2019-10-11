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

def coger_palabras_validas_Heap(archivo):
        distinct = 0
        total = 0
        with open('output/CountWordsHeaps/{}'.format(archivo), 'r') as archivo:
          for line in archivo.readlines():
            if ',' in line:
              palabra = line.split()
              if es_palabra_valida(palabra[1]):
                  distinct += 1
                  total += int(palabra[0].split(',')[0])
        return distinct,total

def zipsLaw(x,a,b,c):
    """ Función de la ley de zipf """
    a = 1.05
    return c/((x+b)**a)

def heapsLaw(numeroPalabras, k , beta):
  return k * (numeroPalabras**beta)

def make_fitPlot(x, y, funcion_fit,log=0):
    popt, pcov = curve_fit(funcion_fit, x, y)
    word = "fit"
    if (log):
        word = "log-fit"
    plt.plot(x,funcion_fit(x,*popt),'g--', linewidth = 0.8, label=word)
    return popt

def make_plot(frecuencias, rangos, funcion_fit = zipsLaw, archivo_a_guardar = '',log=0):
    maxI = 10000

# Gráfico
    # Datos Reales
    dataName = "data"
    if (log):
        dataName="log-data"
    plt.plot(rangos[0:maxI], frecuencias[0:maxI], 'b', label='data')

    # Fitting curve
    valuesFound = make_fitPlot(rangos[0:maxI], frecuencias[0:maxI], funcion_fit,log)

    # Configuramos el plot
    plt.grid(b = True,color = "black",linestyle = "--")
    plt.legend()
    plt.xlabel("x = Rango de las palabras")
    plt.ylabel("y = Frecuencia de la palabra")
    if(log):
        plt.xlabel("x =Log de Rango de las palabras")
        plt.ylabel("y =Log de Frecuencia de la palabra")
        plt.xscale('log')
        plt.yscale('log')


    if archivo_a_guardar != '':
      plt.savefig(archivo_a_guardar+".png")
      # Se guardan los valores de las funciones.
      # c,b,alpha para zips. k y beta para heaps
      with open(archivo_a_guardar + 'Values.txt', 'w+') as archivo:
        archivo.write(np.array2string(valuesFound))
      plt.close()
    else:
      plt.show()

def make_plot_Heap(y, x, funcion_fit = heapsLaw, archivo_a_guardar = '',log=0):
    # Gráfico
    # Datos Reales
    dataName = "data"
    if(log):
        dataName = "log-data"

    plt.plot(x, y, 'b', label=dataName)

    # Fitting curve
    valuesFound = make_fitPlot(x, y, funcion_fit,log)
    # Configuramos el plot
    plt.grid(b = True,color = "black",linestyle = "--")
    plt.legend()
    plt.xlabel("x = Total palabras")
    plt.ylabel("y = Total palabras distintas")
    if (log):
        plt.xlabel("x = log-total-palabras")
        plt.ylabel("y = log-Total-palabras-distintas")
        plt.xscale('log')
        plt.yscale('log')

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

  path_novel_heaps = 'output/CountWordsHeaps'
  difWords = []
  totWords = []
  for i in range(1,10):
      diferent, total = coger_palabras_validas_Heap("out"+str(i)+".txt")
      totWords.append(total)
      difWords.append(diferent)
  make_plot_Heap(
    y=difWords,
    x=totWords,
    archivo_a_guardar="Heaps-log",
    log = 1
  )
  make_plot_Heap(
      y=difWords,
      x=totWords,
      archivo_a_guardar="Heaps",
      log = 0
    )

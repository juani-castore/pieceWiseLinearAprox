import json
import numpy as np
from FuerzaBruta import *
from BackTracking import *
from ProgramDinam import *
import time
from graficador import graficarAjuste

BIG_NUMBER = 1000000000000000000 # Revisar si es necesario.

def main():

	# Ejemplo para leer una instancia con json
	name = input("ingrese el nombre de la instancia (ejemplo: titanium) : ")
	instance_name = name +".json"
	filename = "../../data/" + instance_name
	with open(filename) as f:
		instance = json.load(f)
	
	K = instance["n"]
	print("ingrese la cantidad de columnas de la grilla: ")
	m = int(input())
	print("ingrese la cantidad de filas de la grilla: ")
	n = int(input())
	print("ingrese la cantidad de segmentos: ")
	N = int(input()) 
	
	# Ejemplo para definir una grilla de m x n.
	grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
	grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)


	# TODO: aca se deberia ejecutar el algoritmo.

	best = {}
	best['sol'] = [None]*(N+1)
	best['obj'] = BIG_NUMBER
	actual = []
	
	print("seleccione el algoritmo a ejecutar: ")
	print("1. Fuerza Bruta")
	print("2. BackTracking")
	print("3. Programacion Dinamica")
	opcion = int(input())
	if opcion == 1:
		tiempoInitiFB = time.time()
		aproxPWL(best, actual, grid_x, grid_y, instance)
		tiempoFinFB= time.time()
	elif opcion == 2:
		tiempoInitiFB = time.time()
		aproxPWL_2(best, actual, grid_x, grid_y, instance)
		tiempoFinFB= time.time()
	elif opcion == 3:
		tiempoInitiFB = time.time()
		ProgramDinam(best,N,grid_x,grid_y,instance)
		tiempoFinFB= time.time()
	else:
		print("opcion invalida")
		return

	print("tiempo en segundos: " + str(abs(tiempoInitiFB-tiempoFinFB)))
	print(best)


	# Formato de solucion para una determinada instancia
		# La solucion es una lista de tuplas (i,j), donde:
		# - i indica el indice del punto de la discretizacion de la abscisa
		# - j indica el indice del punto de la discretizacion de la ordenada.
  
	# Formato de la mejor solucion para una determinada instancia
		# La mejor solucion es un diccionario con dos claves:
		#best['sol'] = [(0, 0), (1, 0), (2, 0), (3, 2), (4, 0), (5, 0)]
		#best['obj'] = 5.927733333333335

	# Represetnamos la solucion con un diccionario que indica:
	# - n: cantidad de breakpoints
	# - x: lista con las coordenadas de la abscisa para cada breakpoint
	# - y: lista con las coordenadas de la ordenada para cada breakpoint
	solution = {}
	solution['n'] = len(best['sol'])
	solution['x'] = [grid_x[x[0]] for x in best['sol']]
	solution['y'] = [grid_y[x[1]] for x in best['sol']]
	solution['obj'] = best['obj'] 	
	
	# Se guarda el archivo en formato JSON
	with open('solution_' + instance_name, 'w') as f:
		json.dump(solution, f)
	

	# Graficamos la solucion junto con los puntos de la instancia y guardamos la imagen en formato PNG
	graficarAjuste(solution, instance, grid_x, grid_y, 'solution_'+ str(m) + "x" + str(n) + "," + str(N) + "N_" + name + '.png')	

	
if __name__ == "__main__":
	main()
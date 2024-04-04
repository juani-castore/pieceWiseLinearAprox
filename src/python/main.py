import json
import numpy as np
from fuerzaBruta import *

BIG_NUMBER = 1e10 # Revisar si es necesario.

def main():

	# Ejemplo para leer una instancia con json
	instance_name = "titanium.json"
	filename = "../../data/" + instance_name
	with open(filename) as f:
		instance = json.load(f)
	
	K = instance["n"] # Cantidad de puntos de la instancia
	m = 6 # tamaño del eje x de la grilla
	n = 6 # tamaño del eje y de la grilla
	N = 5 # Cantidad de breakpoints
	
	# Ejemplo para definir una grilla de m x n.
	grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
	grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)

	print(grid_y)
	print("hola")
	print(len(grid_y))
	print("chau")


	# TODO: aca se deberia ejecutar el algoritmo.

	best = {}
	best['sol'] = [None]*(N+1) # [(none), (none), (none), (none), (none), (none)]
	best['obj'] = BIG_NUMBER  #{error total?} numero muy grande para empezar comparando
	
	print(best['sol'])

	actual = []
	aproxPWL(best, actual, grid_x, grid_y, instance)

	# Posible ejemplo (para la instancia titanium) de formato de solucion, y como exportarlo a JSON.
	# La solucion es una lista de tuplas (i,j), donde:
	# - i indica el indice del punto de la discretizacion de la abscisa
	# - j indica el indice del punto de la discretizacion de la ordenada.
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



if __name__ == "__main__":
	main()
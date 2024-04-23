
# clases

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"
    

# funciones auxiliares

def rectaEnX(x:int, pt1:Punto, pt2:Punto ): #Misma que en FB
    m=(pt2.y-pt1.y)/(pt2.x-pt1.x)
    b = pt1.y - m * pt1.x

    return m*x + b 

def distancia(x:int, y:int , actual:list, grid_x, grid_y, k:int): #Misma que en FB
    for j in range(len(grid_x)-1):
        if(x>=grid_x[actual[j][0]] and x<=grid_x[actual[j+1][0]]):
            distancia = abs(y-rectaEnX(x, Punto(grid_x[actual[j][0]],grid_y[actual[j][1]]), Punto(grid_x[actual[j+1][0]], grid_y[actual[j+1][1]])))
            return distancia

def error(actual, grid_x,grid_y, instance, best): #Modificada a diferencia de FB
    '''Calcula el error de cualquier solucion, ya sea parcial o completa '''
    sum=0
    j=0
    while(j<instance["n"] and instance["x"][j]<=grid_x[ actual[len(actual)-1][0] ]):
        if sum > best: 
            ## Poda por optimalidad: Si el error ya se paso del mejor, dejo de calcular el error porque no es una solucion mejor. 
            return sum
        
        sum=sum+abs(distancia(instance["x"][j], instance["y"][j],actual, grid_x, grid_y, j))
        j=j+1
    return sum

def esFuncion(actual:list, grid_x:int): 
    '''Verifica si las soluciones parciales son posibles soluciones'''
    ## Poda factibilidad: Todas las posibles soluciones deben iniciar en x=0
    ## Poda factibilidad: No puede haber dos puntos con un mismo x. No se cumple la propiedad de inyectividad
    
    if len(actual)>0:
        if actual[0][0]!=0:
            return False
    
    for i in range(len(actual)-1):
        if(actual[i][0] >= actual[i+1][0]):
            return False
    
    return True

def esFactible(actual:list, grid_x:int): #Misma que en FB
    if  actual[0][0] != 0 or actual[len(actual)-1][0] != len(grid_x) - 1:
        return False
    for i in range(len(actual)-1):
        
        if(actual[i][0] >= actual[i+1][0]):
            return False
    return True

#### Algoritmo de Backtracking ####
def aproxPWL_2(best:dict , actual:list, grid_x,grid_y, instance):
    #Caso base
    if len(best['sol']) == len(actual) and esFactible(actual, grid_x):
        e = error(actual, grid_x, grid_y, instance, best["obj"])
        if e < (best['obj']):
            best['obj'] = e
            best['sol']=actual.copy()
            
        return

    #Caso base y Poda por factibilidad: Si la solucion parcial no es factible porque no cumple las propiedades de funcion, no sigue con la recursion
    elif len(best['sol']) == len(actual) or not esFuncion(actual, grid_x):
        return
    
    #Poda por Optimalidad: Si el error de la solucion parcial es mas grande, no sigue con la recursion. Necesariamente tiene que tener 2 breakpoints para trazar una recta
    elif(len(actual)>1 and error(actual, grid_x, grid_y, instance, best["obj"])> best['obj']):
        return 

    else:
        for j in range(len(grid_x)):
            for i in range(len(grid_y)):
                actual.append((j,i))
                aproxPWL_2(best, actual, grid_x, grid_y, instance)
                actual.pop()

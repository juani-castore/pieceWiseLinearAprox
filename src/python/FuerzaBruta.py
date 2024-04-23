
# clases

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"
    

# funciones auxiliares

def rectaEnX(x:int, pt1:Punto, pt2:Punto ):
    '''Dado dos breakpoints, calcula la recta que pasa por ellos y devuelve f(x)'''
    m=(pt2.y-pt1.y)/(pt2.x-pt1.x)
    b = pt1.y - m * pt1.x
    return m*x + b 

def distancia(x:int, y:int , actual:list, grid_x, grid_y, k:int):
    '''Dado un punto observado (x,y) y una lista de breakpoints, calcula la distancia/error entre el punto obs. y la recta que pasa por los breakpoints'''
    for j in range(len(grid_x)-1):
        if(x>=grid_x[actual[j][0]] and x<=grid_x[actual[j+1][0]]):
            distancia = abs(y-rectaEnX(x, Punto(grid_x[actual[j][0]],grid_y[actual[j][1]]), Punto(grid_x[actual[j+1][0]], grid_y[actual[j+1][1]])))
            return distancia

def error(actual, grid_x,grid_y, instance):
    '''Dado una lista de breakpoints, calcula el error TOTAL de la aproximacion PWL -a partir de todos los datos observados-'''
    sum=0
    i=0
    while(i<instance['n']):
        sum=sum+abs(distancia(instance["x"][i], instance["y"][i],actual, grid_x, grid_y, i))
        i=i+1
    return sum

def esFactible(actual:list, grid_x:int):
    '''Dado una lista de breakpoints, verifica  si cumple con las restricciones de:
        1. la funcion debe ser continua e inyectiva
        2. de que el primer y ultimo punto sean 0 y m-1 respectivamente)
    '''
    if actual[0][0] != 0 or actual[len(actual)-1][0] != len(grid_x) - 1:
        return False
    for i in range(len(actual)-1):
        if(actual[i][0] >= actual[i+1][0]):
            return False
    return True

def aproxPWL(best:dict , actual:list, grid_x,grid_y, instance):
    #Hablamos con juanjo y le comentamos que ya nuestro fuerza bruta contiene poda por factibilidad por continuidad
    
    ''''Dado una lista de breakpoints, calcula la mejor aproximacion PWL posible (es decir, menor error) y la guarda en best['sol'] y su error en best['obj']
    Para ello, se recorre todas las combinaciones posibles de breakpoints y se calcula al ser una solucion posible -no parcial-.
    '''
    
    '''Caso Base: Se utilizaron todos los breakpoints
    Si la solucion es factible, se calcula el error. Si es menor que el minimo error encontrado hasta el momento, se actualiza el mejor error y la mejor solucion.'''
    if len(best['sol']) == len(actual) and esFactible(actual, grid_x):
        e = error(actual, grid_x, grid_y, instance)
        if e < (best['obj']):
            best['obj'] = e
            best['sol']=actual.copy()
        return

    elif len(best['sol']) == len(actual):
        return
    
    #Caso Recursivo: Restan por agregar breakpoints. Por lo tanto, se agregan nuevos a la lista actual
    else: 
        for j in range(len(grid_x)):
            for i in range(len(grid_y)):
                actual.append((j,i))
                aproxPWL(best, actual, grid_x, grid_y, instance)
                actual.pop()

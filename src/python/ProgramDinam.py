
# clases

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

# Funciones de Testeo
def rectaentre2puntos(x,pt1,pt2):
    """Calcula la recta entre dos puntos y evalua en x (funcion creada para testear)"""
    m=(pt2.y-pt1.y)/(pt2.x-pt1.x)
    b = pt1.y - m * pt1.x

    return m*x + b

def error_sol(grid_x,grid_y,sol,instance):
    '''Calcula el error dada solucion y unos datos'''
    sum = abs(instance['y'][0] - rectaentre2puntos(instance['x'][0],Punto(grid_x[sol[0][0]], grid_y[sol[0][1]]),Punto(grid_x[sol[1][0]], grid_y[sol[1][1]])))

    for i in range(len(sol)-1):
        for j in range(instance['n']):
            if(instance['x'][j]>grid_x[sol[i][0]] and instance['x'][j]<=grid_x[sol[i+1][0]]):
                sum += abs(instance['y'][j] - rectaentre2puntos(instance['x'][j],Punto(grid_x[sol[i][0]], grid_y[sol[i][1]]),Punto(grid_x[sol[i+1][0]], grid_y[sol[i+1][1]])))
                print(j)
    return sum

# Funciones auxiliares
def rectaEnX(x:int, pt1:Punto, pt2:Punto ):
    """Calcula la recta entre dos puntos y evalua en x"""
    m=(pt2.y-pt1.y)/(pt2.x-pt1.x)
    b = pt1.y - m * pt1.x

    return m*x + b 

def error(n,m,i,j, grid_x,grid_y, instance):
    """Calcula el error de un segmento de la PWL con todos los puntos de la instancia abarcados por dicho segmento"""
    sum=0
    p=0
    if(n==0):
        # esto es porque no incluye el primer punto al calcular los errores
        sum = abs(grid_y[m] - instance['y'][0])
    while(p<instance['n']):
        if(instance['x'][p]>grid_x[n] and instance['x'][p]<=grid_x[i]):
            sum += abs(instance['y'][p] - rectaEnX(instance['x'][p],Punto(grid_x[n], grid_y[m]),Punto(grid_x[i], grid_y[j])))
        p=p+1
    return sum


def ProgramDinamK1(grid_x, grid_y, instance, matriz, matriz_vuelta):
    """Programacion dinamica para el primer segmento de la PWL"""
    # para K=1
    # llenar matriz con valores grandes
    tupla = ()
    for i in range(1,len(grid_x)):
        for j in range(len(grid_y)):
            errorMin = 10000000000000000
            for m in range(len(grid_y)):
                errorAct = error(0,m,i,j, grid_x, grid_y, instance)
                if errorAct < errorMin:
                    errorMin = errorAct
                    tupla = (0,m)
            matriz[i][j] = errorMin    # [1]?
            matriz_vuelta[i][j]=tupla
    return matriz, matriz_vuelta

def ProgramDinamKN(cantSegmentos: int, grid_x, grid_y, instance, matriz_nivel, matriz, matriz_vuelta):
    """Programacion dinamica para N segmentos de la PWL (sin contar el primero)"""
    tupla = ()
    for i in range(1,len(grid_x)):
        for j in range(len(grid_y)):
            errorMin = 10000000000000000
            for n in range(cantSegmentos-1,i):
                for m in range(len(grid_y)):
                    errorAct = error(n,m,i,j, grid_x, grid_y, instance) + matriz[cantSegmentos-2][n][m] # llamamos a la funcion
                    if errorAct < errorMin:
                        errorMin = errorAct
                        tupla = (n,m)
            matriz_nivel[i][j] = errorMin
            matriz_vuelta[i][j] = tupla
    return matriz_nivel, matriz_vuelta

def crearMatrizNivel(grid_y,grid_x):
    '''Crea una matriz de un nivel'''
    listaV_y = [()] * len(grid_y)
    listaE_y = [10000000000000000] * len(grid_y)
    matriz_vueltaNiv = []
    matriz_nivel = []
    for i in range(len(grid_x)):
        # apendeamos las listas de vuelta
        listaV_y = [()] * len(grid_y)
        matriz_vueltaNiv.append(listaV_y)
        # apendeamos las listas de error
        listaE_y = [10000000000000000] * len(grid_y)
        matriz_nivel.append(listaE_y)
    return matriz_vueltaNiv, matriz_nivel
    
def recCamino(matriz, matriz_vuelta, grid_x, grid_y, cantSegmentos):
    """Reconstruye el camino de la solucion"""
    camino = []
    i = 0
    min = 100000000000000000
    minCord = ()
    
    #Existen al menos dos breakpoints/1 segmento
    while (i < len(grid_y)):
        # Accede al ultimo nivel de la matriz y a su ultima columna para recorrer todos los errores minimos de las PWL/ soluciones posibles 
        if(matriz[cantSegmentos-1][len(grid_x)-1][i] < min):
            min = matriz[cantSegmentos-1][len(grid_x)-1][i]
            minCord = matriz_vuelta[cantSegmentos-1][len(grid_x)-1][i]
            minUlti = (len(grid_x)-1,i)
        i = i + 1
    
    camino.insert(0,minUlti) #Se agrega el breapoint con minimo error de la columna final
    camino.insert(0,minCord) #Se agrega el breapoint con minimo error de la anteultima columna
    
    #Si tenes mas de dos breakpoints
    i = cantSegmentos - 2
    while (i >= 0):
        minCord2 = matriz_vuelta[i][minCord[0]][minCord[1]]
        camino.insert(0,minCord2)
        minCord = minCord2
        i = i - 1
    return camino

def getErrorMinimo(matriz):
    """Obtiene el error minimo de la matriz del ultimo nivel"""
    min = 100000000000000000

    for j in range(len(matriz[0][0])):
        if(matriz[len(matriz)-1][len(matriz[0])-1][j] < min):
            min = matriz[len(matriz)-1][len(matriz[0])-1][j]
    return min
    

#### Programacion Dinamica ####
def ProgramDinam(best, cantSegmentos: int, grid_x, grid_y, instance):
    """Programacion dinamica para encontrar la mejor solucion de la PWL"""
    # creamos la matriz de reeconstruccioin y el memo
    matriz_vuelta=[]
    matriz = []

    for j in range(1,cantSegmentos+1):
        matriz_vueltaNiv,matriz_nivel = crearMatrizNivel(grid_y,grid_x)
        if(j==1): # LLama a la funcion del nivel 1
            res = ProgramDinamK1(grid_x, grid_y, instance, matriz_nivel, matriz_vueltaNiv)
        
        else: # LLama a la funcion del nivel N
            res = ProgramDinamKN(j, grid_x, grid_y, instance, matriz_nivel, matriz, matriz_vueltaNiv)
            
        ## apendeamos el nuevo nivel
        matriz.append(res[0])
        matriz_vuelta.append(res[1])
        
    best["sol"]=recCamino(matriz, matriz_vuelta, grid_x, grid_y, cantSegmentos)
    best["obj"] = getErrorMinimo(matriz)

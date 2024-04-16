# clases

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"
    

# funciones auxiliares

def rectaEnX(x:int, pt1:Punto, pt2:Punto ):
    m=(pt2.y-pt1.y)/(pt2.x-pt1.x)
    b = pt1.y - m * pt1.x

    return m*x + b 

def error(n,m,i,j, grid_x,grid_y, instance):
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


def ProgramDinamK1(grid_x, grid_y, instance, matriz):
    # para K=1
    # llenar matriz con valores grandes
    for i in range(1,len(grid_x)):
        for j in range(len(grid_y)):
            errorMin = 10000000000000000
            for m in range(len(grid_y)):
                errorAct = error(0,m,i,j, grid_x, grid_y, instance)  # llamamos a la funcion
                if errorAct < errorMin:
                    errorMin = errorAct
            matriz[1][i][j] = errorMin    # [1]?

def ProgramDinamKN(cantSegmentos: int, grid_x, grid_y, instance, matriz):
    for i in range(1,len(grid_x)):
        for j in range(len(grid_y)):
            errorMin = 10000000000000000
            for n in range(cantSegmentos,i):
                for m in range(len(grid_y)):
                    errorAct = error(n,m,i,j, grid_x, grid_y, instance) + matriz[cantSegmentos-1][n][m] # llamamos a la funcion
                    if errorAct < errorMin:
                        errorMin = errorAct
            matriz[cantSegmentos][i][j] = errorMin 

# factible?
# chequear la matriz

def ProgramDinam(cantSegmentos: int, grid_x, grid_y, instance):
    # con K=0, la matriz no tendria sentido ya que es como si hubieran cero segmentos. Nos parecio mas intuitivo que K= a la cantidad de segmentos directamente.
    lista_y = [-1] * len(grid_y)
    matriz_nivel = [lista_y] * len(grid_x)
    matriz = [matriz_nivel] * (cantSegmentos+1)
    ProgramDinamK1(grid_x, grid_y, instance, matriz)
    for i in range(2,cantSegmentos):
        ProgramDinamKN(i, grid_x, grid_y, instance, matriz)
    ProgramDinamKN(cantSegmentos, grid_x, grid_y, instance, matriz)
    return matriz
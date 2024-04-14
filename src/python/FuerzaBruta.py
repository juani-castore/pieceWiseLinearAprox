
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

def distancia(x:int, y:int , actual:list, grid_x, grid_y, k:int):
    for j in range(len(grid_x)-1):
        if(x>=grid_x[actual[j][0]] and x<=grid_x[actual[j+1][0]]):
            distancia = abs(y-rectaEnX(x, Punto(grid_x[actual[j][0]],grid_y[actual[j][1]]), Punto(grid_x[actual[j+1][0]], grid_y[actual[j+1][1]])))
            return distancia

def error(actual, grid_x,grid_y, instance):
    sum=0
    for i in range(instance["n"]-1):
        sum=sum+abs(distancia(instance["x"][i], instance["y"][i],actual, grid_x, grid_y, i))
    return sum

def esFactible(actual:list, grid_x:int):
    if actual[0][0] != 0 or actual[len(actual)-1][0] != len(grid_x) - 1:
        return False
    for i in range(len(actual)-1):
        # duda: puede haber unalinea vertical? (ahi deberiamos poner >=)
        if(actual[i][0] >= actual[i+1][0]):
            return False
    return True

def aproxPWL(best:dict , actual:list, grid_x,grid_y, instance):
    #print(actual)
    #Hablamos con juanjo y le comentamos que ya nuestro fuerza bruta contiene poda por factibilidad por continuidad
    if len(best['sol']) == len(actual) and esFactible(actual, grid_x):
        e = error(actual, grid_x, grid_y, instance)
        if e < (best['obj']):
            print(actual, e)
            best['obj'] = e
            best['sol']=actual.copy()
            

        return

    elif len(best['sol']) == len(actual):
        return
    
    else:
        for j in range(len(grid_x)):
            for i in range(len(grid_y)):
                actual.append((j,i))
                aproxPWL(best, actual, grid_x, grid_y, instance)
                actual.pop()

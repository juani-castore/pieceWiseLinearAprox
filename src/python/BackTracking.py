
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
        print(actual)
        if(x>=grid_x[actual[j][0]] and x<=grid_x[actual[j+1][0]]):
            distancia = abs(y-rectaEnX(x, Punto(grid_x[actual[j][0]],grid_y[actual[j][1]]), Punto(grid_x[actual[j+1][0]], grid_y[actual[j+1][1]])))
            return distancia

def error(actual, grid_x,grid_y, instance, best):
    sum=0
    j=0
    while(instance["x"][j]<=grid_x[ actual[len(actual)-1][0] ] and j<instance["n"]-1):
        #Decidimos iterar cada punto observado y calcular el error hasta el momento

        if sum > best: 
            ## Poda por optimalidad: error ya se paso del mejor, dejo e calcular el error
            return sum
        
        sum=sum+abs(distancia(instance["x"][j], instance["y"][j],actual, grid_x, grid_y, j))
        j=j+1
    '''
    for i in range(instance["n"]-1):
        if sum > best: ## aca pusimos una poda por optimalidad
            ###### si el error ya se paso del mejor, dejo e calcular el error
            return sum
        sum=sum+abs(distancia(instance["x"][i], instance["y"][i],actual, grid_x, grid_y, i), len(best['sol']))
    '''
    return sum

def esFuncion(actual:list, grid_x:int): 
    ## Poda optimalidad: Todas las posibles soluciones deben iniciar en x=0
    ## Poda optimalidad: No puede haber dos puntos con un mismo x
    
    if len(actual)>0:
        if actual[0][0]!=0:
            return False
    
    for i in range(len(actual)-1):
        if(actual[i][0] >= actual[i+1][0]):
            return False
    
    return True

def esFactible(actual:list, grid_x:int):
    if  actual[0][0] != 0 or actual[len(actual)-1][0] != len(grid_x) - 1:
        return False
    for i in range(len(actual)-1):
        # duda: puede haber unalinea vertical? (ahi deberiamos poner >=)
        if(actual[i][0] >= actual[i+1][0]):
            return False
    return True

def aproxPWL_2(best:dict , actual:list, grid_x,grid_y, instance):
    if len(best['sol']) == len(actual) and esFactible(actual, grid_x):
        e = error(actual, grid_x, grid_y, instance, best["obj"])
        if e < (best['obj']):
            best['obj'] = e
            best['sol']=actual.copy()
            print(actual, e)
        return

    elif len(best['sol']) == len(actual) or not esFuncion(actual, grid_x):
        return
    
    elif(len(actual)>1 and error(actual, grid_x, grid_y, instance, best["obj"])> best['obj']):
        #Necesariamente tiene que tener 2 breakpoints para trazar una recta
        return 

    else:
        print(actual)
        for j in range(len(grid_x)):
            for i in range(len(grid_y)):
                actual.append((j,i))
                aproxPWL_2(best, actual, grid_x, grid_y, instance)
                actual.pop()

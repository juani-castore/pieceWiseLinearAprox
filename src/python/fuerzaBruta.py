
# clases
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


# funciones
'''
def esValida(actual:list, best:dict): #Innecesario. Se fijaba si era continua y llegar al final 
    return (len(actual)==len(best["sol"]))
'''

def rectaEnX(x:int, pt1:Punto, pt2:Punto ):
    m=(pt2.y-pt1.y)/(pt2.x-pt1.x)
    y = pt1.y - m * pt1.x
    return y



# en que celda esta el punto?

def distancia(x:int, y:int , actual:list, grid_x, grid_y, k:int):
    for j in range(len(grid_x)-1):
        if(x>=grid_x[j] and x<=grid_x[j+1]):
            distancia = abs(y-rectaEnX(x, Punto(grid_x[j],grid_y[actual[j]]), Punto(grid_x[j+1], grid_y[actual[j+1]])))
            return distancia
        

def error(actual, grid_x,grid_y, instance):
    sum=0
    for i in range(instance["n"]-1):
        print(instance["x"][i])
        print(instance["y"][i])
        sum=sum+distancia(instance["x"][i], instance["y"][i],actual, grid_x, grid_y, i)

def aproxPWL(best:dict , actual:list, grid_x,grid_y, instance): #instance:datos obs
    print(actual)
    # len(actual)==len(best["sol"]) and
    if len(actual)==len(best["sol"]) and error(actual,grid_x,grid_y, instance) < best["obj"]:
        best["sol"]=actual
        best["obj"]=error(actual, grid_x,grid_y, instance)
        return
    
    elif len(actual)==len(best["sol"]):
        return

    else:
        print("...................................................")
        for i in range(len(grid_y)):
            #nueva = list(actual)
            actual.append(i)
            aproxPWL(best, actual, grid_x,grid_y, instance)
            actual.pop()




    

        

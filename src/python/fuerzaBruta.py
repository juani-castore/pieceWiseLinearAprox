
# clases
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


# funciones
def esValida(actual:list, best:dict): #Innecesario. Se fijaba si era continua y llegar al final 
    return (len(actual)==len(best["sol"]))

def rectaEnX(x:int, pt1:Punto, pt2:Punto ):
    m=(pt2.y-pt1.y)/(pt2.x-pt1.x)
    y = pt1.y - m * pt1.x
    return y


def distancia(x:int, y:int , actual:list, grid_x, grid_y):
    for i in range(len(actual)):
        if actual[i][0]>=x:
            return abs(y-rectaEnX(x, Punto(grid_x[i],grid_y[actual[i]]), Punto(grid_x[i], grid_y[actual[i]]))) # aca le pasamos el valor de x_obs y 

def error(actual, grid_x,grid_y, instance):
    sum=0
    for i in range(instance["n"]-1):
        sum+=distancia(instance["x"][i], instance["y"][i],actual, grid_x, grid_y)
    return sum

def aproxPWL(best:dict , actual:list, grid_x,grid_y, instance): #instance:datos obs
    if esValida(actual, best) and error(actual) < best["obj"]:
        best["sol"]=actual
        best["obj"]=error(actual, grid_x,grid_y, instance)
    
    else:
        for i in range(len(grid_y)):
            nueva= actual.append(i)
            aproxPWL(best, nueva, grid_x,grid_y, instance)




    

        

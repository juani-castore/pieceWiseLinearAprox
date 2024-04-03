
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

'''
def distancia(x:int, y:int , actual:list, grid_x, grid_y):
    
    
    
    for i in range(len(actual)-1):
        if i>=x:
            return abs(y-rectaEnX(x, Punto(grid_x[i],grid_y[actual[i]]), Punto(grid_x[i+1], grid_y[actual[i+1]]))) # aca le pasamos el valor de x_obs y 
'''

def error(actual, grid_x,grid_y, instance):
    sum=0
    for j in range(len(actual)-1):
        for i in range(instance["n"]-1):
            
            while( instance["x"][i] >= grid_x[j] and instance["x"][i] < grid_x[j+1]):
                sum=sum+distancia(instance["x"][i], instance["y"][i],actual, grid_x, grid_y)

    return sum

def aproxPWL(best:dict , actual:list, grid_x,grid_y, instance): #instance:datos obs
    print(actual)
    # len(actual)==len(best["sol"]) and
    if len(actual)==len(best["sol"]) and error(actual,grid_x,grid_y, instance) < best["obj"]:
        best["sol"]=actual
        best["obj"]=error(actual, grid_x,grid_y, instance)
    
    else:
        print("...................................................")
        for i in range(len(grid_y)):
            actual.append(i)
            nueva=actual
            aproxPWL(best, nueva, grid_x,grid_y, instance)




    

        

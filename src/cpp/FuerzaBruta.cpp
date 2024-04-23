#include "FuerzaBruta.h"
#include <iostream>
#include <vector>
#include <map>
#include <unordered_map>
#include <string>


using namespace std;

float maximo(vector<float> x) {
    //Calcula el maximo valor de x de la instancia
    float max = x[0];
    for (int i = 1; i < x.size(); i++) {
        if (x[i] > max) {
            max = x[i];
        }
    }
    return max;
}

float minimo(vector<float> x) {
    //Calcula el minimo valor de x de la instancia
    float min = x[0];
    for (int i = 1; i < x.size(); i++) {
        if (x[i] < min) {
            min = x[i];
        }
    }
    return min;
}

float rectaEnX(float x, float x1, float y1, float x2, float y2) {
    //Dado dos breakpoints (x1,y1) y (x2,y2), calcula la recta que pasa por ellos y devuelve f(x)
    float m = (y2 - y1) / (x2 - x1);
    float b = y1 - m * x1;
    return m * x + b;
}
    
Grilla::Grilla(int m, int n, float xi, float xf, float yi, float yf) {
    //Crea una grilla desde el minimo punto observado (xi,yi) hasta el maximo punto observado (xf,yf) con m columnas y n filas
    for (int i = 0; i < m; i++) {
        x.push_back(xi + i * ((xf - xi) / (m-1)));
    }
    for (int i = 0; i < n; i++) {
        y.push_back(yi + i * ((yf - yi) / (n-1)));
    }
}

SolPosible::SolPosible() {
    //Se inicializa una solucion posible con error infinito para asegurarnos que cualquier solucion sea mejor.
    // El vector de puntos esta vacio y almacenara los breakpoints de la solucion.
    this->error = 1000000000;
    this->sol = vector<Punto>();
}

Best::Best(SolPosible sol) {
    //Se inicializa la mejor solucion con error infinito para asegurarnos que cualquier solucion sea mejor.
    sol.error = 1000000000;
    this->best = sol;
}

void SolPosible::calcularError(vector<float> x, vector<float> y, Grilla& grilla) {
    //Calcula el error de la solucion posible con respecto a los puntos observados
    //vector<float> x: puntos observados en x
    //vector<float> y: puntos observados en y
    //Grilla& grilla: los valores discretizados segun la instancia

    float error = abs(y[0] - grilla.y[this->sol[0].y]); //comenzamos calculando el error del primer dato observado porque el for no lo toma en cuenta
    for (int i = 0; i < this->sol.size()-1; i++)
    {
        for (int j = 0; j < x.size(); j++)
        {
            // si el punto_obs esta en el segmento (es decir, entre los dos breakpoints), calculamos el error
            // si no, continuamos con el siguiente punto_obs
            if (x[j]>grilla.x[this->sol[i].x] && x[j]<=grilla.x[this->sol[i+1].x])
            {                
                error += abs(y[j] - rectaEnX(x[j],grilla.x[this->sol[i].x],grilla.y[this->sol[i].y],grilla.x[this->sol[i+1].x],grilla.y[this->sol[i+1].y]));
            }
            
        }
        
    }
    //Actualizamos el error de la solucion posible -no parcial-
    this->error = error;
}  

void SolPosible::agregarPunto(Punto p) {
    this->sol.push_back(p);
}
void SolPosible::eliminarPunto(int i) {
    this->sol.erase(this->sol.begin() + i);
}
    
bool SolPosible::esFactible(Grilla& grilla, int k) {
    bool res = true;
    //Dado una lista de breakpoints, verifica  si cumple con las restricciones de:
    //    1. la funcion debe ser continua e inyectiva
    //    2. de que el primer y ultimo punto sean 0 y m-1 respectivamente)

    if (this->sol[0].x != 0 || this->sol[this->sol.size()-1].x != grilla.x.size() - 1) {
        res = false;
    }
    for (int i = 0; i < this->sol.size()-1; i++) {
        if (this->sol[i].x >= this->sol[i+1].x) {
            res = false;
        }
    }
    return res;   
}

void aproxPWL(Best& best, SolPosible actual, vector<float> x_obs, vector<float> y_obs, Grilla& grilla, int k) {
    //K segmentos. K+1 Breakpoints
        //Dado una lista de breakpoints, calcula la mejor aproximacion PWL posible (es decir, menor error) y la guarda en best['sol'] y su error en best['obj']
        //Para ello, se recorre todas las combinaciones posibles de breakpoints y se calcula al ser una solucion posible -no parcial-.
    
    
    //Caso Base: Se utilizaron todos los breakpoints
    //Si la solucion es factible, se calcula el error. Si es menor que el minimo error encontrado hasta el momento, se actualiza el mejor error y la mejor solucion.
    if(actual.sol.size()==k+1 && actual.esFactible(grilla, k+1)){
        actual.calcularError(x_obs, y_obs, grilla);
        if(actual.error<best.best.error){
            best.best=actual;
            best.best.error=actual.error;
        }
    }
    else if(actual.sol.size()==k+1){
    }
    //Caso Recursivo: Se agregan nuevos breakpoints
    else{
        for (int i = 0; i < grilla.x.size(); i++){
            for (int j = 0; j < grilla.y.size(); j++){
                SolPosible actualNueva = SolPosible();
                actualNueva.sol = actual.sol;
                actualNueva.agregarPunto(Punto(i,j));
                aproxPWL(best, actualNueva, x_obs, y_obs, grilla, k);
            }
        }
    }   
}


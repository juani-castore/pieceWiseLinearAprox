#include "FuerzaBruta.h"
#include <iostream>
#include <vector>
#include <string>


using namespace std;

bool SolPosible::vaSerFactible(){ // si la solucion parcial es factible
    bool res = true;
    if (this->sol.size() <= 1)
    {  // si esta vacia o tiene un solo pto (0, algo) entonces puede ser factible
        if (this->sol.size() == 1 && this->sol[0].x != 0)
        {
            // si tiene un solo pto y no esta en x=0
            res = false;
        }  
    }
    else{
        for (int i = 0; i < this->sol.size() - 1; i++)
        {
            if (this->sol[i].x >= this->sol[i+1].x)
            {
                // si el pto ant es >= que el pto sig
                res = false;
            }
        }
    }
    return res;
}
    

float calcularErrorBT(vector<float> x, vector<float> y, Grilla& grilla, Best& best, SolPosible& actual) {
    // Adecuamos la funcion de FB para  poder calcular el error en solucion parciales y tambien completas
    float error = abs(y[0] - grilla.y[actual.sol[0].y]);
    for (int i = 0; i < actual.sol.size()-1; i++)
    {
        for (int j = 0; j < x.size(); j++)
        {
            if (x[j]>grilla.x[actual.sol[i].x] && x[j]<=grilla.x[actual.sol[i+1].x])
            {
                // si el punto_obs esta dentro del segmento
                error += abs(y[j] - rectaEnX(x[j],grilla.x[actual.sol[i].x],grilla.y[actual.sol[i].y],grilla.x[actual.sol[i+1].x],grilla.y[actual.sol[i+1].y]));
                if (error > best.best.error)
                {
                    // poda por optimalidad 1
                    return error; // si el error ya se paso, deja de calcularlo
                }              
            }
            
        }
        
    }
    actual.error = error;
    return error;
}  


void aproxPWL_BT(Best& best, SolPosible actual, vector<float> x_obs, vector<float> y_obs, Grilla& grilla, int k) {
    //K segmentos. K+1 Breakpoints
    //Caso Base
    if(actual.sol.size()==k+1 && actual.esFactible(grilla, k+1)){
        actual.calcularError(x_obs, y_obs, grilla);
        if(actual.error<best.best.error){
            best.best=actual;
            best.best.error=actual.error;
        }
    }
    //Cortamos la recursion cuando: ya usamos los breakpoints disponibles, o si el error actual es mayor al mejor error encontrado hasta ahora (poda optimalidad)
    else if(actual.sol.size()==k+1 || ( best.best.error < 1000000000 && actual.sol.size() >= 2 && (calcularErrorBT(x_obs, y_obs, grilla, best, actual) > best.best.error))){}
    else if (!actual.vaSerFactible()){} // poda de factibilidad
    else{
        for (int i = 0; i < grilla.x.size(); i++){
            for (int j = 0; j < grilla.y.size(); j++){
                SolPosible actualNueva = SolPosible();
                actualNueva.sol = actual.sol;
                actualNueva.agregarPunto(Punto(i,j));
                aproxPWL_BT(best, actualNueva, x_obs, y_obs, grilla, k);
            }
        }
    }   
}


#include "FuerzaBruta.h"
#include <iostream>
#include <vector>
#include <map>
#include <unordered_map>
#include <string>


using namespace std;

float maximo(vector<float> x) {
    float max = x[0];
    for (int i = 1; i < x.size(); i++) {
        if (x[i] > max) {
            max = x[i];
        }
    }
    return max;
}

float minimo(vector<float> x) {
    float min = x[0];
    for (int i = 1; i < x.size(); i++) {
        if (x[i] < min) {
            min = x[i];
        }
    }
    return min;
}

float rectaEnX(float x, float x1, float y1, float x2, float y2) {
    float m = (y2 - y1) / (x2 - x1);
    float b = y1 - m * x1;
    return m * x + b;
}
    



Grilla::Grilla(int m, int n, float xi, float xf, float yi, float yf) {
    for (int i = 0; i < m; i++) {
        x.push_back(xi + i * ((xf - xi) / (m-1)));
    }
    for (int i = 0; i < n; i++) {
        y.push_back(yi + i * ((yf - yi) / (n-1)));
    }
}

SolPosible::SolPosible() {
    this->error = 1000000000;
    this->sol = vector<Punto>();
}

Best::Best(SolPosible sol) {
    sol.error = 1000000000;
    this->best = sol;
}

void SolPosible::calcularError(vector<float> x, vector<float> y, Grilla& grilla) {
    float error = abs(y[0] - grilla.y[this->sol[0].y]); //comenzamos calculando el e[0] porque el for no lo toma en cuenta
    for (int i = 0; i < this->sol.size()-1; i++)
    {
        for (int j = 0; j < x.size(); j++)
        {
            if (x[j]>grilla.x[this->sol[i].x] && x[j]<=grilla.x[this->sol[i+1].x])
            {
                // si el punto_obs esta dentro del segmento
                error += abs(y[j] - rectaEnX(x[j],grilla.x[this->sol[i].x],grilla.y[this->sol[i].y],grilla.x[this->sol[i+1].x],grilla.y[this->sol[i+1].y]));
            }
            
        }
        
    }
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
    if(actual.sol.size()==k+1 && actual.esFactible(grilla, k+1)){
        actual.calcularError(x_obs, y_obs, grilla);
        if(actual.error<best.best.error){
            best.best=actual;
            best.best.error=actual.error;
        }
    }
    else if(actual.sol.size()==k+1){
    }
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


#ifndef __FuerzaBruta_H__
#define __FuerzaBruta_H__

#include <set>
#include <string>
#include <map>
#include <vector>
#include <unordered_map>
#include <utility>
//using namespace std;


class Punto {
public:
    int x;
    int y;
    Punto(int x, int y) : x(x), y(y) {}
    Punto() {}
};

class Grilla {
public:
    std::vector<float> x; //Discretizacion
    std::vector<float> y;
    Grilla(int m, int n, float xi, float xf, float yi, float yf);
};

class SolPosible {
public:
    std::vector<Punto> sol;
    float error;
    //int tamanio;


    SolPosible();
    void calcularError(std::vector<float> x, std::vector<float> y, Grilla& grilla);
    void agregarPunto(Punto p);
    void eliminarPunto(int i);
    bool esFactible(Grilla& grilla, int k);
    bool vaSerFactible();
};

class Best {
public:
    SolPosible best;
    //float error;
    Best(SolPosible sol);
};


void aproxPWL(Best& best, SolPosible actual, std::vector<float> x_obs, std::vector<float> y_obs, Grilla& grilla, int k);
void aproxPWL_BT(Best& best, SolPosible actual, std::vector<float> x_obs, std::vector<float> y_obs, Grilla& grilla, int k);
float rectaEnX(float x, float x1, float y1, float x2, float y2);
float maximo(std::vector<float> x);
float minimo(std::vector<float> x);
float calcularErrorBT(std::vector<float> x, std::vector<float> y, Grilla& grilla, Best& best, SolPosible& actual);

#endif // __FuerzaBruta_H__
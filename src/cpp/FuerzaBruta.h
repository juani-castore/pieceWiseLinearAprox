#ifndef __FuerzaBruta_H__
#define __FuerzaBruta_H__

#include <set>
#include <string>
#include <map>
#include <vector>
#include <unordered_map>
#include <utility>
#include <tuple>
using namespace std;


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
    Best(SolPosible sol);
};


void aproxPWL(Best& best, SolPosible actual, std::vector<float> x_obs, std::vector<float> y_obs, Grilla& grilla, int k);
void aproxPWL_BT(Best& best, SolPosible actual, std::vector<float> x_obs, std::vector<float> y_obs, Grilla& grilla, int k);
float rectaEnX(float x, float x1, float y1, float x2, float y2);
float maximo(std::vector<float> x);
float minimo(std::vector<float> x);
float calcularErrorBT(std::vector<float> x, std::vector<float> y, Grilla& grilla, Best& best, SolPosible& actual);
vector<vector<float>> matrizNivelErrores(vector<float> grid_x, vector<float> grid_y);
vector<vector<tuple<int,int>>> matrizNivelVuelta(vector<float> grid_x, vector<float> grid_y);
void programDinam(Best& best,int cantidadSegmentos, vector<float> grid_x, vector<float> grid_y, vector<float> xObs, vector<float> yObs);
void programDinamKN (int cantidadSegmentos, vector<float> grid_x, vector<float> grid_y, vector<float> xObs, vector<float> yObs, vector<vector<vector<float>>> & matriz, vector<vector<vector<tuple<int,int>>>> & matrizVuelta);
void programDinamK1 (vector<float> grid_x, vector<float> grid_y, vector<float> xObs, vector<float> yObs, vector<vector<vector<float>>> & matriz, vector<vector<vector<tuple<int,int>>>> & matrizVuelta);
float error_pd(int n, int m, int i, int j, vector<float> grid_x, vector<float> grid_y, vector<float> xObs, vector<float> yObs);
vector<tuple<int,int>> recCamino(vector<vector<vector<float>>> & matriz, vector<vector<vector<tuple<int,int>>>> & matriz_vuelta, vector<float> grid_x, vector<float> grid_y, int cantidadSegmentos);

#endif // __FuerzaBruta_H__
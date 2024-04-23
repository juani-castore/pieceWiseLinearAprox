#include "FuerzaBruta.h"
#include <iostream>
#include <vector>
#include <tuple>

using namespace std;

vector<vector<float>> matrizNivelErrores(vector<float> grid_x, vector<float> grid_y){
    vector<vector<float>> matrizNivel {};
    for (int i=0; i < grid_x.size(); i=i+1){
        vector<float> lista_y (grid_y.size(), 10000000);
        matrizNivel.push_back(lista_y);
    }
    return matrizNivel;
}

vector<vector<tuple<int,int>>> matrizNivelVuelta(vector<float> grid_x, vector<float> grid_y){
    vector<vector<tuple<int,int>>> matrizNivel {};
    for (int i=0; i < grid_x.size(); i=i+1){
        tuple<int,int> tupla(0,0);
        vector<tuple<int,int>> lista_y (grid_y.size(), tupla);
        matrizNivel.push_back(lista_y);
    }
    return matrizNivel;
}

/* float rectaEnX(float x, float x1, float y1, float x2, float y2) {
    //Dado dos breakpoints (x1,y1) y (x2,y2), calcula la recta que pasa por ellos y devuelve f(x)
    float m = (y2 - y1) / (x2 - x1);
    float b = y1 - m * x1;
    return m * x + b;
} */

float error_pd(int n, int m, int i, int j, vector<float> grid_x, vector<float> grid_y, vector<float> xObs, vector<float> yObs){
    float error;
    if(n == 0){
        error = abs(yObs[0] - grid_y[m]);
    } else{
        error = 0;
    }
    //el priumero arrancarlo desde antes
    int z = 0;
    while(z < xObs.size()){
        if(xObs[z] > grid_x[n] && xObs[z] <= grid_x[i]){
            float errorAct = abs(yObs[z] - rectaEnX(xObs[z], grid_x[n], grid_y[m], grid_x[i], grid_y[j]));
            error = error + errorAct;
        }
        z = z + 1;
    }
    return error;

}

void programDinamK1 (vector<float> grid_x, vector<float> grid_y, vector<float> xObs, vector<float> yObs, vector<vector<vector<float>>> & matriz, vector<vector<vector<tuple<int,int>>>> & matrizVuelta){
    for(int i = 1; i < grid_x.size(); i = i + 1){
        for(int j = 0; j < grid_y.size(); j = j + 1){
            float errorMin = 1000000000;
            tuple<int,int> tupla;
            for(int m = 0; m < grid_y.size(); m = m + 1){
                float errorAct = error_pd(0, m, i, j, grid_x, grid_y, xObs, yObs);
                if(errorAct < errorMin){
                    errorMin = errorAct;
                    tupla = make_tuple(0,m);
                }
            }
            matriz[0][i][j] = errorMin;
            //cout << "Error en la matriz: " << matriz[0][i][j] << endl;
            matrizVuelta[0][i][j] = tupla;
        }
    }
}

void programDinamKN (int cantidadSegmentos, vector<float> grid_x, vector<float> grid_y, vector<float> xObs, vector<float> yObs, vector<vector<vector<float>>> & matriz, vector<vector<vector<tuple<int,int>>>> & matrizVuelta){
    for(int i = 1; i < grid_x.size(); i = i + 1){
        for(int j = 0; j < grid_y.size(); j = j + 1){
            float errorMin = 1000000000;
            tuple<int,int> tupla;
            for(int n = cantidadSegmentos-1; n < i; n = n + 1){
                for(int m = 0; m < grid_y.size(); m = m + 1){
                    float errorAct = error_pd(n, m, i, j, grid_x, grid_y, xObs, yObs) + matriz[cantidadSegmentos - 2][n][m];
                    //cout << errorAct << " ";
                    if(errorAct < errorMin){
                        //cout << "entro" << endl;
                        errorMin = errorAct;
                        tupla = make_tuple(n,m);
                    }
                }
            }
            matriz[cantidadSegmentos-1][i][j] = errorMin;
            matrizVuelta[cantidadSegmentos-1][i][j] = tupla;
        }
    }
}

vector<tuple<int,int>> recCamino(vector<vector<vector<float>>> & matriz, vector<vector<vector<tuple<int,int>>>> & matriz_vuelta, vector<float> grid_x, vector<float> grid_y, int cantidadSegmentos){
    vector<tuple<int,int>> camino = {};
    int i = 0;
    int min = 100000000;
    tuple<int,int> minCord;
    tuple<int,int> minUlti;
    while(i< grid_y.size()){
        if(matriz[cantidadSegmentos-1][grid_x.size()-1][i] < min){
            min = matriz[cantidadSegmentos-1][grid_x.size()-1][i];
            minCord = matriz_vuelta [cantidadSegmentos-1][grid_x.size()-1][i];
            minUlti = make_tuple(grid_x.size()-1, i);
            //tuple<int,int> minUlti (grid_x.size()-1, i);
        }
        i = i + 1;
    }
    camino.insert(camino.begin(), minUlti);
    camino.insert(camino.begin(), minCord);
    i = cantidadSegmentos - 2;
    while( i >= 0){
        tuple<int,int> minCord2 = matriz_vuelta[i][get<0>(minCord)][get<1>(minCord)];
        camino.insert(camino.begin(), minCord2);
        minCord = minCord2;
        i--;
    }
    return camino;
}

void programDinam(Best& best,int cantidadSegmentos, vector<float> grid_x, vector<float> grid_y, vector<float> xObs, vector<float> yObs){
    vector<vector<vector<float>>> matriz = {};
    vector<vector<vector<tuple<int,int>>>> matrizVuelta = {};
    for (int i=0; i < cantidadSegmentos; i=i+1){
        vector<vector<float>> matrizNivel = matrizNivelErrores(grid_x, grid_y);
        vector<vector<tuple<int,int>>> matrizNivelVuelt = matrizNivelVuelta(grid_x, grid_y);
        matriz.push_back(matrizNivel);
        matrizVuelta.push_back(matrizNivelVuelt);
    }

    programDinamK1(grid_x, grid_y, xObs, yObs, matriz, matrizVuelta);
    for(int j = 2; j < cantidadSegmentos + 1; j = j + 1){
        programDinamKN(j, grid_x, grid_y, xObs, yObs, matriz, matrizVuelta);
    }
    float errorMin = 1000000;

    for(int j = 0; j < grid_y.size(); j = j + 1){
        if(matriz[cantidadSegmentos-1][grid_x.size()-1][j] < errorMin){
            errorMin = matriz[cantidadSegmentos-1][grid_x.size()-1][j];
        }
    }
    // guardar el error minimo
    best.best.error = errorMin;
    // guardar el camino
    vector<tuple<int,int>> camino = recCamino(matriz, matrizVuelta, grid_x, grid_y, cantidadSegmentos);
    for(int i = 0; i < camino.size(); i = i + 1){
        best.best.sol.push_back(Punto(get<0>(camino[i]), get<1>(camino[i])));
    }
}


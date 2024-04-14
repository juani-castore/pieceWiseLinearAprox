#include <string>
#include <iostream>
#include <fstream>
#include <chrono>
#include "include/json.hpp"
#include "FuerzaBruta.h"
//#include "FuerzaBruta.cpp"

// Para libreria de JSON.
using namespace nlohmann;
using namespace std;

int main(int argc, char** argv) {
    std::string instance_name = "titanium.json";
    std::cout << "Reading file " << instance_name << std::endl;
    std::ifstream input("../../data/" + instance_name);

    json instance;
    input >> instance;
    input.close();

    int K = instance["n"];
    int m = 4;
    int n = 4;
    int N = 3;

    SolPosible sol=SolPosible();
    Best b= Best(sol);
    Grilla grilla= Grilla(m,n,instance["x"][0],instance["x"][K-1], minimo(instance["y"]),maximo(instance["y"]));
    
    // medimos el tiempo antes y despues
    auto start = std::chrono::high_resolution_clock::now();

    //fuerza bruta
    //aproxPWL(b, sol, instance["x"], instance["y"], grilla, N);
    //backtracking
    aproxPWL_BT(b, sol, instance["x"], instance["y"], grilla, N);

    auto fin = std::chrono::high_resolution_clock::now();

    // imprimimos el tiempo
    std::chrono::duration<double> elapsed = fin - start;
    cout << "Tiempo: " << elapsed.count() << " segundos" << endl;
    

    // imprimimos la solucion
    cout << "Best solution: " << endl
            << "Error: " << b.best.error << endl
            << "Size: " << b.best.sol.size() << endl;
    for (int i = 0; i < b.best.sol.size(); i++) {
        cout << "Punto " << i << ": (" << b.best.sol[i].x << ", " << b.best.sol[i].y << ")" << endl;
    }


    // creamos un vector para los y y uno para los x
    // y guardamos los valores de los puntos de la solucion en ellos.
    vector<float> x;
    vector<float> y;
    for (int i = 0; i < b.best.sol.size(); i++) {
        x.push_back(grilla.x[b.best.sol[i].x]);
        y.push_back(grilla.y[b.best.sol[i].y]);
    }

    // Creamos un JSON con los resultados.
    instance["n"] = b.best.sol.size();
    instance["x"] = x;
    instance["y"] = y;
    instance["obj"] = b.best.error;

    // Guardamos el JSON en un archivo.
    std::ofstream output("solution_" + instance_name);

    output << instance;
    output.close();

    return 0;
}
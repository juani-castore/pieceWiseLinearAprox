#include <string>
#include <iostream>
#include <fstream>
#include "include/json.hpp"
#include "FuerzaBruta.h"
//#include "FuerzaBruta.cpp"

// Para libreria de JSON.
using namespace nlohmann;
using namespace std;

int main(int argc, char** argv) {
    std::string instance_name = "../../data/titanium.json";
    std::cout << "Reading file " << instance_name << std::endl;
    std::ifstream input(instance_name);

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
    
    //aproxPWL(b, sol, instance["x"], instance["y"], grilla, N);
    aproxPWL_BT(b, sol, instance["x"], instance["y"], grilla, N);

    cout << "Best solution: " << endl
            << "Error: " << b.best.error << endl
            << "Size: " << b.best.sol.size() << endl;
    for (int i = 0; i < b.best.sol.size(); i++) {
        cout << "Punto " << i << ": (" << b.best.sol[i].x << ", " << b.best.sol[i].y << ")" << endl;
    }


    // Ejemplo para guardar json.
    // Probamos guardando el mismo JSON de instance, pero en otro archivo.
    std::ofstream output("test_output.out");

    output << instance;
    output.close();

    return 0;
}
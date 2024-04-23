#include <string>
#include <iostream>
#include <fstream>
#include <chrono>
#include "include/json.hpp"
#include "FuerzaBruta.h"



// Para libreria de JSON.
using namespace nlohmann;
using namespace std;

int main(int argc, char** argv) {
    // Leemos el archivo de la instancia.
    std::string instance_name;
    cout << "ingrese el nombre de la instancia" << endl;
    cout << "Ejemplo: aspen_simulation" << endl;
    cout << "Si esta no se encuentra en la carpeta data, por favor agreguela o se cortara el programa" << endl;
    getline(cin, instance_name);
    
    std::cout << "Reading file " << instance_name << ".json" << std::endl;
    std::ifstream input("../../data/" + instance_name + ".json");

    json instance;
    input >> instance;
    input.close();

    // Obtenemos los parametros de la instancia.
    int K = instance["n"];
    int m;
    int n;
    int N;
    cout << "ingrese la cantidad de columnas: " << endl;
    cin >> m;
    cout << "ingrese la cantidad de filas: " << endl;
    cin >> n;
    cout << "ingrese la cantidad de segmentos: " << endl;
    cin >> N;

    cout << "ingrese el algoritmo a utilizar: " << endl;
    cout << "1: Fuerza Bruta" << endl;
    cout << "2: Backtracking" << endl;
    cout << "3: Programacion Dinamica" << endl;
    int algoritmo;
    cin >> algoritmo;



    SolPosible sol=SolPosible();
    Best b= Best(sol);
    Grilla grilla= Grilla(m,n,instance["x"][0],instance["x"][K-1], minimo(instance["y"]),maximo(instance["y"]));
    auto start = std::chrono::high_resolution_clock::now();
    auto fin = std::chrono::high_resolution_clock::now();
    // aca se elige el algoritmo y se mide el tiempo de ejecucion
    if(algoritmo == 1){
        start = std::chrono::high_resolution_clock::now();
        aproxPWL(b, sol, instance["x"], instance["y"], grilla, N);
        fin = std::chrono::high_resolution_clock::now();
    } else if(algoritmo == 2){
        start = std::chrono::high_resolution_clock::now();
        aproxPWL_BT(b, sol, instance["x"], instance["y"], grilla, N);
        fin = std::chrono::high_resolution_clock::now();
    } else if(algoritmo == 3){
        start = std::chrono::high_resolution_clock::now();
        programDinam(b,N,grilla.x,grilla.y,instance["x"],instance["y"]);
        fin = std::chrono::high_resolution_clock::now();
    } else{
        cout << "Algoritmo no valido" << endl;
        return 0;
    }

    cout << "Best solution: " << endl
            << "Error: " << b.best.error << endl
            << "Size: " << b.best.sol.size() << endl;

    // imprimimo el camino
    cout << "Camino: ";
    for (int i = 0; i < b.best.sol.size(); i++) {
        cout << "(" << b.best.sol[i].x << ", " << b.best.sol[i].y << ") ";
    }
    cout << endl;
    

    // imprimimos el tiempo
    std::chrono::duration<double> elapsed = fin - start;
    cout << "Tiempo: " << elapsed.count() << " segundos" << endl;

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
    std::ofstream output("solution_" + instance_name + ".json");

    output << instance;
    output.close();

    return 0;
}
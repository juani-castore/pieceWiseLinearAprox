from matplotlib import pyplot as plt


def graficarAjuste(solution,instance, grid_x, grid_y, filename):
    # Graficamos los puntos de instance y la solucion
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.xticks(grid_x)
    plt.yticks(grid_y)
    # grafica los puntos en negro
    plt.plot(instance['x'], instance['y'], 'ko')
    plt.plot(solution['x'], solution['y'], 'g')
    plt.draw()
    # me guardo el grafico en formato png
    plt.savefig(filename)
    return





    
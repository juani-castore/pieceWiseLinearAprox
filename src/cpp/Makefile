CC = g++
CFLAGS = -std=c++17
SRC = main.cpp FuerzaBruta.cpp BackTracking.cpp ProgramacionDinamica.cpp
OBJ = $(SRC:.cpp=.o)
EXEC = pwl_fit

all: $(EXEC)

$(EXEC): $(OBJ)
	$(CC) $(OBJ) -o $(EXEC)

%.o: %.cpp
	$(CC) $(CFLAGS) -c -O3 $< -o $@

clean:
	rm -f $(OBJ) $(EXEC)
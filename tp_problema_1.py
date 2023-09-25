import math
from typing import Any
import scanf

    

class Sucursal:
    def __init__(self, numero, demanda):
        self.numero = numero
        self.demanda = demanda
    def getNum(self):
        return self.numero
    def getDem(self):
        return self.demanda


class SucursalOrdenada:
    def __init__(self, sucursal, x, y):
        self.x  = x
        self.y = y
        self.numero = sucursal.getNum()
        self.demanda = sucursal.getDem()
    def getNumero(self):
        return self.numero
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getDemanda(self):
        return self.demanda

def distancia(i,j):
    return math.sqrt(math.pow(i.getX()- j.getX(),2) + math.pow(i.getY() - j.getY(),2))
    


class Entrega:
    def __init__(self, capacidad, sucursales):
        self.capacidad = capacidad
        self.sucursales = sucursales
    def getCapacidad(self):
        return self.capacidad
    def getSucursales(self):
        return self.sucursales
    def matriz_de_distancias(self):
        sucursales = self.sucursales
        matriz_de_sucursales =[]

        for i in sucursales:
            matriz_de_sucursales.append([])
            for j in sucursales:
                matriz_de_sucursales[i.numero - 1].append([j.numero,distancia(i,j)])
        
        return matriz_de_sucursales
     

def leer_problema(path_file):
    try:
        archivo = open(path_file, 'r')
    except(FileNotFoundError):
        return

    primera_linea = archivo.readline()
    segunda_linea = archivo.readline()
    archivo.readline()
    linea = archivo.readline()
    capacidad = scanf.scanf("%*s %i", primera_linea)[0]
    c_sucursales = scanf.scanf("%*s %i", segunda_linea)[0]
    sucursales = []

    while(linea != "FIN DEMANDAS\n"):
        datos = scanf.scanf("%i %i", linea)
        sucursal = Sucursal(datos[0], datos[1])
        sucursales.append(sucursal)
        linea = archivo.readline()
    
    archivo.readline()
    archivo.readline()
    linea = archivo.readline()
    while(linea != "EOF"):
        datos = scanf.scanf("%i %f %f", linea)
        sucursal = sucursales[datos[0]-1]
        sucursal_ordenada = SucursalOrdenada(sucursal, datos[1], datos[2])
        sucursales[datos[0]-1] = sucursal_ordenada
        linea = archivo.readline()
    
    return Entrega(capacidad, sucursales)
        
def calcular_caminos(entrega):
    matriz_de_distancias = entrega.matriz_de_distancias()
    sucursales = entrega.getSucursales()
    recorridos = []
    for i in [*range(0, len(sucursales))]:
        recorrido = []
        recorrido.append(i+1)        
        distancia_total = 0
        i_sucursal_actual = i
        carga = 0
        recorrido_valido = True
        pares_ordenados = []
        
        while(len(recorrido) != len(sucursales)):
            sucursal_actual = sucursales[i_sucursal_actual]
            ordenado = sorted(matriz_de_distancias[i_sucursal_actual], key=lambda par: par[1])
            indice = 1
            carga += sucursal_actual.getDemanda()
            par_ordenado = [sucursal_actual.getX(), sucursal_actual.getY(),sucursal_actual.getDemanda(), sucursal_actual.getNumero()]
            pares_ordenados.append(par_ordenado)

            if(carga < 0 or carga > entrega.getCapacidad()):
                recorrido_valido = False
            
            while(recorrido.__contains__(ordenado[indice][0]) or (sucursales[ordenado[indice][0]-1].getDemanda() + carga < 0) or sucursales[ordenado[indice][0]-1].getDemanda() + carga >=  + entrega.getCapacidad()):
                indice = indice + 1
                if(indice >= len(sucursales)):
                    recorrido_valido = False
                    break
            if(indice >= len(sucursales)):
                break   
            recorrido.append(ordenado[indice][0])
            distancia_total = distancia_total + ordenado[indice][1]
            i_sucursal_actual = ordenado[indice][0] - 1

        if(recorrido_valido == True):
            sucursal_actual = sucursales[i_sucursal_actual]
            par_ordenado = [sucursal_actual.getX(), sucursal_actual.getY(),sucursal_actual.getDemanda(), sucursal_actual.getNumero()]
            pares_ordenados.append(par_ordenado)
            recorridos.append([recorrido,distancia_total,pares_ordenados])
    
    return recorridos
        
    

def main():
    entrega = leer_problema("problema_uno.txt")
    caminos = calcular_caminos(entrega)
    mejor_camino = sorted(caminos, key=lambda par: par[1])[0]
    
    


if __name__ == "__main__":
    main()

import math
import scanf
import numpy as np
from numpy.random import seed
from numpy.random import shuffle
from numpy.random import choice


    

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
    x = abs(i.x - j.x)
    y = abs(i.y - j.y)
    return math.sqrt(x*x + y*y)
    


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
        matriz_de_sucursales = np.zeros((len(sucursales),len(sucursales),2))
        
        for i in sucursales:
            
            for j in sucursales:
                
                matriz_de_sucursales[i.numero - 1,j.numero-1,0] = j.numero
                matriz_de_sucursales[i.numero - 1,j.numero-1,1] = distancia(i,j) 
                
        print("listo loco")
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
    i = 3
    while(len(recorridos) != 15):
        print(i)
        recorrido = []
        recorrido.append(i+1)        
        distancia_total = 0
        i_sucursal_actual = i
        carga = 0
        recorrido_valido = True
        pares_ordenados = []
        
        while(len(recorrido) != len(sucursales)):
            sucursal_actual = sucursales[int(i_sucursal_actual)]
            ordenado = sorted(matriz_de_distancias[i_sucursal_actual], key=lambda par: par[1])
            indice = 1
            carga += sucursal_actual.getDemanda()
            par_ordenado = [sucursal_actual.getX(), sucursal_actual.getY(),sucursal_actual.getDemanda(), sucursal_actual.getNumero()]
            pares_ordenados.append(par_ordenado)

            if(carga < 0 or carga > entrega.getCapacidad()):
                recorrido_valido = False
            
            while(recorrido.__contains__(ordenado[indice][0]) or (sucursales[int(ordenado[indice][0]-1)].getDemanda() + carga <= 0) or sucursales[int(ordenado[indice][0]-1)].getDemanda() + carga >  + entrega.getCapacidad()):
                indice = indice + 1
                if(indice >= len(sucursales)):
                    recorrido_valido = False
                    break
            if(indice >= len(sucursales)):
                break   
            recorrido.append(int(ordenado[indice][0]))
            
            distancia_total = distancia_total + ordenado[indice][1]
            i_sucursal_actual = int(ordenado[indice][0] - 1)

        if(recorrido_valido == True):
            sucursal_actual = sucursales[int(i_sucursal_actual)]
            par_ordenado = [sucursal_actual.getX(), sucursal_actual.getY(),sucursal_actual.getDemanda(), sucursal_actual.getNumero()]
            pares_ordenados.append(par_ordenado)
            recorridos.append([recorrido,distancia_total,pares_ordenados])
        i = i+1
    
    return recorridos

#ESTO NO ES UTILIZADO PARA LA OBTENCIÓN DE LA SOLUCIÓN
#-----------------------------------------------------

def generar_posibles_recorridos(sucursales, cantidad):
    recorridos = []
    for i in range(0, cantidad):
        lista = [j for j in sucursales]
        shuffle(lista)
        recorridos.append([lista, True])
    
    return recorridos


def verificar_recorrido_valido(recorrido,capacidad, recorridos, sucursales):
    dist = 0
    carga = 0
    sucursales_visitadas = []

    sucursales_no_visitadas = [*range(1, len(recorrido[0])+1)]
    print(len(sucursales_no_visitadas))
    for i in [*range(0, len(recorrido[0]))]:
        if(carga + recorrido[0][i].getDemanda() < 0 or carga + recorrido[0][i].getDemanda()> capacidad):
            numeros_para_elegir = [j for j in sucursales_no_visitadas]
            nueva_sucursal = choice(numeros_para_elegir)
            while(sucursales_visitadas.__contains__(nueva_sucursal) or (carga + sucursales[nueva_sucursal-1].getDemanda()>capacidad
                                                                          or sucursales[nueva_sucursal-1].getDemanda() < 0)):
                numeros_para_elegir.remove(nueva_sucursal)
                if(len(numeros_para_elegir) == 0):
                    recorrido[1] = False
                    break
                nueva_sucursal = choice(numeros_para_elegir)
            if(recorrido[1] == False):
                break
            s = sucursales[nueva_sucursal - 1]
            indice_actual_ns = recorrido[0].index(s)
            
            aux = recorrido[0][i]
            recorrido[0][i] = recorrido[0][indice_actual_ns]
            recorrido[0][indice_actual_ns] = aux
        sucursales_visitadas.append(recorrido[0][i].getNumero())
        sucursales_no_visitadas.remove(recorrido[0][i].getNumero())
        carga += recorrido[0][i].getDemanda()
        if(i == 0):
            dist += distancia(recorrido[0][0], 0)
        else:
            dist += distancia(recorrido[0][i], recorrido[0][i-1])
    print(dist)
    
    return [dist, sucursales_visitadas]

def validar_recorridos(recorridos, capacidad, sucursales):
    a_eliminar = []
    ind = 0
    for i in recorridos:
        i.append(verificar_recorrido_valido(i, capacidad, recorridos, sucursales))
        
    for i in recorridos:
        if(i[1] == False):
            a_eliminar.append(ind)
        ind += 1
    a_eliminar.sort(reverse=True)
    for i in a_eliminar:
        recorridos.remove(recorridos[i])
    
    return recorridos
    

    
def resolver_segundo_problema(entrega):
    recorridos = generar_posibles_recorridos(entrega.getSucursales(), 1)
    while(len(validar_recorridos(recorridos, entrega.getCapacidad(), entrega.getSucursales()))<= 0):
        recorridos = generar_posibles_recorridos(entrega.getSucursales(),1)
    
    print(recorridos[0][2][1])
    print("distancia" + str(recorridos[0][2][0]))
    
#-----------------------------------------------------------------------------    
    

def main():
    entrega = leer_problema("segundo_problema.txt")
    caminos = calcular_caminos(entrega)
    mejor_camino = sorted(caminos, key=lambda par: par[1])[0]
    file = open("respuesta.txt", "w")
    for i in mejor_camino[0]:
        file.write(str(i) + " ")
    print(mejor_camino[1])
    # La posición 0 del vector mejor_camino contiene el recorrido, la posición 1 contiene la distancia total y 
    # la posicion 2 contiene un vector con los pares X,Y, la demanda y el número de cada sucursal en el orden en el que fueron recorridas

    


if __name__ == "__main__":
    main()
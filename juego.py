from terreno import Terreno
from direccion import Derecha, Izquierda
from ranas import Rana
from threading import Lock
from colorama import init
import os

DEBUG = False
TIPO_JUEGO = 1

if __name__ == '__main__':
    os.system('clear')
    init(autoreset=True)
    ranas = []
    slots_lock = Lock()
    if (TIPO_JUEGO == 1):
        cantidadD = int(input("Ingrese cantidad de Ranas de cada lado: "))
        cantidadI = cantidadD
    else:
        cantidadD = int(input("Ingrese cantidad de Ranas para el lado derecho: "))
        cantidadI = int(input("Ingrese cantidad de Ranas para el lado izquierdo: "))
    terreno = Terreno(DEBUG)
    for i in range(cantidadI):
        rana = Rana(slots_lock, 'Rana Izquierda {}'.format(i+1), i, Derecha(), terreno, DEBUG)
        ranas.append(rana)
        terreno.agregar_rana(rana)
    
    for i in range(cantidadD):
        rana = Rana(slots_lock, 'Rana Derecha {}'.format(i+1), i, Izquierda(), terreno, DEBUG)
        ranas.append(rana)
        terreno.agregar_rana(rana)

    terreno.startGame()
    terreno.imprimir_estado()
    if (TIPO_JUEGO == 1):
        print('\nPara {} ranas de cada lado, el juego termina en {} movidas'.format(cantidadD, terreno.get_cantidad_movidas()))
    else:
        print('\nPara {} ranas de la derecha y {} de la izquierda, el juego termina en {} movidas'.format(cantidadD, cantidadI, terreno.get_cantidad_movidas()))
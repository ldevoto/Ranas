from threading import Thread
from time import sleep
from colorama import Fore

class Rana(Thread):
    def __init__(self, lock, nombre, id, direccion, terreno, debug):
        super().__init__(name=nombre)
        self.lock = lock
        self.id = id
        self.direccion = direccion
        self.terreno = terreno
        self.finalizo = False
        self.debug = debug
        self.ultra_debug = False
        self.color = Fore.RESET
    
    def run(self):
        while (not self.finalizo):
            self.lock.acquire()
            if (self.ultra_debug):
                print('--{} fue habilitada para ejecutar'.format(self.name))
                print('No debería haber ninguna interrupcion en este flujo de texto')
                print('Chequeando si le corresponde avanzar..')
            if (self.tiene_que_avanzar()):
                if (self.ultra_debug):
                    print('Le corresponde avanzar')
                self.avanzar()
                if (self.ultra_debug):
                    print('Avanzó')
                    print('Chequeando si llegó al final..')
                if (self.termino()):
                    if (self.ultra_debug):
                        print('Llegó al final. La Rana debe morir!')
                    self.marcar_fin()
                else:
                    print('Todavía no le llegó la hora')
            else:
                if (self.ultra_debug):
                    print('No le corresponde avanzar')
            if (self.ultra_debug):
                print('Liberando el lock..')
            self.lock.release()
        if (self.debug):
            print('{} finalizó'.format(self.name))

    def tiene_que_avanzar(self):
        return (self.tiene_slot_libre() 
            and not self.queda_pegado_a_la_proxima()
            and (self.es_la_ultima() 
                or self.se_separa_un_slot() 
                or self.se_separa_mas_de_un_slot_saltando()
                or self.llego_al_final()))
    
    def avanzar(self):
        self.color = Fore.GREEN
        self.terreno.avanzar(self, self.direccion.get_proximo_indice(self, self.terreno, self.proximo_movimiento()))

    def termino(self):
        return not self.tiene_slot_libre() and self.todos_slots_ocupados()
    
    def marcar_fin(self):
        self.finalizo = True

    def llego_al_final(self):
        return self.terreno.llega_al_final(self, self.proximo_movimiento()) or self.terreno.todo_slots_ocupados(self)
    
    def proximo_movimiento(self):
        return self.direccion.proximo_movimiento(self.terreno, self)
    
    def tiene_que_saltar(self):
        return self.proximo_movimiento() == 2

    def todos_slots_ocupados(self):
        return self.terreno.todo_slots_ocupados(self)
    
    def tiene_slot_libre(self):
        return self.proximo_movimiento() >= 1
    
    def queda_pegado_a_la_proxima(self):
        return self.terreno.se_pega_a_la_proxima(self, self.proximo_movimiento())
    
    def es_la_ultima(self):
        return self.terreno.es_la_ultima(self, self.proximo_movimiento())

    def se_separa_un_slot(self):
        return self.terreno.se_separa_un_slot(self, self.proximo_movimiento())
    
    def se_separa_mas_de_un_slot_saltando(self):
        return self.terreno.se_separa_mas_de_un_slot(self, self.proximo_movimiento()) and self.tiene_que_saltar()
    
    def se_mueve_en_direccion(self, direccion):
        return self.direccion.equals(direccion)
    
    def get_direccion(self):
        return self.direccion
    
    def va_hacia_izquierda(self):
        return self.direccion.es_izquierda()
    
    def va_hacia_derecha(self):
        return self.direccion.es_derecha()
    
    def va_en_mismo_sentido_que(self, rana):
        return self.se_mueve_en_direccion(rana.get_direccion())
    
    def es_rana(self):
        return True
    
    def es_vacio(self):
        return False
    
    def __str__(self):
        con_color = self.color + self.direccion.__str__()
        self.reset_color()
        return con_color

    def reset_color(self):
        if (self.termino()):
            self.color = Fore.RED
        else:
            self.color = Fore.RESET
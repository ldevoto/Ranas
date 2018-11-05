from threading import Thread, Lock
from time import sleep
from colorama import Fore

lock = Lock()

class Rana(Thread):
    def __init__(self, permiso_lectura, permiso_esritura, cantidad, nombre, id, direccion, terreno, debug):
        super().__init__(name=nombre)
        self.permiso_lectura = permiso_lectura
        self.permiso_escritura = permiso_esritura
        self.cantidad = cantidad
        self.id = id
        self.direccion = direccion
        self.terreno = terreno
        self.finalizo = False
        self.debug = debug
        self.ultra_debug = True
        self.color = Fore.RESET
    
    def run(self):
        while (not self.finalizo):
            self.imprimir("Obteniendo permiso de lectura..")
            self.permiso_lectura.acquire()
            self.imprimir("Permiso de lectura otorgado")
            self.imprimir("Todas las Ranas podrian estar en esta seccion.")
            self.imprimir("Chequeando si tiene que avanzar..")
            avanza = self.tiene_que_avanzar()
            self.imprimir("Liberando permiso de lectura..")
            self.permiso_lectura.release()
            self.imprimir("Permiso de lectura liberado")
            if (avanza):
                self.imprimir("Le corresponde avanzar")
                self.imprimir("Obteniendo permiso de escritura!!!!!!..")
                self.permiso_escritura.acquire()
                self.imprimir("Permiso de escritura obtenido")
                self.imprimir("Una sola Rana puede estar en esta seccion")
                self.imprimir("Se piden todos los permisos de lectura..")
                for i in range(self.cantidad):
                    self.permiso_lectura.acquire()
                    self.imprimir("Permiso de lectura obtenido")
                self.imprimir("Avanza")
                self.avanzar()
                self.imprimir("Se liberan los permisos de lectura")
                for i in range(self.cantidad):
                    self.permiso_lectura.release()
                    self.imprimir("Permiso de lectura liberado")
                self.imprimir("Liberando permiso de escritura..")
                self.permiso_escritura.release()
                self.imprimir("Permiso de escritura liberado")
                self.imprimir("Obteniendo permiso de lectura para chequear fin")
                self.permiso_lectura.acquire()
                self.imprimir("Permiso de lectura obtenido")
                self.imprimir("Chequeando si llegó al final..")
                if (self.termino()):
                    self.imprimir("Llegó al final. Es el final de esta Rana")
                    self.marcar_fin()
                self.imprimir("Liberando permiso de lectura")
                self.permiso_lectura.release()
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
    
    def imprimir(self, mensaje):
        if (self.ultra_debug):
            lock.acquire()
            print("-{} {}".format(self.name, mensaje))
            lock.release()
    
    def __str__(self):
        con_color = self.color + self.direccion.__str__()
        self.reset_color()
        return con_color

    def reset_color(self):
        if (self.termino()):
            self.color = Fore.RED
        else:
            self.color = Fore.RESET
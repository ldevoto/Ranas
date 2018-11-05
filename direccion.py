class Direccion:
    def proximo_movimiento(self, terreno, rana):
        indice = terreno.indice_de(rana)
        indice_1 = self.proximo_indice(indice, 1)
        indice_2 = self.proximo_indice(indice, 2)
        if (not self.excede_maximo(indice_1, terreno) and terreno.get_slot(indice_1).es_vacio()):
                return 1
        else:
            if (not self.excede_maximo(indice_2, terreno) and terreno.get_slot(indice_2).es_vacio() and self.va_en_direccion_contraria(terreno.get_slot(indice_1))):
                return 2
            else:
                return 0
    
    def get_proximo_indice(self, rana, terreno, movimiento):
        return self.proximo_indice(terreno.indice_de(rana), movimiento)
    
    def proximo_indice(self, indice, proximo):
        return indice

    def excede_maximo(self, indice, terreno):
        return True
    
    def va_en_direccion_contraria(self, rana):
        return False
    
    def get_direccion_contraria(self):
        return None

    def es_derecha(self):
        return False

    def es_izquierda(self):
        return False
    
    def equals(self, direccion):
        return False

class Derecha(Direccion):
    def proximo_indice(self, indice, proximo):
        return indice + proximo
    
    def excede_maximo(self, indice, terreno):
        return terreno.excede_maximo(indice)
    
    def va_en_direccion_contraria(self, rana):
        return rana.va_hacia_izquierda()
    
    def get_direccion_contraria(self):
        return Izquierda()
    
    def es_derecha(self):
        return True
    
    def equals(self, direccion):
        return direccion.es_derecha()
    
    def __str__(self):
        return "->"

class Izquierda(Direccion):
    def proximo_indice(self, indice, proximo):
        return indice - proximo
    
    def excede_maximo(self, indice, terreno):
        return terreno.excede_minimo(indice)
    
    def va_en_direccion_contraria(self, rana):
        return rana.va_hacia_derecha()
    
    def get_direccion_contraria(self):
        return Derecha()
    
    def es_izquierda(self):
        return True
    
    def equals(self, direccion):
        return direccion.es_izquierda()
    
    def __str__(self):
        return "<-"
from espacio_vacio import EspacioVacio

class Terreno:
    def __init__(self):
        self.slotsDerechos = []
        self.slotsIzquierdos = []
        self.slots = []
        self.cantidad_movidas = 0
    
    def startGame(self):
        self.slots = self.getSlots()
        self.imprimir_estado()
        for rana in self.slotsDerechos:
            rana.start()
        for rana in self.slotsIzquierdos:
            rana.start()
        for rana in self.slotsDerechos + self.slotsIzquierdos:
            rana.join()
    

    def avanzar(self, rana, indice):
        indice_viejo = self.indice_de(rana)
        if (indice != indice_viejo):
            self.cantidad_movidas += 1
            self.set_slot(indice, rana)
            self.set_slot(indice_viejo, self.get_espacio_vacio())
            self.imprimir_estado()
    
    def agregar_rana(self, rana):
        if (rana.va_hacia_izquierda()):
            self.agregar_rana_derecha(rana)
        else:
            self.agregar_rana_izquierda(rana)
    
    def agregar_rana_derecha(self, rana):
        self.slotsDerechos.append(rana)

    def agregar_rana_izquierda(self, rana):
        self.slotsIzquierdos.append(rana)
    
    def getSlots(self):
        return self.slotsIzquierdos + [self.get_espacio_vacio()] + list(reversed(self.slotsDerechos))
    
    def get_espacio_vacio(self):
        return EspacioVacio()
    
    def se_pega_a_la_proxima(self, rana, movimiento):
        proximo_indice = rana.get_direccion().get_proximo_indice(rana, self, movimiento + 1)
        if not self.excede_topes(proximo_indice):
            proximo_slot = self.get_proximo_slot(rana, movimiento + 1)
            if (proximo_slot.es_rana()):
                return proximo_slot.va_en_mismo_sentido_que(rana) and not proximo_slot.termino()
        return False
    
    def es_la_ultima(self, rana, movimiento):
        return self.get_separacion_de(rana, movimiento) == -1

    def se_separa_un_slot(self, rana, movimiento):
        return self.get_separacion_de(rana, movimiento) == 1
    
    def se_separa_mas_de_un_slot(self, rana, movimiento):
        return self.get_separacion_de(rana, movimiento) > 1
    
    def todo_slots_ocupados(self, rana):
        alguno_desocupado = False
        proximo_indice = rana.get_direccion().get_proximo_indice(rana, self, rana.proximo_movimiento() + 1)
        while (not self.excede_topes(proximo_indice)):
            proximo_slot = self.get_slot(proximo_indice)
            if ( proximo_slot.es_rana() and proximo_slot.va_en_mismo_sentido_que(rana)):
                proximo_indice = rana.get_direccion().proximo_indice(proximo_indice, 1)
            else:
                alguno_desocupado = True
                break
        return not alguno_desocupado
    
    def llega_al_final(self, rana, movimiento):
        return self.es_final(rana.get_direccion().get_proximo_indice(rana, self, movimiento))
    
    def indice_de(self, rana):
        try:
            return self.slots.index(rana)
        except:
            return -1
    
    def cantidad_slots(self):
        return len(self.slots)
    
    def get_slot(self, indice):
        return self.slots[indice]
    
    def set_slot(self, indice, slot):
        self.slots[indice] = slot

    def excede_maximo(self, indice):
        return indice >= self.cantidad_slots()
    
    def excede_minimo(self, indice):
        return indice < 0
    
    def excede_topes(self, indice):
        return self.excede_maximo(indice) or self.excede_minimo(indice)
    
    def es_final(self, indice):
        return indice == 0 or indice == self.cantidad_slots() - 1
    
    def get_proximo_slot(self, rana, movimiento):
        return self.get_slot(self.get_proximo_indice(rana, movimiento))
    
    def get_proximo_indice(self, rana, movimiento):
        return rana.get_direccion().proximo_indice(self.indice_de(rana), movimiento)
    
    def get_separacion_de(self, rana, movimiento):
        indice_proxima_rana = self.indice_de(
                                self.get_proxima_rana(
                                    rana, self.indice_de(rana), 
                                    rana.get_direccion().get_direccion_contraria())
                                )
        if (indice_proxima_rana == -1):
            return -1
        else:
            return abs( indice_proxima_rana - self.get_proximo_indice(rana, movimiento)) - 1
    
    def get_proxima_rana(self, rana, indice, direccion):
        proxima_rana = None
        proximo_indice = direccion.proximo_indice(indice, 1)
        while (not self.excede_maximo(proximo_indice) and not self.excede_minimo(proximo_indice)):
            proximo_slot = self.get_slot(proximo_indice)
            if (proximo_slot.es_rana()):
                if (proximo_slot.va_en_mismo_sentido_que(rana)):
                    proxima_rana = proximo_slot
                    break
            proximo_indice = direccion.proximo_indice(proximo_indice, 1)
        return proxima_rana
    
    def imprimir_estado(self):
        print('{:3}) '.format(self.get_cantidad_movidas()), end='')
        for slot in self.slots:
            print('  {}  '.format(slot), end='')
        print()
    
    def get_cantidad_movidas(self):
        return self.cantidad_movidas

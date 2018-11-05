from colorama import Fore

class EspacioVacio:
    def es_vacio(self):
        return True
    
    def es_rana(self):
        return False
    
    def __str__(self):
        return '..'
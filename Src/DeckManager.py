import pygame

class Mazo():
    def __init__(self, cartas):
        self.cartas = cartas

    def agregar_carta(self, nombre, cantidad):
        if(cantidad >=50 or cantidad <= 0): return
        for i in range(cantidad):
            self.cartas.append(nombre)
    
    def eliminar_carta(self, nombre, cantidad):
        for carta in self.cartas:
            if(carta == nombre):
                self.cartas.remove(carta)

    def limpiar_mazo(self):
        self.cartas = []

    def cantidad_cartas(self):
        return self.cartas.count()

class Mano():
    def __init__(self, screen, cantidad_en_mano, mazo):
        self.cantidad_en_mano = cantidad_en_mano
        self.mazo = mazo
        self.screen = screen


    def dibujar_cartas(self):
        
        for i in range(self.cantidad_en_mano):
            n = pygame.Rect(400 + i * 20, 20, 300, 90)
            pygame.draw.rect(self.screen, (200,200,200), n)

                
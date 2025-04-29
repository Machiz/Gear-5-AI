# card_loader.py
import json
import pygame
import os


class CartaLoader:
    def __init__(self):
        self.cards_data = []

    # Lee un mazo y busca los numeros de las cartas en los archivos JSON para su lectura
    # finalmente convierte los archivos JSON en un objeto de la clase Carta que contiene informacion como color, nombre, etc
    def load_cards(self, json_path, mazo):
        json_f = [file for file in os.listdir(json_path) if file.endswith('.json')]
        for path in json_f:
            if(path == "DON.json"): continue
            with open('assets/JSON/' + path, "r", encoding="utf-8") as f:
                all_cards = json.load(f)
                for carta in mazo:
                    if(carta in all_cards):
                        info = all_cards[carta]
                        if(info['type'] == 'leader'):
                            nueva_carta = CartaLider(info['name'], info['color'], info['type'], info['group'],
                                info['attribute'],info['life'], info['power'], info['effect'],
                                info['images'])
                        elif(info['type'] == 'character'):
                            nueva_carta = CartaPersonaje(info['name'], info['color'], info['type'], info['group'],
                                info['attribute'], info['cost'], info['power'], info['counter'], info['effect'],
                                info['images'])
                        elif(info['type'] == 'stage'):
                            nueva_carta = CartaEscenario(info['name'], info['color'], info['type'], info['group'],
                                info['cost'], info['effect'],
                                info['images'])
                        elif(info['type'] == 'event'):
                            nueva_carta = CartaEvento(info['name'], info['color'], info['type'], info['group'],
                                info['cost'], info['effect'],
                                info['images'])
                        self.cards_data.append(nueva_carta)



class Carta:
    def __init__(self, name, color,type, group, effect, images):
        self.name = name
        self.color = color
        self.type = type
        self.group = group
        self.effect = effect
        self.images = images

        # Estado de juego
        self.is_active = False
        self.tapped = False
        self.position = (0, 0)  # x, y en pantalla

        # Cargar imagen
        self.image = None
        # if images:
        #     try:
        #         self.image = pygame.image.load(images[0]).convert_alpha()
        #         self.image = pygame.transform.scale(self.image, (150, 210))  # redimensionar
        #     except Exception as e:
        #         print(f"Error cargando imagen para {self.name}: {e}")

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.position)

    def on_play(self):
        print(f"{self.name} entra en juego.")


class CartaLider(Carta):
    def __init__(self, name, color,type, group, attribute, life, power, effect, images):
        super().__init__(name, color, type, group, effect, images)
        self.attribute = attribute
        self.life = life
        self.power = power

        # Estado de juego
        self.is_active = False
        self.tapped = False
        self.position = (0, 0)  # x, y en pantalla

        # Cargar imagen
        self.image = None

class CartaPersonaje(Carta):
    def __init__(self, name, color,type, group, attribute,cost, power, counter, effect, images):
        super().__init__(name, color, type, group, effect, images)
        self.attribute = attribute
        self.cost = cost
        self.power = power
        self.counter = counter

        # Estado de juego
        self.is_active = False
        self.tapped = False
        self.position = (0, 0)  # x, y en pantalla

        # Cargar imagen
        self.image = None

class CartaEscenario(Carta):
    def __init__(self, name, color,type, group, cost,effect, images):
        super().__init__(name, color, type, group, effect, images)
        self.cost = cost
        

        # Estado de juego
        self.is_active = False
        self.tapped = False
        self.position = (0, 0)  # x, y en pantalla

        # Cargar imagen
        self.image = None

class CartaEvento(Carta):
    def __init__(self, name, color,type, group, cost, effect, images):
        super().__init__(name, color, type, group, effect, images)
        self.cost = cost

        # Estado de juego
        self.is_active = False
        self.tapped = False
        self.position = (0, 0)  # x, y en pantalla

        # Cargar imagen
        self.image = None
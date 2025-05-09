# card_loader.py
import json
import pygame
import os
import random
import queue

class CartaLoader:
    def __init__(self):
        self.card_data = []
        self.leader_card = []
        self.hand_data = []
        self.shuffled_data = queue.Queue()
        self.selected_card = None
    
    # Lee un mazo y busca los numeros de las cartas en los archivos JSON para su lectura
    # finalmente convierte los archivos JSON en un objeto de la clase Carta que contiene informacion como color, nombre, etc
    def load_card_data(self, json_path, mazo):
        json_f = [file for file in os.listdir(json_path) if file.endswith('.json')]
        for path in json_f:
            if(path == "DON.json"): continue
            with open('assets/JSON/Cards/' + path, "r", encoding="utf-8") as f:
                all_cards = json.load(f)
                for carta in mazo:
                    if(carta in all_cards):
                        info = all_cards[carta]
                        if(info['type'] == 'leader'):
                            nueva_carta = CartaLider(info['name'], info['color'], info['type'], info['group'],
                                info['attribute'],info['life'], info['power'], info['effect'],
                                info['images'])
                            self.leader_card.append(nueva_carta)
                            continue
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
                        self.card_data.append(nueva_carta)

        random.shuffle(self.card_data)
        for i in self.card_data:
            self.shuffled_data.put(i)
    
    def load_hand_images(self, screen, mousePos):
        if(len(self.hand_data) <= 0): return
        if(len(self.hand_data) > 60): return
        i = 0
        start_x = 70
        start_y = 640
        img_size = 0.2
        hover_over_card = 0
        
        for card in self.hand_data:
            img = pygame.image.load('assets/' + card.images)
            img = pygame.transform.scale(img, (img.get_width() * img_size, img.get_height() * img_size))
            
            screen.blit(img, pygame.Rect(start_x + i * 25, start_y - 10 if card == self.selected_card else start_y, img.get_width(), img.get_height()))
            i += 1
        zoomed_size = 0.7
        for b in range(len(self.hand_data)):
            rect = pygame.Rect(start_x + (len(self.hand_data) - 1 - b)* 25, start_y, img.get_width(), img.get_height())
            if(rect.collidepoint(mousePos)):
                self.selected_card = self.hand_data[len(self.hand_data) - 1 - b]
                card = self.hand_data[len(self.hand_data) - 1 - b]
                img = pygame.image.load('assets/' + card.images).convert_alpha()
                img = pygame.transform.smoothscale(img, (img.get_width() * zoomed_size, img.get_height() * zoomed_size))
                screen.blit(img, (100, 150))
                hover_over_card += 1
                break
            
            
        
        # mostrar carta lider y ver si el mouse se posiciona sobre ella
        leader_x = 920
        leader_y = 530
        img = pygame.image.load('assets/' + self.leader_card[0].images)
        img = pygame.transform.scale(img, (img.get_width() * img_size, img.get_height() * img_size))
        screen.blit(img, (leader_x, leader_y - 10 if self.leader_card[0] == self.selected_card else leader_y))
        rect = pygame.Rect(leader_x, leader_y, img.get_width(), img.get_height())
        if(rect.collidepoint(mousePos)):
            self.selected_card = self.leader_card[0]
            img = pygame.image.load('assets/' + self.leader_card[0].images).convert_alpha()
            img = pygame.transform.smoothscale(img, (img.get_width() * zoomed_size, img.get_height() * zoomed_size))
            screen.blit(img, (100, 150))
            hover_over_card += 1
        
        
        print(hover_over_card)
        if hover_over_card == 0 : self.selected_card = None
        
    
    def load_hand_data(self, start_amount = 5): # carga las primeras 5 cartas de tu mano
        for i in range(start_amount):
            self.hand_data.append(self.shuffled_data.get())
        

    def add_hand_data(self, add_amount): # añade cierta cantidad de cartas a la mano
        for i in range(add_amount):
            self.hand_data.append(self.shuffled_data.get())



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
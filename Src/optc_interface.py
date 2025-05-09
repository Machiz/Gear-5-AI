
import pygame
from DeckManager import *
from carta import *


def dibujar_tabla_jugador1():

    # leader rectangle
    pygame.draw.rect(screen, (230,230,230), (xPivot1 + 745, yPivot1 + 525, 90, 120))
    text = text_font.render("LEADER", True, (0,0,0))
    screen.blit(text, (xPivot1 + 750, yPivot1 + 525, 90, 120))

    # stage rectangle
    pygame.draw.rect(screen, (230,230,230), (xPivot1 + 855, yPivot1 + 525, 90, 120))
    text = text_font.render("STAGE", True, (0,0,0))
    screen.blit(text, (xPivot1 + 860, yPivot1 + 525, 90, 120))

    # don area rectangle
    pygame.draw.rect(screen, (230,230,230), (xPivot1 + 525, yPivot1 + 650, 420, 120))
    text = text_font.render("DON!! AREA", True, (0,0,0))
    screen.blit(text, (xPivot1 + 530, yPivot1 + 650, 500, 120))

    # character area rectangle
    pygame.draw.rect(screen, (230,230,230), (xPivot1 + 545, yPivot1 + 400, 500, 120))
    text = text_font.render("CHARACTER AREA", True, (0,0,0))
    screen.blit(text, (xPivot1 + 545, yPivot1 + 400, 570, 120))

    # life area rectangle
    pygame.draw.rect(screen, (230,230,230), (xPivot1 + 410, yPivot1 + 400, 120, 170))
    text = text_font.render("LIFE", True, (0,0,0))
    screen.blit(text, (xPivot1 + 410, yPivot1 + 400, 570, 120))

    # trash area rectangle
    pygame.draw.rect(screen, (230,230,230), (xPivot1 + 955, yPivot1 + 650, 90, 110))
    text = text_font.render("TRASH", True, (0,0,0))
    screen.blit(text, (xPivot1 + 960, yPivot1 + 650, 555, 105))

    # DECK don area rectangle
    pygame.draw.rect(screen, (182, 66, 245), (xPivot1 + 420, yPivot1 + 650, 90, 110))
    text = text_font.render("DON DECK", True, (255,255,255))
    screen.blit(text, (xPivot1 + 425, yPivot1 + 650, 555, 105))

    # DECK main area rectangle
    pygame.draw.rect(screen, (245, 191, 66), (xPivot1 + 955, yPivot1 + 530, 90, 110))
    text = text_font.render("MAIN DECK", True, (255,255,255))
    screen.blit(text, (xPivot1 + 960, yPivot1 + 530, 555, 105))

def dibujar_tabla_jugador2():
    # cost area (don) rectangle

    pygame.draw.rect(screen, (230,230,230), (xPivot2 + 510, yPivot2 + 400, 420, 120))
    text = text_font.render("DON!! AREA", True, (0,0,0))
    screen.blit(text, (xPivot2 + 520, yPivot2 + 400, 500, 120))

    # leader rectangle

    pygame.draw.rect(screen, (230,230,230), (xPivot2 + 620, yPivot2 + 525, 90, 120))
    text = text_font.render("LEADER", True, (0,0,0))
    screen.blit(text, (xPivot2 + 630, yPivot2 + 525, 90, 120))

    # stage rectangle
    pygame.draw.rect(screen, (230,230,230), (xPivot2 + 510, yPivot2 + 525, 90, 120))
    text = text_font.render("STAGE", True, (0,0,0))
    screen.blit(text, (xPivot2 + 520, yPivot2 + 525, 90, 120))

    # character area rectangle
    pygame.draw.rect(screen, (230,230,230), (xPivot2 + 410, yPivot2 + 650, 500, 120))
    text = text_font.render("CHARACTER AREA", True, (0,0,0))
    screen.blit(text, (xPivot2 + 420, yPivot2 + 650, 570, 120))

    # life area rectangle
    pygame.draw.rect(screen, (230,230,230), (xPivot2 + 925, yPivot2 + 600, 120, 170))
    text = text_font.render("LIFE AREA", True, (0,0,0))
    screen.blit(text, (xPivot2 + 925, yPivot2 + 600, 570, 120))

    # trash area rectangle
    pygame.draw.rect(screen, (230,230,230), (xPivot1 + 410, yPivot1 + 10, 90, 110))
    text = text_font.render("TRASH", True, (0,0,0))
    screen.blit(text, (xPivot1 + 410, yPivot1 + 10, 555, 105))

    # DECK don area rectangle
    pygame.draw.rect(screen, (182, 66, 245), (xPivot1 + 945, yPivot1 + 10, 90, 110))
    text = text_font.render("DON DECK", True, (255,255,255))
    screen.blit(text, (xPivot1 + 955, yPivot1 + 10, 555, 105))

    # DECK main area rectangle
    pygame.draw.rect(screen, (245, 191, 66), (xPivot1 + 410, yPivot1 + 130, 90, 110))
    text = text_font.render("MAIN DECK", True, (255,255,255))
    screen.blit(text, (xPivot1 + 410, yPivot1 + 130, 555, 105))

bg_dict = {1:(0.75,0.75),
           2:(2,1.75),
           3:(2.6,2.2),
           4:(2.1,2.3),}


def change_bg(c_bg):
    bg_count = 4
    img = pygame.image.load('assets/Images/Playmat_BGs/bg'+ str(c_bg % bg_count  + 1) + '.jpg')

    w_mult = bg_dict[c_bg % bg_count  + 1]
    img = pygame.transform.smoothscale(img, (img.get_width() * w_mult[0], img.get_height() * w_mult[1]))
    return img


icon = pygame.image.load('assets/Images/Game_Icon/Chopper.png')
table_texture = pygame.image.load('assets/Images/Playmat_BGs/bg1.jpg')
pygame.display.set_icon(icon)
pygame.display.set_caption("OPTCG vs Chopper")

scale = 0.3
table_texture = pygame.transform.smoothscale(table_texture, (table_texture.get_width() * 0.75, table_texture.get_height() * 0.7))

white = (100, 100, 100)
w = 1540
h = 810
screen = pygame.display.set_mode((w, h))
screen.fill((white))
running = 1

pygame.font.init()
text_font = pygame.font.SysFont("Times New Roman", 12)

xPivot1, yPivot1 = 170, 10 # player 1 board pivot
xPivot2, yPivot2 = 170, -385 # player 2 board pivot

n = pygame.Rect(110, 20, 300, 90)
text = text_font.render("Change bg", True, (0,0,0))


## CREADOR DE MAZO

mazo = Mazo([])
mazo.agregar_carta('OP01-002', 1) # agregas el nombre de la carta y la cantidad que quieres
mazo.agregar_carta('OP02-003', 4)
mazo.agregar_carta('OP01-004', 4)
mazo.agregar_carta('OP01-010', 4)

pluffy = Mazo([])
pluffy.agregar_carta('OP05-060', 1)
pluffy.agregar_carta('OP05-070', 1)
pluffy.agregar_carta('OP05-074', 1)
pluffy.agregar_carta('OP06-076', 4)
pluffy.agregar_carta('OP07-064', 4)
pluffy.agregar_carta('OP08-069', 2)
pluffy.agregar_carta('OP09-065', 2)
pluffy.agregar_carta('OP09-069', 4)
pluffy.agregar_carta('OP09-119', 3)
pluffy.agregar_carta('ST10-010', 2)
pluffy.agregar_carta('ST18-001', 4)
pluffy.agregar_carta('ST18-002', 3)
pluffy.agregar_carta('ST18-003', 4)
pluffy.agregar_carta('ST18-004', 4)
pluffy.agregar_carta('ST18-005', 4)
pluffy.agregar_carta('OP05-077', 2)
pluffy.agregar_carta('OP09-078', 4)

# carga de cartas
cargador_cartas = CartaLoader()
cargador_cartas.load_card_data('assets/JSON/Cards/', pluffy.cartas)
cargador_cartas.load_hand_data()


button_timer = 0
current_bg = 1

while running:
    button_timer -= 0.01
    screen.fill((white))
    screen.blit(table_texture, (0,0))
    
    
    # main table rectangle
    pygame.draw.rect(screen, (200,200,200), (380 + xPivot1, 8, 700, 780))

    mousePos = pygame.mouse.get_pos()
    
    # BOTON para cambiar fondo
    pygame.draw.rect(screen, (200,200,200), n)
    screen.blit(text, n)

    if n.collidepoint(mousePos) and button_timer <=0:
        if pygame.mouse.get_pressed()[0] == 1:
                table_texture = change_bg(current_bg)
                current_bg += 1
                button_timer = 1


    dibujar_tabla_jugador1()
    dibujar_tabla_jugador2()
    cargador_cartas.load_hand_images(screen, mousePos)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

















# import pygame
# import sys

# pygame.init()
# WIDTH, HEIGHT = 1200, 800
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("One Piece TCG - 2 Jugadores")
# clock = pygame.time.Clock()
# FONT = pygame.font.SysFont("arial", 16)

# # Colores
# WHITE = (255, 255, 255)
# GRAY = (40, 40, 40)
# BLUE = (50, 50, 200)
# RED = (200, 50, 50)
# BLACK = (0, 0, 0)

# CARD_WIDTH, CARD_HEIGHT = 70, 100

# class Card:
#     def __init__(self, name, cost=1, power=1000):
#         self.name = name
#         self.cost = cost
#         self.power = power
#         self.rested = False
#         self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)

#     def draw(self, surface, x, y, highlight=False):
#         self.rect.topleft = (x, y)
#         pygame.draw.rect(surface, BLUE, self.rect)
#         pygame.draw.rect(surface, WHITE if not highlight else RED, self.rect, 2)
#         name_text = FONT.render(self.name, True, WHITE)
#         cost_text = FONT.render(f"{self.cost}/{self.power}", True, WHITE)
#         surface.blit(name_text, (x + 5, y + 5))
#         surface.blit(cost_text, (x + 5, y + 25))
#         if self.rested:
#             pygame.draw.line(surface, WHITE, self.rect.topleft, self.rect.bottomright, 2)

# class Player:
#     def __init__(self, name, bottom=True):
#         self.name = name
#         self.hand = [Card(f"C{i+1}", cost=2+i%3, power=3000+i*500) for i in range(5)]
#         self.board = []
#         self.life = 5
#         self.bottom = bottom

#     def draw_hand(self, surface):
#         y = HEIGHT - CARD_HEIGHT - 10 if self.bottom else 10
#         for i, card in enumerate(self.hand):
#             x = 100 + i * (CARD_WIDTH + 10)
#             card.draw(surface, x, y)

#     def draw_board(self, surface):
#         y = HEIGHT // 2 + 80 if self.bottom else HEIGHT // 2 - CARD_HEIGHT - 80
#         for i, card in enumerate(self.board):
#             x = 150 + i * (CARD_WIDTH + 10)
#             card.draw(surface, x, y)

#     def draw_life(self, surface):
#         x = WIDTH - 90
#         y = HEIGHT - 150 if self.bottom else 50
#         pygame.draw.rect(surface, RED, (x, y, 60, 30))
#         text = FONT.render(f"Vida: {self.life}", True, WHITE)
#         surface.blit(text, (x + 5, y + 5))

# # Crear jugadores
# player1 = Player("Jugador 1", bottom=True)
# player2 = Player("Jugador 2", bottom=False)

# # Simular que ambos tienen 3 cartas en campo
# for _ in range(3):
#     player1.board.append(player1.hand.pop(0))
#     player2.board.append(player2.hand.pop(0))

# fase_actual = "MAIN PHASE"

# # Bucle principal
# running = True
# while running:
#     screen.fill(GRAY)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Dibujar texto de fase
#     pygame.draw.rect(screen, BLACK, (0, HEIGHT // 2 - 20, WIDTH, 40))
#     phase_text = FONT.render(f"Fase actual: {fase_actual}", True, WHITE)
#     screen.blit(phase_text, (WIDTH // 2 - 60, HEIGHT // 2 - 10))

#     # Dibujar mano, tablero y vida
#     player1.draw_hand(screen)
#     player1.draw_board(screen)
#     player1.draw_life(screen)

#     player2.draw_hand(screen)
#     player2.draw_board(screen)
#     player2.draw_life(screen)

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()
# sys.exit()

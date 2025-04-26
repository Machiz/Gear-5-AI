# Fase 1: Inicialización y Configuración
import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("One Piece Card Game (Tapete Oficial)")

# Cargar imágenes de fondo (simuladas con colores)
BACKGROUND = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND.fill((20, 50, 80))  # Azul marino oscuro como fondo
# Dibujar el diseño del tapete One Piece
pygame.draw.rect(BACKGROUND, (30, 70, 110), (50, 50, SCREEN_WIDTH-100, SCREEN_HEIGHT-100), border_radius=20)
pygame.draw.rect(BACKGROUND, (40, 90, 130), (70, 70, SCREEN_WIDTH-140, SCREEN_HEIGHT-140), border_radius=15)

# Colores adaptados al estilo One Piece
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 30, 30)  # Rojo más oscuro
BLUE = (30, 100, 200)  # Azul One Piece
YELLOW = (255, 200, 0)  # Amarillo como el sombrero de Luffy
GREEN = (50, 180, 50)
PURPLE = (150, 50, 180)
ORANGE = (255, 120, 0)  # Naranja para los DON!!

# Fase 2: Definición de Clases
class Card(pygame.sprite.Sprite):
    def __init__(self, name, color, power=0, cost=0, effect=None, card_type="Character"):
        super().__init__()
        self.name = name
        self.color = color
        self.power = power
        self.cost = cost
        self.effect = effect
        self.card_type = card_type
        self.image = pygame.Surface((100, 140))  # Tamaño más grande para las cartas
        self.image.fill((240, 240, 240))  # Fondo blanco para las cartas
        pygame.draw.rect(self.image, self.color, (5, 5, 90, 130), 2, border_radius=5)
        self.rect = self.image.get_rect()
        self.is_rested = False
        self.is_active = False
        self.font_small = pygame.font.Font(None, 22)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_large = pygame.font.Font(None, 36)

    def draw(self, surface, position):
        self.rect.topleft = position
        surface.blit(self.image, self.rect)
        
        # Dibujar el diseño de la carta al estilo One Piece
        if self.card_type == "Leader":
            pygame.draw.rect(self.image, (220, 220, 220), (10, 10, 80, 30), border_radius=3)
            pygame.draw.rect(self.image, self.color, (10, 45, 80, 85), border_radius=3)
        elif self.card_type == "Life":
            pygame.draw.rect(self.image, (220, 220, 220), (10, 10, 80, 120), border_radius=3)
        else:
            pygame.draw.rect(self.image, self.color, (10, 10, 80, 30), border_radius=3)
            pygame.draw.rect(self.image, (220, 220, 220), (10, 45, 80, 85), border_radius=3)
        
        # Texto de la carta
        name_text = self.font_small.render(self.name, True, BLACK)
        self.image.blit(name_text, (15, 15))
        
        if self.card_type == "Leader":
            power_text = self.font_large.render(f"PWR: {self.power}", True, BLACK)
            self.image.blit(power_text, (15, 50))
        elif self.card_type != "Life":
            cost_text = self.font_medium.render(f"COST: {self.cost}", True, BLACK)
            power_text = self.font_medium.render(f"PWR: {self.power}", True, BLACK)
            self.image.blit(cost_text, (15, 50))
            self.image.blit(power_text, (15, 80))
        
        if self.is_rested:
            pygame.draw.line(self.image, RED, (10, 10), (90, 130), 3)
            pygame.draw.line(self.image, RED, (90, 10), (10, 130), 3)
        
        if self.is_active:
            pygame.draw.rect(self.image, YELLOW, (5, 5, 90, 130), 3, border_radius=5)

class DonCard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill(ORANGE)
        pygame.draw.circle(self.image, YELLOW, (30, 30), 25)
        font = pygame.font.Font(None, 40)
        text = font.render("D!!", True, BLACK)
        text_rect = text.get_rect(center=(30, 30))
        self.image.blit(text, text_rect)
        self.rect = self.image.get_rect()

    def draw(self, surface, position):
        self.rect.topleft = position
        surface.blit(self.image, self.rect)

class Zone:
    def __init__(self, name, rect, color=(50, 50, 50), text_color=WHITE):
        self.name = name
        self.rect = rect
        self.color = color
        self.text_color = text_color
        self.cards = []
        self.font = pygame.font.Font(None, 24)

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def draw(self, surface):
        # Dibujar zona con estilo One Piece
        pygame.draw.rect(surface, self.color, self.rect, 2, border_radius=10)
        if len(self.cards) == 0:  # Solo mostrar nombre si no hay cartas
            text = self.font.render(self.name, True, self.text_color)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(None, 30)
        self.text_surface = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        surface.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()

# Fase 3: Configuración Inicial del Juego
player1_hand = []
player2_hand = []
player1_leader = Card("Monkey D. Luffy", RED, power=5000, card_type="Leader")
player2_leader = Card("Kaido", PURPLE, power=5000, card_type="Leader")
player1_don = 0
player2_don = 0
player1_don_deck = [DonCard() for _ in range(10)]
player2_don_deck = [DonCard() for _ in range(10)]
player1_don_active = 0
player2_don_active = 0
player1_life = [Card(f"Vida {i+1}", WHITE, card_type="Life") for i in range(5)]
player2_life = [Card(f"Vida {i+1}", WHITE, card_type="Life") for i in range(5)]
player1_deck = [Card(f"Zoro", GREEN, power=random.randint(3000, 6000), cost=random.randint(1, 5)) for _ in range(2)] + \
               [Card(f"Sanji", BLUE, power=random.randint(3000, 6000), cost=random.randint(1, 5)) for _ in range(2)] + \
               [Card(f"Nami", YELLOW, power=random.randint(2000, 5000), cost=random.randint(1, 4)) for _ in range(1)]
player2_deck = [Card(f"King", PURPLE, power=random.randint(3000, 6000), cost=random.randint(1, 5)) for _ in range(2)] + \
               [Card(f"Queen", GREEN, power=random.randint(3000, 6000), cost=random.randint(1, 5)) for _ in range(2)] + \
               [Card(f"Jack", RED, power=random.randint(2000, 5000), cost=random.randint(1, 4)) for _ in range(1)]
random.shuffle(player1_deck)
random.shuffle(player2_deck)
player1_trash = []
player2_trash = []
player1_stage = None
player2_stage = None
player1_character_area = []
player2_character_area = []
player1_cost_area = []
player2_cost_area = []

# Fase 4: Definición de Zonas del Juego con nueva distribución
# Jugador 1 (abajo)
p1_life_zone = Zone("LIFE", pygame.Rect(50, SCREEN_HEIGHT - 180, 100, 140), (180, 50, 50))
p1_hand_zone = Zone("HAND", pygame.Rect(170, SCREEN_HEIGHT - 180, 600, 140), (70, 70, 70))
p1_don_deck_zone = Zone("DON!! DECK", pygame.Rect(790, SCREEN_HEIGHT - 180, 100, 70), ORANGE)
p1_cost_area_zone = Zone("COST", pygame.Rect(790, SCREEN_HEIGHT - 100, 100, 70), (30, 70, 30))
p1_leader_zone = Zone("LEADER", pygame.Rect(910, SCREEN_HEIGHT - 180, 100, 140), (80, 30, 30))
p1_character_area_zone = Zone("CHARACTER", pygame.Rect(910, SCREEN_HEIGHT - 320, 400, 130), (40, 40, 40))
p1_stage_zone = Zone("STAGE", pygame.Rect(1030, SCREEN_HEIGHT - 180, 100, 70), (70, 70, 30))
p1_deck_zone = Zone("DECK", pygame.Rect(1150, SCREEN_HEIGHT - 180, 100, 70), (30, 30, 70))
p1_trash_zone = Zone("TRASH", pygame.Rect(1270, SCREEN_HEIGHT - 180, 100, 70), (70, 30, 30))

# Jugador 2 (arriba)
p2_life_zone = Zone("LIFE", pygame.Rect(50, 50, 100, 140), (180, 50, 50))
p2_hand_zone = Zone("HAND", pygame.Rect(170, 50, 600, 140), (70, 70, 70))
p2_don_deck_zone = Zone("DON!! DECK", pygame.Rect(790, 50, 100, 70), ORANGE)
p2_cost_area_zone = Zone("COST", pygame.Rect(790, 130, 100, 70), (30, 70, 30))
p2_leader_zone = Zone("LEADER", pygame.Rect(910, 50, 100, 140), (80, 30, 80))
p2_character_area_zone = Zone("CHARACTER", pygame.Rect(910, 190, 400, 130), (40, 40, 40))
p2_stage_zone = Zone("STAGE", pygame.Rect(1030, 50, 100, 70), (70, 70, 30))
p2_deck_zone = Zone("DECK", pygame.Rect(1150, 50, 100, 70), (30, 30, 70))
p2_trash_zone = Zone("TRASH", pygame.Rect(1270, 50, 100, 70), (70, 30, 30))

game_phase = "START_PHASE"
current_player = 1

next_phase_button = Button("Next Phase", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 50, 150, 40, GREEN, (0, 180, 0), lambda: next_phase())
end_turn_button = Button("End Turn", SCREEN_WIDTH - 370, SCREEN_HEIGHT - 50, 150, 40, YELLOW, (180, 180, 0), lambda: end_turn())

def draw_text(surface, text, size, x, y, color=WHITE, bold=False):
    font = pygame.font.Font(None, size)
    font.set_bold(bold)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(x, y))
    surface.blit(text_surface, text_rect)

def draw_game_state():
    screen.blit(BACKGROUND, (0, 0))
    
    # Dibujar todas las zonas
    # Jugador 1 (abajo)
    p1_life_zone.draw(screen)
    p1_hand_zone.draw(screen)
    p1_don_deck_zone.draw(screen)
    p1_cost_area_zone.draw(screen)
    p1_leader_zone.draw(screen)
    p1_character_area_zone.draw(screen)
    p1_stage_zone.draw(screen)
    p1_deck_zone.draw(screen)
    p1_trash_zone.draw(screen)

    # Jugador 2 (arriba)
    p2_life_zone.draw(screen)
    p2_hand_zone.draw(screen)
    p2_don_deck_zone.draw(screen)
    p2_cost_area_zone.draw(screen)
    p2_leader_zone.draw(screen)
    p2_character_area_zone.draw(screen)
    p2_stage_zone.draw(screen)
    p2_deck_zone.draw(screen)
    p2_trash_zone.draw(screen)

    # Dibujar cartas en las zonas
    # Jugador 1
    player1_leader.draw(screen, p1_leader_zone.rect.topleft)
    
    for i, card in enumerate(player1_life):
        card.draw(screen, (p1_life_zone.rect.x + 10, p1_life_zone.rect.y + 10 + i * 25))
    
    for i, card in enumerate(player1_hand):
        card.draw(screen, (p1_hand_zone.rect.x + 10 + i * 110, p1_hand_zone.rect.y + 10))
    
    for i, card in enumerate(player1_character_area):
        card.draw(screen, (p1_character_area_zone.rect.x + 10 + i * 110, p1_character_area_zone.rect.y + 10))
    
    # Dibujar DON!! activos en el área de coste
    for i in range(min(player1_don_active, 5)):  # Máximo 5 DON!! visibles
        player1_don_deck[i].draw(screen, (p1_cost_area_zone.rect.x + 10 + i * 18, p1_cost_area_zone.rect.y + 10))
    
    # Jugador 2
    player2_leader.draw(screen, p2_leader_zone.rect.topleft)
    
    for i, card in enumerate(player2_life):
        card.draw(screen, (p2_life_zone.rect.x + 10, p2_life_zone.rect.y + 10 + i * 25))
    
    for i, card in enumerate(player2_hand):
        card.draw(screen, (p2_hand_zone.rect.x + 10 + i * 110, p2_hand_zone.rect.y + 10))
    
    for i, card in enumerate(player2_character_area):
        card.draw(screen, (p2_character_area_zone.rect.x + 10 + i * 110, p2_character_area_zone.rect.y + 10))
    
    # Dibujar DON!! activos en el área de coste
    for i in range(min(player2_don_active, 5)):  # Máximo 5 DON!! visibles
        player2_don_deck[i].draw(screen, (p2_cost_area_zone.rect.x + 10 + i * 18, p2_cost_area_zone.rect.y + 10))
    
    # Información del juego
    draw_text(screen, f"Phase: {game_phase}", 36, SCREEN_WIDTH // 2 - 100, 20, YELLOW, True)
    draw_text(screen, f"Player {current_player}'s Turn", 36, SCREEN_WIDTH // 2 - 120, 60, WHITE, True)
    
    # Contadores de DON!!
    draw_text(screen, f"DON!!: {player1_don_active}", 28, p1_don_deck_zone.rect.x, p1_don_deck_zone.rect.y - 30, ORANGE)
    draw_text(screen, f"DON!!: {player2_don_active}", 28, p2_don_deck_zone.rect.x, p2_don_deck_zone.rect.y - 30, ORANGE)
    
    # Botones
    next_phase_button.draw(screen)
    end_turn_button.draw(screen)

    pygame.display.flip()

def next_phase():
    global game_phase, current_player, player1_don_active, player2_don_active

    if game_phase == "START_PHASE":
        game_phase = "DRAW_PHASE"
        if current_player == 1 and not player1_hand:
            for _ in range(5):
                if player1_deck:
                    player1_hand.append(player1_deck.pop(0))
        elif current_player == 2 and not player2_hand:
            for _ in range(5):
                if player2_deck:
                    player2_hand.append(player2_deck.pop(0))
    elif game_phase == "DRAW_PHASE":
        if current_player == 1 and player1_deck:
            player1_hand.append(player1_deck.pop(0))
        elif current_player == 2 and player2_deck:
            player2_hand.append(player2_deck.pop(0))
        game_phase = "DON_PHASE"
    elif game_phase == "DON_PHASE":
        if current_player == 1:
            player1_don_active = min(len(player1_don_deck), player1_don_active + 2)
        else:
            player2_don_active = min(len(player2_don_deck), player2_don_active + 2)
        game_phase = "MAIN_PHASE"
    elif game_phase == "MAIN_PHASE":
        game_phase = "ATTACK_PHASE"
    elif game_phase == "ATTACK_PHASE":
        game_phase = "END_PHASE"
    elif game_phase == "END_PHASE":
        current_player = 3 - current_player
        game_phase = "START_PHASE"

def end_turn():
    global current_player, game_phase
    current_player = 3 - current_player
    game_phase = "START_PHASE"

# Fase 6: Loop Principal del Juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        next_phase_button.handle_event(event)
        end_turn_button.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and current_player == 1 and player1_hand:
                card_to_play = player1_hand.pop(0)
                if player1_don_active >= card_to_play.cost:
                    player1_character_area.append(card_to_play)
                    player1_don_active -= card_to_play.cost
                    print(f"Player 1 played: {card_to_play.name}")
                else:
                    player1_hand.append(card_to_play)
                    print("Not enough DON!!")
            elif event.key == pygame.K_2 and current_player == 2 and player2_hand:
                card_to_play = player2_hand.pop(0)
                if player2_don_active >= card_to_play.cost:
                    player2_character_area.append(card_to_play)
                    player2_don_active -= card_to_play.cost
                    print(f"Player 2 played: {card_to_play.name}")
                else:
                    player2_hand.append(card_to_play)
                    print("Not enough DON!!")

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for card in player1_hand:
                if card.rect.collidepoint(mouse_pos):
                    card.is_active = not card.is_active
            for card in player2_hand:
                if card.rect.collidepoint(mouse_pos):
                    card.is_active = not card.is_active
            for card in player1_character_area:
                if card.rect.collidepoint(mouse_pos):
                    card.is_rested = not card.is_rested
            for card in player2_character_area:
                if card.rect.collidepoint(mouse_pos):
                    card.is_rested = not card.is_rested

    draw_game_state()

pygame.quit()
sys.exit()
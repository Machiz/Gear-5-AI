import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("One Piece TCG - 2 Jugadores")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 16)

# Colores
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
BLUE = (50, 50, 200)
RED = (200, 50, 50)
BLACK = (0, 0, 0)

CARD_WIDTH, CARD_HEIGHT = 70, 100

class Card:
    def __init__(self, name, cost=1, power=1000):
        self.name = name
        self.cost = cost
        self.power = power
        self.rested = False
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)

    def draw(self, surface, x, y, highlight=False):
        self.rect.topleft = (x, y)
        pygame.draw.rect(surface, BLUE, self.rect)
        pygame.draw.rect(surface, WHITE if not highlight else RED, self.rect, 2)
        name_text = FONT.render(self.name, True, WHITE)
        cost_text = FONT.render(f"{self.cost}/{self.power}", True, WHITE)
        surface.blit(name_text, (x + 5, y + 5))
        surface.blit(cost_text, (x + 5, y + 25))
        if self.rested:
            pygame.draw.line(surface, WHITE, self.rect.topleft, self.rect.bottomright, 2)

class Player:
    def __init__(self, name, bottom=True):
        self.name = name
        self.hand = [Card(f"C{i+1}", cost=2+i%3, power=3000+i*500) for i in range(5)]
        self.board = []
        self.life = 5
        self.bottom = bottom

    def draw_hand(self, surface):
        y = HEIGHT - CARD_HEIGHT - 10 if self.bottom else 10
        for i, card in enumerate(self.hand):
            x = 100 + i * (CARD_WIDTH + 10)
            card.draw(surface, x, y)

    def draw_board(self, surface):
        y = HEIGHT // 2 + 80 if self.bottom else HEIGHT // 2 - CARD_HEIGHT - 80
        for i, card in enumerate(self.board):
            x = 150 + i * (CARD_WIDTH + 10)
            card.draw(surface, x, y)

    def draw_life(self, surface):
        x = WIDTH - 90
        y = HEIGHT - 150 if self.bottom else 50
        pygame.draw.rect(surface, RED, (x, y, 60, 30))
        text = FONT.render(f"Vida: {self.life}", True, WHITE)
        surface.blit(text, (x + 5, y + 5))

# Crear jugadores
player1 = Player("Jugador 1", bottom=True)
player2 = Player("Jugador 2", bottom=False)

# Simular que ambos tienen 3 cartas en campo
for _ in range(3):
    player1.board.append(player1.hand.pop(0))
    player2.board.append(player2.hand.pop(0))

fase_actual = "MAIN PHASE"

# Bucle principal
running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujar texto de fase
    pygame.draw.rect(screen, BLACK, (0, HEIGHT // 2 - 20, WIDTH, 40))
    phase_text = FONT.render(f"Fase actual: {fase_actual}", True, WHITE)
    screen.blit(phase_text, (WIDTH // 2 - 60, HEIGHT // 2 - 10))

    # Dibujar mano, tablero y vida
    player1.draw_hand(screen)
    player1.draw_board(screen)
    player1.draw_life(screen)

    player2.draw_hand(screen)
    player2.draw_board(screen)
    player2.draw_life(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

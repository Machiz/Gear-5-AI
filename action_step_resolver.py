import pygame
import struct
from dataclasses import dataclass

@dataclass
class ActionStepResolver:
    iActorID: int
    iActionIdx: int
    iStepIdx: int

    def to_bytes(self) -> bytes:
        return struct.pack('iii', self.iActorID, self.iActionIdx, self.iStepIdx)

    @classmethod
    def from_bytes(cls, data: bytes):
        iActorID, iActionIdx, iStepIdx = struct.unpack('iii', data)
        return cls(iActorID, iActionIdx, iStepIdx)


# --------- Ejemplo de uso en un loop de Pygame ---------

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

resolver = ActionStepResolver(1, 0, 0)

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Simulamos una acción: al presionar espacio, cambia el índice de acción
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                resolver.iActionIdx += 1
                print("Acción actual:", resolver)

                # Simulamos enviar datos por red
                data_bytes = resolver.to_bytes()
                print("Bytes enviados:", data_bytes)

                # Simulamos recibir los datos y reconstruir el objeto
                nuevo_resolver = ActionStepResolver.from_bytes(data_bytes)
                print("Reconstruido desde red:", nuevo_resolver)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

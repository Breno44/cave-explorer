import pygame
from code.settings import C_YELLOW, C_ORANGE
from code.sprite_loader import load_image


class Coin:
    SIZE  = 14
    VALUE = 100

    def __init__(self, x, y):
        self.rect  = pygame.Rect(x - self.SIZE // 2, y - self.SIZE // 2,
                                 self.SIZE, self.SIZE)
        self.frame = 0
        self.image = load_image("asset/coin.png",
                                (self.SIZE, self.SIZE),
                                C_YELLOW)
        self._use_sprite = self.image.get_at((0, 0))[3] < 255

    def update(self):
        self.frame += 1

    def draw(self, surface):
        if self._use_sprite:
            surface.blit(self.image, self.rect)
        else:
            # fallback animado
            color = C_YELLOW if (self.frame // 20) % 2 == 0 else C_ORANGE
            pygame.draw.ellipse(surface, color, self.rect)
            pygame.draw.ellipse(surface, C_ORANGE, self.rect, 2)

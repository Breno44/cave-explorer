import pygame
from code.settings import PLATFORM_COLOR
from code.sprite_loader import load_tile

TILE_SIZE = 18  # tamanho de cada tile em pixels


class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.tile = load_tile("asset/platform_tile.png",
                              (TILE_SIZE, height),
                              PLATFORM_COLOR)

    def draw(self, surface):
        # Desenha o tile repetido da esquerda para a direita (tiling)
        x = self.rect.x
        while x < self.rect.right:
            # O último tile pode ser cortado — clip garante que não vaze
            clip_w = min(TILE_SIZE, self.rect.right - x)
            tile_clip = self.tile.subsurface((0, 0, clip_w, self.rect.height))
            surface.blit(tile_clip, (x, self.rect.y))
            x += TILE_SIZE

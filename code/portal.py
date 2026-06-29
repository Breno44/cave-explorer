import pygame
from code.settings import C_GREEN, C_WHITE
from code.sprite_loader import load_image


class Portal:
    WIDTH  = 30
    HEIGHT = 50

    def __init__(self, x, y):
        self.rect  = pygame.Rect(x - self.WIDTH // 2, y - self.HEIGHT,
                                 self.WIDTH, self.HEIGHT)
        self.frame = 0
        self.image = load_image("asset/portal.png",
                                (self.WIDTH, self.HEIGHT),
                                C_GREEN)
        self._use_sprite = self.image.get_at((0, 0))[3] < 255

    def update(self):
        self.frame += 1

    def draw(self, surface):
        if self._use_sprite:
            surface.blit(self.image, self.rect)
        else:
            # fallback pulsante
            pulse     = 4 if (self.frame // 20) % 2 == 0 else 0
            draw_rect = self.rect.inflate(pulse, pulse)
            pygame.draw.rect(surface, C_GREEN, draw_rect, border_radius=6)
            pygame.draw.rect(surface, C_WHITE, draw_rect, 2, border_radius=6)

        font  = pygame.font.SysFont("Arial", 12)
        label = font.render("SAÍDA", True, C_WHITE)
        surface.blit(label, (self.rect.centerx - label.get_width() // 2,
                             self.rect.top - 18))

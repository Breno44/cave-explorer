import pygame
from code.settings import ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED, ENEMY_COLOR, C_WHITE
from code.sprite_loader import load_image


class Enemy:
    def __init__(self, x, y, patrol_left, patrol_right):
        self.rect         = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.patrol_left  = patrol_left
        self.patrol_right = patrol_right
        self.direction    = 1

        self.image_right = load_image("asset/enemy.png",
                                      (ENEMY_WIDTH, ENEMY_HEIGHT),
                                      ENEMY_COLOR)
        self.image_left  = pygame.transform.flip(self.image_right, True, False)

    def update(self):
        self.rect.x += ENEMY_SPEED * self.direction

        if self.rect.right >= self.patrol_right:
            self.rect.right = self.patrol_right
            self.direction  = -1

        if self.rect.left <= self.patrol_left:
            self.rect.left = self.patrol_left
            self.direction = 1

    def draw(self, surface):
        image = self.image_right if self.direction == 1 else self.image_left
        surface.blit(image, self.rect)

        # Olhinho (fica visível apenas no fallback colorido)
        if self.image_right.get_at((0, 0))[3] == 255:
            eye_y = self.rect.top + 8
            ex    = self.rect.right - 12 if self.direction == 1 else self.rect.left + 6
            pygame.draw.rect(surface, C_WHITE, (ex, eye_y, 6, 6))

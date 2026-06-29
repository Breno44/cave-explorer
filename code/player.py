import pygame
from code.settings import (PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR,
                           PLAYER_SPEED, GRAVITY, JUMP_FORCE,
                           WIN_WIDTH, WIN_HEIGHT, PLAYER_LIVES, C_YELLOW)
from code.sprite_loader import load_image


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)

        self.vel_y       = 0
        self.on_ground   = False
        self.facing_right = True   # controla a direção do sprite

        self.lives = PLAYER_LIVES
        self.score = 0

        self.invincible          = False
        self.invincible_timer    = 0
        self.INVINCIBLE_DURATION = 120

        # Carrega sprite (fallback = retângulo azul)
        self.image_right = load_image("asset/player.png",
                                      (PLAYER_WIDTH, PLAYER_HEIGHT),
                                      PLAYER_COLOR)
        # Versão espelhada (olhando para a esquerda)
        self.image_left  = pygame.transform.flip(self.image_right, True, False)

    def take_damage(self):
        if self.invincible:
            return
        self.lives -= 1
        self.invincible       = True
        self.invincible_timer = self.INVINCIBLE_DURATION

    def update(self, platforms):
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        keys = pygame.key.get_pressed()

        # ── PASSO 1: horizontal ────────────────────────────────────────
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED
            self.facing_right = True

        self.rect.x += dx

        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if dx > 0:
                    self.rect.right = plat.rect.left
                elif dx < 0:
                    self.rect.left  = plat.rect.right

        self.rect.x = max(0, min(self.rect.x, WIN_WIDTH - self.rect.width))

        # ── PASSO 2: pulo ─────────────────────────────────────────────
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y     = JUMP_FORCE
            self.on_ground = False

        # ── PASSO 3: gravidade e vertical ─────────────────────────────
        self.vel_y  += GRAVITY
        self.rect.y += self.vel_y

        self.on_ground = False

        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0:
                    self.rect.bottom = plat.rect.top
                    self.vel_y       = 0
                    self.on_ground   = True
                elif self.vel_y < 0:
                    self.rect.top = plat.rect.bottom
                    self.vel_y    = 0

        if self.rect.bottom >= WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT
            self.vel_y       = 0
            self.on_ground   = True

    def draw(self, surface):
        # Pisca durante a invencibilidade
        if self.invincible and self.invincible_timer % 6 < 3:
            return

        image = self.image_right if self.facing_right else self.image_left
        surface.blit(image, self.rect)

        # Borda amarela no ar (só no modo retângulo — some com sprite real)
        if not self.on_ground and self.image_right.get_at((0, 0))[3] == 255:
            pygame.draw.rect(surface, C_YELLOW, self.rect, 2)

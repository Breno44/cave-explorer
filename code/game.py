import sys
import pygame
from code.settings   import WIN_WIDTH, WIN_HEIGHT, FPS, TITLE, C_WHITE, C_RED, C_GREEN, C_YELLOW
from code.player     import Player
from code.platform   import Platform
from code.enemy      import Enemy
from code.coin       import Coin
from code.portal     import Portal
from code.menu       import Menu
from code.background import Background


def create_platforms():
    return [
        Platform(0,   WIN_HEIGHT - 40, WIN_WIDTH, 40),   # chão
        Platform(100, 360, 160, 18),
        Platform(350, 290, 140, 18),
        Platform(560, 220, 160, 18),
        Platform(200, 180, 120, 18),
        Platform(480, 140, 100, 18),                      # plataforma mais alta
    ]


def create_enemies():
    return [
        Enemy(150, WIN_HEIGHT - 40 - 32,  50,  400),
        Enemy(370, 290 - 32,             350,  490),
        Enemy(580, 220 - 32,             560,  720),
    ]


def create_coins():
    return [
        # chão
        Coin(250, WIN_HEIGHT - 40 - 10),
        Coin(320, WIN_HEIGHT - 40 - 10),
        Coin(500, WIN_HEIGHT - 40 - 10),
        # plataformas — recompensa a exploração
        Coin(180, 360 - 10),
        Coin(420, 290 - 10),
        Coin(640, 220 - 10),
        Coin(260, 180 - 10),
        Coin(530, 140 - 10),
    ]


class Game:
    def __init__(self):
        pygame.init()
        self.window   = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock    = pygame.time.Clock()
        self.font_hud = pygame.font.SysFont("Arial", 20)
        self.font_big = pygame.font.SysFont("Arial", 64, bold=True)

    def _reset(self):
        self.background = Background()
        self.platforms  = create_platforms()
        self.enemies    = create_enemies()
        self.coins      = create_coins()
        self.portal     = Portal(x=530, y=140)
        self.player     = Player(x=60, y=WIN_HEIGHT - 40 - 48)
        self.game_over  = False
        self.victory    = False

    def run(self):
        while True:
            menu   = Menu(self.window)
            choice = menu.run()
            if choice == "NOVO JOGO":
                self._reset()
                self._play()
            elif choice == "SAIR":
                pygame.quit()
                sys.exit()

    # ── Loop da partida ────────────────────────────────────────────────
    def _play(self):
        while True:
            # --- 1. Eventos ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    if self.game_over or self.victory:
                        return  # volta ao menu

            # --- 2. Atualizar ---
            if not self.game_over and not self.victory:
                self.player.update(self.platforms)

                for enemy in self.enemies:
                    enemy.update()

                for coin in self.coins:
                    coin.update()

                self.portal.update()
                self._check_collisions()

            # --- 3. Desenhar ---
            self.background.draw(self.window)

            for plat in self.platforms:
                plat.draw(self.window)
            for enemy in self.enemies:
                enemy.draw(self.window)
            for coin in self.coins:
                coin.draw(self.window)

            self.portal.draw(self.window)
            self.player.draw(self.window)
            self._draw_hud()

            if self.game_over:
                self._draw_overlay("GAME OVER", C_RED,
                                   f"Score final: {self.player.score}")
            if self.victory:
                self._draw_overlay("VOCÊ VENCEU!", C_GREEN,
                                   f"Score final: {self.player.score}")

            pygame.display.flip()
            self.clock.tick(FPS)

    def _check_collisions(self):
        # Inimigos → dano
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage()
                if self.player.lives <= 0:
                    self.game_over = True

        # Moedas → coleta (list comprehension filtra as não-coletadas)
        coletadas = [c for c in self.coins if self.player.rect.colliderect(c.rect)]
        for c in coletadas:
            self.player.score += Coin.VALUE
        self.coins = [c for c in self.coins if c not in coletadas]

        # Portal → vitória
        if self.player.rect.colliderect(self.portal.rect):
            self.victory = True

    def _draw_hud(self):
        coracoes = "♥ " * self.player.lives + "♡ " * (3 - self.player.lives)
        moedas   = f"  💰 {self.player.score}"
        texto    = f"{coracoes}{moedas}     [← →] mover  [SPACE] pular"
        self.window.blit(self.font_hud.render(texto, True, C_WHITE), (10, 10))

    def _draw_overlay(self, titulo: str, cor_titulo, subtitulo: str):
        overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.window.blit(overlay, (0, 0))

        msg = self.font_big.render(titulo, True, cor_titulo)
        sub = self.font_hud.render(subtitulo, True, C_WHITE)
        hin = self.font_hud.render("Pressione R para voltar ao menu", True, C_YELLOW)

        cy = WIN_HEIGHT // 2
        self.window.blit(msg, (WIN_WIDTH // 2 - msg.get_width() // 2, cy - 70))
        self.window.blit(sub, (WIN_WIDTH // 2 - sub.get_width() // 2, cy + 10))
        self.window.blit(hin, (WIN_WIDTH // 2 - hin.get_width() // 2, cy + 40))

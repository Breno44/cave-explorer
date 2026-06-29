import sys
import pygame
from code.settings import WIN_WIDTH, WIN_HEIGHT, FPS, C_SKY, C_WHITE, C_YELLOW, C_ORANGE, C_GRAY


class Menu:
    def __init__(self, window):
        self.window = window
        self.clock  = pygame.time.Clock()

        self.font_title   = pygame.font.SysFont("Arial", 72, bold=True)
        self.font_option  = pygame.font.SysFont("Arial", 36)
        self.font_control = pygame.font.SysFont("Arial", 20)

        self.options = ["NOVO JOGO", "SAIR"]
        self.selected = 0   # índice da opção atualmente selecionada

    def run(self):
        """Loop do menu. Retorna a string da opção escolhida."""
        while True:
            # ── Eventos ───────────────────────────────────────────────
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # move seleção para cima (com wrap-around)
                        self.selected = (self.selected - 1) % len(self.options)

                    elif event.key == pygame.K_DOWN:
                        # move seleção para baixo (com wrap-around)
                        self.selected = (self.selected + 1) % len(self.options)

                    elif event.key == pygame.K_RETURN:
                        return self.options[self.selected]  # sai do loop

            # ── Desenho ───────────────────────────────────────────────
            self.window.fill(C_SKY)
            self._draw_cave_decoration()
            self._draw_title()
            self._draw_options()
            self._draw_controls()

            pygame.display.flip()
            self.clock.tick(FPS)

    def _draw_title(self):
        title = self.font_title.render("CAVE EXPLORER", True, C_ORANGE)
        x = WIN_WIDTH // 2 - title.get_width() // 2
        self.window.blit(title, (x, 80))

        # subtítulo
        sub = self.font_control.render("Um explorador em busca do tesouro perdido", True, C_GRAY)
        self.window.blit(sub, (WIN_WIDTH // 2 - sub.get_width() // 2, 160))

    def _draw_options(self):
        start_y = 230
        for i, option in enumerate(self.options):
            if i == self.selected:
                # opção selecionada: amarelo com seta
                color = C_YELLOW
                prefix = "► "
            else:
                color = C_WHITE
                prefix = "  "

            text = self.font_option.render(prefix + option, True, color)
            x = WIN_WIDTH // 2 - text.get_width() // 2
            self.window.blit(text, (x, start_y + i * 55))

        hint = self.font_control.render("↑ ↓ navegar   ENTER confirmar", True, C_GRAY)
        self.window.blit(hint, (WIN_WIDTH // 2 - hint.get_width() // 2, 350))

    def _draw_controls(self):
        """Exibe os controles do jogo — requisito obrigatório do trabalho."""
        # Linha separadora
        pygame.draw.line(self.window, C_GRAY, (60, 400), (WIN_WIDTH - 60, 400), 1)

        titulo = self.font_control.render("CONTROLES DO JOGO", True, C_ORANGE)
        self.window.blit(titulo, (WIN_WIDTH // 2 - titulo.get_width() // 2, 410))

        controles = [
            ("← →",   "Mover o explorador"),
            ("SPACE",  "Pular"),
            ("R",      "Reiniciar após Game Over"),
        ]
        col_x = [WIN_WIDTH // 2 - 160, WIN_WIDTH // 2 - 60]
        y = 435
        for tecla, acao in controles:
            t_key  = self.font_control.render(tecla, True, C_YELLOW)
            t_acao = self.font_control.render(acao,  True, C_WHITE)
            self.window.blit(t_key,  (col_x[0], y))
            self.window.blit(t_acao, (col_x[1], y))
            y += 22

    def _draw_cave_decoration(self):
        """Estalactites simples para dar cara de caverna."""
        stalactites = [
            (80,  0, 14, 50),
            (200, 0, 10, 35),
            (380, 0, 16, 60),
            (540, 0, 12, 45),
            (700, 0, 18, 55),
        ]
        for x, y, w, h in stalactites:
            points = [(x, y), (x + w, y), (x + w // 2, y + h)]
            pygame.draw.polygon(self.window, C_GRAY, points)

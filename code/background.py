import pygame
from code.settings import WIN_WIDTH, WIN_HEIGHT, C_SKY


class Background:
    def __init__(self):
        self.layers = self._load_layers()

    def _load_layers(self):
        """
        Tenta carregar as 4 camadas de parallax (bg_L1..L4).
        Cada camada é escalada para preencher a janela.
        A área branca das imagens PNG é tratada como transparente (colorkey).
        """
        layers = []
        all_found = True

        for i in range(1, 5):
            try:
                img = pygame.image.load(f"asset/bg_L{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (WIN_WIDTH, WIN_HEIGHT))
                layers.append(img)
            except FileNotFoundError:
                all_found = False
                break

        if not all_found:
            layers = [self._draw_cave_fallback()]

        return layers

    def _draw_cave_fallback(self):
        """Fundo de caverna gerado em código, usado quando os PNGs não existem."""
        surf = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))

        # Gradiente vertical escuro
        for y in range(WIN_HEIGHT):
            t = y / WIN_HEIGHT
            r = int(30 + t * 10)
            g = int(30 + t * 10)
            b = int(60 + t * 15)
            pygame.draw.line(surf, (r, g, b), (0, y), (WIN_WIDTH, y))

        # Estalactites (teto)
        for x, h in [(60,70),(160,50),(280,80),(400,45),(520,65),(640,55),(740,75)]:
            pygame.draw.polygon(surf, (50, 50, 70), [(x-10,0),(x+10,0),(x,h)])

        # Estalagmites (chão)
        floor = WIN_HEIGHT - 40
        for x, h in [(120,30),(250,45),(450,35),(600,50),(720,40)]:
            pygame.draw.polygon(surf, (45, 45, 65), [(x-8,floor),(x+8,floor),(x,floor-h)])

        return surf

    def draw(self, surface):
        for layer in self.layers:
            surface.blit(layer, (0, 0))

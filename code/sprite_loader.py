import pygame


def load_image(path: str, size: tuple, fallback_color: tuple) -> pygame.Surface:
    """
    Tenta carregar uma imagem PNG. Se não encontrar o arquivo,
    retorna um retângulo colorido do mesmo tamanho — o jogo nunca quebra.
    """
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except FileNotFoundError:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf


def load_tile(path: str, tile_size: tuple, fallback_color: tuple) -> pygame.Surface:
    """Carrega um tile para ser repetido em plataformas."""
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, tile_size)
    except FileNotFoundError:
        surf = pygame.Surface(tile_size)
        surf.fill(fallback_color)
        # Borda levemente mais escura para dar textura visual mesmo sem sprite
        darker = tuple(max(0, c - 40) for c in fallback_color)
        pygame.draw.rect(surf, darker, surf.get_rect(), 2)
        return surf

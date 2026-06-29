import pygame

# Tamanho da janela
WIN_WIDTH = 800
WIN_HEIGHT = 500
FPS = 60
TITLE = "Cave Explorer"

# Cores (R, G, B) — valores de 0 a 255
C_BLACK  = (0,   0,   0)
C_WHITE  = (255, 255, 255)
C_RED    = (220, 50,  50)
C_GREEN  = (50,  180, 50)
C_BLUE   = (50,  100, 220)
C_YELLOW = (255, 220, 0)
C_GRAY   = (120, 120, 120)
C_BROWN  = (139, 90,  43)
C_ORANGE = (255, 140, 0)
C_SKY    = (30,  30,  60)   # fundo da caverna

# Física do jogador
GRAVITY       = 0.5   # aceleração de queda por frame
JUMP_FORCE    = -12   # velocidade inicial do pulo (negativo = sobe)
PLAYER_SPEED  = 3     # pixels por frame na horizontal

# Jogador
PLAYER_WIDTH  = 48
PLAYER_HEIGHT = 48
PLAYER_LIVES  = 3
PLAYER_COLOR  = C_BLUE

# Inimigo
ENEMY_WIDTH   = 32
ENEMY_HEIGHT  = 32
ENEMY_SPEED   = 1
ENEMY_COLOR   = C_RED

# Plataforma
PLATFORM_COLOR = C_BROWN
GROUND_COLOR   = C_GRAY

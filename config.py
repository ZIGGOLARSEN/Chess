import pygame

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720
BLOCK_SIZE = int(WINDOW_WIDTH/8)
BORDER_SIZE = 10

WHITE = (255, 229, 204)
BLACK = (72, 114, 54)
BLUE = (0, 128, 255)
RED = (204, 0, 0)


# WHITES
WHITE_PAWN = pygame.image.load(r'C:\Users\Maka Jukhvashvili\Desktop\Python\Python code\Python Projects\chess\images\white_pawn.png')
WHITE_ROOK = pygame.image.load(r'C:\Users\Maka Jukhvashvili\Desktop\Python\Python code\Python Projects\chess\images\white_rook.png')
WHITE_KNIGHT = pygame.image.load(r'C:\Users\Maka Jukhvashvili\Desktop\Python\Python code\Python Projects\chess\images\white_knight.png')
WHITE_BISHOP = pygame.image.load(r'C:\Users\Maka Jukhvashvili\Desktop\Python\Python code\Python Projects\chess\images\white_bishop.png')
WHITE_QUEEN = pygame.image.load(r'C:\Users\Maka Jukhvashvili\Desktop\Python\Python code\Python Projects\chess\images\white_queen.png')
WHITE_KING = pygame.image.load(r'C:\Users\Maka Jukhvashvili\Desktop\Python\Python code\Python Projects\chess\images\white_king.png')
# BLACKS
BLACK_PAWN = pygame.image.load(r'C:\Users\Maka Jukhvashvili\Desktop\Python\Python code\Python Projects\chess\images\black_pawn.png')
BLACK_ROOK = pygame.image.load(r'C:\Users\Maka Jukhvashvili\Desktop\Python\Python code\Python Projects\chess\images\black_rook.png')
BLACK_KNIGHT = pygame.image.load(r'C:\Users\Maka Jukhvashvili\Desktop\Python\Python code\Python Projects\chess\images\black_knight.png')
BLACK_BISHOP = pygame.image.load(r'C:\Users\Maka Jukhvashvili\Desktop\Python\Python code\Python Projects\chess\images\black_bishop.png')
BLACK_QUEEN = pygame.image.load(r'C:\Users\Maka Jukhvashvili\Desktop\Python\Python code\Python Projects\chess\images\black_queen.png')
BLACK_KING = pygame.image.load(r'C:\Users\Maka Jukhvashvili\Desktop\Python\Python code\Python Projects\chess\images\black_king.png')

STARTING_POSITION_WHITE = 'r07,k17,b27,q37,K47,b57,k67,r77,p06,p16,p26,p36,p46,p56,p66,p76'
STARTING_POSITION_BLACK = 'r00,k10,b20,q30,K40,b50,k60,r70,p01,p11,p21,p31,p41,p51,p61,p71'

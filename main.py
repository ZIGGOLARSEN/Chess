from Board import Board
from config import *

class Screen:
    screen, taken_piece = None, None
    running, checkmate, draw = False, False, False
    board = Board()

    def __init__(self):
        pygame.init()
        self.initialize()

    def initialize(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Chess')
        pygame.display.set_icon(BLACK_KING)
        self.render()



    def handle_click_events(self):
        x, y = pygame.mouse.get_pos()
        pos_x, pos_y = x // BLOCK_SIZE, y // BLOCK_SIZE

        if self.taken_piece:
            self.place_piece(pos_x, pos_y)
        else:
            self.take_piece(pos_x, pos_y)

    def take_piece(self, pos_x, pos_y):
        piece = self.board.board[pos_y, pos_x]

        if piece == 0: return
        if piece.type_of_piece != self.board.current_player: return

        self.taken_piece = piece
        self.board.board[pos_y, pos_x] = 0

        self.board.positions = self.taken_piece.generate_positions(self.board.board)[0]

        self.board.castling(self.taken_piece)

        self.board.handle_check(self.taken_piece)

    def place_piece(self, pos_x, pos_y):
        if self.taken_piece.x == pos_x and self.taken_piece.y == pos_y:
            self.board.board[pos_y, pos_x] = self.taken_piece
            self.taken_piece = None
            self.board.positions = []
            return

        if (pos_y, pos_x) not in self.board.positions: return

        self.taken_piece.x = pos_x
        self.taken_piece.y = pos_y

        # handling castling
        if (pos_y, pos_x) in self.board.castling_positions:
            try:
                rook = self.board.board[pos_y, pos_x + 1]
                rook.x = rook.x - 2
                self.board.board[pos_y, pos_x - 1] = rook
                self.board.board[pos_y, pos_x + 1] = 0
            except AttributeError:
                rook = self.board.board[pos_y, pos_x - 1]
                self.board.board[pos_y, pos_x + 1] = rook
                self.board.board[pos_y, pos_x - 1] = 0
                rook.x = rook.x + 2
            finally:
                self.board.castling_positions = []
                if self.taken_piece.type_of_piece == 'white':
                    self.board.castled_white = True
                else:
                    self.board.castled_white = True

        if self.taken_piece.__class__.__name__ == 'King' or self.taken_piece.__class__.__name__ == "Rook":
            if self.taken_piece.type_of_piece == 'white':
                self.board.can_castle_white = False
            else:
                self.board.can_castle_black = False

        # handling pawn promotion
        if self.taken_piece.__class__.__name__ == 'Pawn':
            if self.taken_piece.check_promotion():
                self.taken_piece = self.board.pawn_promotion(self.taken_piece)


        self.board.board[pos_y, pos_x] = self.taken_piece
        self.taken_piece = None

        self.board.positions = []
        self.board.change_player()

        if self.board.is_checkmate():
            self.checkmate = True

        if self.board.is_draw():
            self.draw = True




    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
            for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
                idx, jdx = x/BLOCK_SIZE, y/BLOCK_SIZE
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)

                if (idx+jdx) % 2 == 0:
                    pygame.draw.rect(self.screen, WHITE, rect, int(BLOCK_SIZE/2))
                else:
                    pygame.draw.rect(self.screen, BLACK, rect, int(BLOCK_SIZE/2))

    def draw_pieces(self):
        for row in self.board.board:
            for piece in row:
                if piece != 0:
                    pos_x = piece.x*BLOCK_SIZE
                    pos_y = piece.y*BLOCK_SIZE
                    self.screen.blit(piece.image, (pos_x, pos_y))

    def draw_positions(self):
        for position in self.board.positions:
            rect = pygame.Rect(position[1]*BLOCK_SIZE, position[0]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)

            if self.board.board[position] != 0:
                pygame.draw.rect(self.screen, RED, rect, BORDER_SIZE)
            else:
                pygame.draw.rect(self.screen, BLUE, rect, BORDER_SIZE)

    def draw_text(self, text):
        font = pygame.font.SysFont('consolas', 70)
        text_surface = font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface,
                         ((WINDOW_WIDTH-text_surface.get_width())/2, (WINDOW_HEIGHT-text_surface.get_height())/2))

    def handle_checkmate(self):
        self.draw_text('CHECKMATE')

    def handle_draw(self):
        self.draw_text('DRAW')


    def update(self):
        self.draw_grid()
        self.draw_pieces()
        self.draw_positions()

        if self.checkmate:
            self.handle_checkmate()
        if self.draw:
            self.handle_draw()

        pygame.display.update()

    def render(self):
        self.running = True
        self.update()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    if not (self.checkmate or self.draw):
                        self.handle_click_events()
                        self.update()

Screen()

from pieces.Piece import ShortRangePiece
from config import *

class Pawn(ShortRangePiece):
    first_move = True

    def __init__(self, type_of_piece, x, y):
        super().__init__(type_of_piece, x, y)
        self.assign_image()

    def assign_image(self):
        if self.type_of_piece == 'white':
            self.image = WHITE_PAWN
        else:
            self.image = BLACK_PAWN

    def generate_positions(self, board):
        delta_y = 1

        self.check_first_move()

        positions = []
        attacked_positions = []
        for y in range(1, delta_y+1):
            if self.type_of_piece == 'white': y *= -1

            if self.y + y >= 8 or self.y + y < 0: return [], []

            if board[self.y+y, self.x] == 0:
                positions.append((self.y+y, self.x))

            if self.x - 1 >= 0:
                if not(board[self.y+y, self.x-1] == 0 or board[self.y+y, self.x-1].type_of_piece == self.type_of_piece):
                    positions.append((self.y+y, self.x-1))
                    attacked_positions.append((self.y+y, self.x-1))
                else:
                    attacked_positions.append((self.y+y, self.x-1))

            if self.x + 1 < 8:
                if not(board[self.y+y, self.x+1] == 0 or board[self.y+y, self.x+1].type_of_piece == self.type_of_piece):
                    positions.append((self.y+y, self.x+1))
                    attacked_positions.append((self.y+y, self.x+1))
                else:
                    attacked_positions.append((self.y+y, self.x+1))

        if self.first_move:
            if self.type_of_piece == 'white' and board[self.y-1, self.x] == 0 and board[self.y-2, self.x] == 0:
                positions.append((self.y-2, self.x))

            if self.type_of_piece == 'black' and board[self.y+1, self.x] == 0 and board[self.y+2, self.x] == 0:
                positions.append((self.y+2, self.x))

        return positions, attacked_positions

    def check_first_move(self):
        if self.type_of_piece == 'white' and self.y != 6:
            self.first_move = False
        if self.type_of_piece == 'black' and self.y != 1:
            self.first_move = False

    def check_promotion(self):
        if self.y == 0 or self.y == 7: return True

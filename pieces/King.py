from pieces.Piece import ShortRangePiece
from config import *

class King(ShortRangePiece):
    def __init__(self, type_of_piece, x, y):
        super().__init__(type_of_piece, x, y)
        self.assign_image()

    def assign_image(self):
        if self.type_of_piece == 'white':
            self.image = WHITE_KING
        else:
            self.image = BLACK_KING

    def generate_positions(self, board):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]

        positions = []
        attacked_positions = []
        for direction in directions:
            x, y = direction

            if self.y + y >= 8 or self.y + y < 0 or self.x + x >= 8 or self.x + x < 0: continue

            if board[self.y + y, self.x + x] != 0:
                if board[self.y + y, self.x + x].type_of_piece == self.type_of_piece:
                    attacked_positions.append((self.y + y, self.x + x))
                    continue

            positions.append((self.y + y, self.x + x))

        return positions, attacked_positions

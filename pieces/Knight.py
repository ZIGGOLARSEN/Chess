from pieces.Piece import Piece
from config import *

class Knight(Piece):
    def __init__(self, type_of_piece, x, y):
        super().__init__(type_of_piece, x, y)
        self.assign_image()

    def assign_image(self):
        if self.type_of_piece == 'white':
            self.image = WHITE_KNIGHT
        else:
            self.image = BLACK_KNIGHT

    def generate_positions(self, board):
        directions = [(1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2)]

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

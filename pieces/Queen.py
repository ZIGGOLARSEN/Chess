from pieces.Piece import LongRangePiece
from config import *

class Queen(LongRangePiece):
    def __init__(self, type_of_piece, x, y):
        super().__init__(type_of_piece, x, y)
        self.assign_image()

    def assign_image(self):
        if self.type_of_piece == 'white':
            self.image = WHITE_QUEEN
        else:
            self.image = BLACK_QUEEN

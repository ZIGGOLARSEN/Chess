class Piece:
    image = None

    def __init__(self, type_of_piece, x, y):
        self.type_of_piece = type_of_piece
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{self.__class__.__name__}({self.type_of_piece}, x={self.x}, y={self.y})'

    def assign_image(self):
        pass

    def generate_positions(self, board):
        pass


class ShortRangePiece(Piece):
    def __init__(self, type_of_piece, x, y):
        super().__init__(type_of_piece, x, y)


class LongRangePiece(Piece):
    def __init__(self, type_of_piece, x, y):
        super().__init__(type_of_piece, x, y)

    def generate_positions(self, board):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]

        positions = []
        attacked_positions = []
        if self.__class__.__name__ == 'Rook': directions = directions[:4]
        if self.__class__.__name__ == 'Bishop': directions = directions[4:]

        for direction in directions:
            for i in range(1, 9):
                x, y = direction[0] * i, direction[1] * i

                if self.y + y >= 8 or self.y + y < 0 or self.x + x >= 8 or self.x + x < 0: continue

                if board[self.y + y, self.x + x] != 0:
                    if board[self.y + y, self.x + x].type_of_piece == self.type_of_piece:
                        attacked_positions.append((self.y + y, self.x + x))
                        break

                    if board[self.y + y, self.x + x].type_of_piece != self.type_of_piece:
                        positions.append((self.y + y, self.x + x))
                        break

                positions.append((self.y + y, self.x + x))

        return positions, attacked_positions

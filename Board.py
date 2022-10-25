import itertools
import numpy as np
from config import *

from pieces.Piece import Piece
from pieces.Pawn import Pawn
from pieces.Rook import Rook
from pieces.Knight import Knight
from pieces.Bishop import Bishop
from pieces.Queen import Queen
from pieces.King import King


class Board:
    positions, castling_positions = [], []
    current_player = 'white'
    pieces_dict = {'p': Pawn, 'r': Rook, 'k': Knight, 'b': Bishop, 'q': Queen, 'K': King}
    draw, castled_white, castled_black = False, False, False
    can_castle_white, can_castle_black = True, True

    def __init__(self):
        self.board = np.zeros((8, 8)).astype(Piece)
        self.starting_position()

    def change_player(self):
        if self.current_player == 'white':
            self.current_player = 'black'
        else:
            self.current_player = 'white'

    def starting_position(self, start_white=STARTING_POSITION_WHITE, start_black=STARTING_POSITION_BLACK):
        whites = start_white.split(',')
        blacks = start_black.split(',')

        for piece in whites:
            x, y = piece[1:]
            piece_type = self.pieces_dict[piece[0]]('white', int(x), int(y))
            self.board[int(y), int(x)] = piece_type

        for piece in blacks:
            x, y = piece[1:]
            piece_type = self.pieces_dict[piece[0]]('black', int(x), int(y))
            self.board[int(y), int(x)] = piece_type

    def pawn_promotion(self, pawn):
        new_piece_name = input('type in initials for new piece')
        new_piece = self.pieces_dict.get(new_piece_name)
        return new_piece(pawn.type_of_piece, pawn.x, pawn.y)

    def castling(self, taken_piece):
        if taken_piece.type_of_piece == 'white' and not self.can_castle_white: return
        if taken_piece.type_of_piece == 'black' and not self.can_castle_black: return

        if taken_piece.__class__.__name__ != 'King' and taken_piece.__class__.__name__ != 'Rook': return

        if taken_piece.type_of_piece == 'white' and self.castled_white: return
        if taken_piece.type_of_piece == 'black' and self.castled_black: return


        if taken_piece.__class__.__name__ == 'King':
            try:
                if self.board[taken_piece.y, taken_piece.x + 2] == 0 and self.board[taken_piece.y, taken_piece.x + 1] == 0:
                    if self.board[taken_piece.y, taken_piece.x + 3].__class__.__name__ == "Rook":
                        self.positions.append((taken_piece.y, taken_piece.x + 2))
                        self.castling_positions.append((taken_piece.y, taken_piece.x + 2))

                if self.board[taken_piece.y, taken_piece.x - 3] == 0 and self.board[taken_piece.y, taken_piece.x - 2] == 0 \
                        and self.board[taken_piece.y, taken_piece.x - 1] == 0:
                    if self.board[taken_piece.y, taken_piece.x - 4].__class__.__name__ == "Rook":
                        self.positions.append((taken_piece.y, taken_piece.x - 3))
                        self.castling_positions.append((taken_piece.y, taken_piece.x - 3))
            except IndexError:
                return


    def get_allies(self):
        allies = []
        for piece in self.board.flatten():
            if piece == 0: continue
            if piece.type_of_piece != self.current_player: continue
            allies.append(piece)
        return allies

    def get_allied_king(self):
        for piece in self.get_allies():
            if piece.__class__.__name__ != 'King': continue
            return piece

    def get_enemies(self):
        enemies = []
        for square in self.board.flatten():
            if square == 0: continue
            if square.type_of_piece == self.current_player: continue
            enemies.append(square)
        return enemies

    def is_check(self):
        attacked_positions = self.generate_enemy_positions()[0]
        attacked_positions = list(itertools.chain.from_iterable(attacked_positions))

        king = self.get_allied_king()
        if (king.y, king.x) in attacked_positions: return True

        return False



    def generate_enemy_positions(self):
        """
        Generates all enemies and positions which they can attack

        :return: tuple of lists -> (attacked positions, enemies): all positions which enemy can attack and enemies itself
        """
        enemies = self.get_enemies()

        attacked_positions = []
        for enemy in enemies:
            positions, attackable_positions = enemy.generate_positions(self.board)

            # here we divide pieces into pawns and not pawns, because pawns moving positions and attacking positions
            # are different.On pawns generate_positions function returns two arrays: moving positions and
            # positions on which they can attack (diagonals). On other pieces generate_positions function also returns
            # two arrays: moving positions which include attacking positions and positions within their range
            # on which allied pieces are placed (positions which they can defend if enemy takes out allied piece)

            if enemy.__class__.__name__ != 'Pawn':
                attacked_positions.append(positions)
                attacked_positions.append(attackable_positions)
            else:
                attacked_positions.append(attackable_positions)

        return attacked_positions, enemies

    def handle_check(self, taken_piece: Piece):
        """
            Filters generated positions by taken_piece.generate_positions(), so that it only leaves legal positions -
        positions on which king in not in check

        :param taken_piece: instance of Piece, current piece which player wants to move
        :return: None
        """
        attacked_positions, enemies = self.generate_enemy_positions()

        # flattens attacked_positions array
        attacked_positions = list(itertools.chain.from_iterable(attacked_positions))

        if taken_piece.__class__.__name__ == 'King':
            self.positions = [pos for pos in self.positions if pos not in attacked_positions]
        else:
            for pos in attacked_positions:
                # check if king is in check
                if self.board[pos].__class__.__name__ != 'King': continue
                if self.board[pos].type_of_piece != self.current_player: continue

                # generate positions of enemies which are checking the king
                # and also the positions to block that check
                attacker_enemy_positions, attacker_enemies = self.get_positions_of_enemy_which_is_checking_the_king(
                    enemies)
                blocking_positions = self.get_positions_that_block_check(attacker_enemies)

                # if there are two enemies checking the king at the same time then we break out from the loop
                # and set positions to empty array, because only way to remove check is by moving the king
                self.positions = []
                if len(attacker_enemy_positions) > 1:
                    break

                # here we generate all positions that can kill the checker enemy or block the check
                if taken_piece.__class__.__name__ != 'Pawn':
                    possible_attacking_positions = taken_piece.generate_positions(self.board)[0]
                    possible_blocking_positions = possible_attacking_positions
                else:
                    possible_blocking_positions, possible_attacking_positions = taken_piece.generate_positions(self.board)

                if attacker_enemy_positions[0] in possible_attacking_positions:
                    self.positions.append(attacker_enemy_positions[0])

                for blk_pos in blocking_positions:
                    if blk_pos in possible_blocking_positions:
                        self.positions.append(blk_pos)

    def get_positions_of_enemy_which_is_checking_the_king(self, enemies: list):
        """
            Generates enemies which are checking the king and their positions

        :param enemies: list of instances of Piece
        :return: tuple of lists, (checker enemy positions, checker enemies, king)
        """

        positions = []
        checker_enemies = []
        for enemy in enemies:
            if enemy.__class__.__name__ == 'Pawn':
                attacked_positions = enemy.generate_positions(self.board)[1]
            else:
                attacked_positions = list(itertools.chain.from_iterable(enemy.generate_positions(self.board)))

            for pos in attacked_positions:
                if self.board[pos].__class__.__name__ == 'King' and self.board[pos].type_of_piece == self.current_player:
                    positions.append((enemy.y, enemy.x))
                    checker_enemies.append(enemy)

        return positions, checker_enemies

    def get_positions_that_block_check(self, attacker_enemies: list):
        """
            Generates positions which are between checker enemy and the king

        :param attacker_enemies: list on length one
        :return: list, positions between checker enemy and the king
        """
        king = self.get_allied_king()

        attacker_enemy = attacker_enemies[0]
        attacker_enemy_positions = attacker_enemy.generate_positions(self.board)[0]

        positions_toward_king = []

        step_x = 1 if king.x > attacker_enemy.x else -1
        step_y = 1 if king.y > attacker_enemy.y else -1

        # DIAGONAL ENEMY
        if attacker_enemy.x != king.x and attacker_enemy.y != king.y:
            for i in range(step_x, king.x - attacker_enemy.x, step_x):
                if i > 0:
                    pos = (attacker_enemy.y + step_y * i, attacker_enemy.x + i)
                else:
                    pos = (attacker_enemy.y - step_y * i, attacker_enemy.x + i)

                if pos in attacker_enemy_positions:
                    positions_toward_king.append(pos)

        # HORIZONTAL ENEMY
        if attacker_enemy.y == king.y:
            for i in range(step_x, king.x - attacker_enemy.x, step_x):
                pos = (attacker_enemy.y, attacker_enemy.x + i)

                if pos in attacker_enemy_positions:
                    positions_toward_king.append(pos)

        # VERTICAL ENEMY
        if attacker_enemy.x == king.x:
            for i in range(step_y, king.y - attacker_enemy.y, step_y):
                pos = (attacker_enemy.y + i, attacker_enemy.x)

                if pos in attacker_enemy_positions:
                    positions_toward_king.append(pos)

        return positions_toward_king

    def is_checkmate(self):
        """
            Determines whether there is a checkmate or not

        :return: bool
        """

        allied_pieces = self.get_allies()

        # we loop over allied pieces and generate moves one by one
        # if we find the piece which has at least one legal move,
        # then we know that it can't be checkmate so the function returns False early
        # if loop finishes without returning than here must be no available move for any of the allied piece
        # which indicates checkmate so function returns True

        for piece in allied_pieces:
            self.positions = piece.generate_positions(self.board)[0]
            # we imitate taking off the piece because handle_check function works when we take the piece from the board
            # after calling handle_check function we put the piece back where it was before
            self.board[piece.y, piece.x] = 0
            self.handle_check(piece)
            self.board[piece.y, piece.x] = piece

            if self.positions:
                # here we set positions to be an empty array because
                # Screen displays positions automatically after this function
                self.positions = []
                return False

        if self.is_check():
            return True
        else:
            self.draw = True
            return False


    def is_draw(self):
        return self.draw

"""
Game state module
"""

import copy

import pygame

from checkers.cons import WHITE, BLACK, ROWS, COLS, BLUE, SQUARE_SIZE
from checkers.elements import Board


class GameState:
    def __init__(self, player, window):
        self.board = Board()
        self.turn = player
        self.opponent = BLACK if self.turn == WHITE else WHITE
        self.captured = []
        self.window = window
        self.reset()
        self.selected = None
        self.valid_moves = {}

    def reset(self):
        self.pieces = self.get_pieces(self.turn)

    def get_pieces(self, color):
        pieces = []
        for i in range(ROWS):
            for j in range(ROWS):
                piece = self.board.board[i][j]
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_valid_moves(self, row_dirs, position):
        next_moves = []
        is_back = False

        for row_dir in row_dirs:
            left_capture = False
            next_row = position[0] + row_dir

            if next_row < 0 or next_row >= COLS:
                continue

            for col_dir in (-1, 1):
                next_col = position[1] + col_dir

                if next_col < 0 or next_col >= ROWS:
                    continue

                next_position = self.board.board[next_row][next_col]

                if next_position == 0:
                    if not self.captured:
                        next_move = {'end_move': (next_row, next_col), 'capture': copy.deepcopy(self.captured)}
                        next_moves.append(next_move)
                elif next_position.color == self.opponent:
                    skip_row, skip_col = next_row + row_dir, next_col + col_dir

                    if 0 <= skip_row < COLS and 0 <= skip_col < ROWS and self.board.board[skip_row][skip_col] == 0:
                        self.captured.append({"capture": (next_row, next_col), "next_position": (skip_row, skip_col)})
                        piece = self.board.board[next_row][next_col]
                        self.board.board[next_row][next_col] = 0

                        if col_dir == -1:
                            left_capture = True

                        if (next_row + row_dir == ROWS - 1 and self.turn == WHITE) or (
                                next_row + row_dir == 0 and self.turn == BLACK):
                            row_dirs = [-1, 1]

                        next_move = self.get_valid_moves(row_dirs, (skip_row, skip_col)) #recurion
                        next_moves += next_move

                        del self.captured[-1]      #backtracking
                        is_back = True
                        self.board.board[next_row][next_col] = piece
                        if next_row + row_dir == ROWS - 1 and self.turn == WHITE:
                            row_dirs = (1,)
                        elif next_row + row_dir == 0 and self.turn == BLACK:
                            row_dirs = (-1,)

        if self.captured and not is_back and not left_capture:
            end_move = self.captured[-1]['next_position']
            move = {'end_move': (end_move[0], end_move[1]), 'capture': copy.deepcopy(self.captured)}
            next_moves.append(move)
            return next_moves

        return next_moves

    def update_board(self, piece, next_move, make_move=False):
        if make_move:
            board_temp = self.board
        else:
            board_temp = copy.deepcopy(self.board)
        if next_move['capture']:
            board_temp.skip(piece, next_move['capture'])
        else:
            board_temp.move(piece, next_move['end_move'][0], next_move['end_move'][1])
        return board_temp

    def select(self, row, col):
        if self.selected:
            result = self.human_move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.board[row][col]
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.get_valid_moves(piece.dir, (piece.row, piece.col))
            return True
        return False

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move['end_move'][0], move['end_move'][1]
            pygame.draw.circle(self.window, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def update_window(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def is_valid_move(self, row, col):
        for move in self.valid_moves:
            if (row, col) == move['end_move']:
                return move
        return False

    def human_move(self, row, col):
        piece = self.board.board[row][col]
        next_move = self.is_valid_move(row, col)
        if self.selected and piece == 0 and next_move:
            self.update_board(self.selected, next_move, make_move=True)
            self.change_turn()
        else:
            return False
        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
            self.opponent = BLACK
        else:
            self.turn = BLACK
            self.opponent = WHITE

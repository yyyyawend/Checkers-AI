"""
Elements of Boards and Piece for pygame.

Reference:
https://github.com/techwithtim/Python-Checkers-AI/tree/master/checkers
"""

import pygame
from checkers.cons import RED, ROWS, SQUARE_SIZE, WHITE, BLACK, CROWN, COLS, GREY


class Board:
    def __init__(self):
        self.board = []
        self.w_left = self.b_left = (ROWS // 2 - 1) * ROWS // 2
        self.w_king_left = self.b_king_left = 0
        self.create_board()


    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < ROWS // 2-1:
                        self.board[row].append(Piece(row, col, WHITE, (1,)))
                    elif row > ROWS // 2:
                        self.board[row].append(Piece(row, col, BLACK,(-1,)))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.w_king_left += 1
            else:
                self.b_king_left += 1

    def skip(self, piece, captures):
        for capture in captures:
            captured_piece=self.board[capture["capture"][0]][capture["capture"][1]]
            if captured_piece != 0:
                if captured_piece.color == BLACK:
                    self.b_left -= 1
                else:
                    self.w_left -= 1
            self.board[capture["capture"][0]][capture["capture"][1]] = 0
            self.move(piece,capture["next_position"][0],capture["next_position"][1])

    def winner(self):
        if self.b_left <= 0:
            return WHITE
        elif self.w_left <= 0:
            return BLACK
        return None

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color, dir):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.dir=dir
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True
        self.dir=[-1,1]

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)
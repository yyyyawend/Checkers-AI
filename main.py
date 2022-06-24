import pygame
from checkers.cons import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, WHITE
from checkers.elements import Piece
from checkers.gameState import GameState

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = GameState(BLACK,WIN)

    while run:
        clock.tick(FPS)

        # if game.turn == WHITE:
        #     value, new_board =
        #     game.ai_move(new_board)

        winner=game.board.winner()
        if winner != None:
            print(winner)
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update_window()

    pygame.quit()

def test():
    board1 = [[0, 0, Piece(0, 2, WHITE, (1,)), 0, Piece(0, 4, WHITE, (1,)), 0, 0, 0, ],
              [0, 0, Piece(1, 2, WHITE, (1,)), 0, Piece(1, 4, WHITE, (1,)), 0, 0, 0, ],
              [0, Piece(2, 1, BLACK, (-1,)), 0, 0, 0, 0, 0, 0, ],
              [0, 0, 0, 0, 0, 0, 0, 0, ],
              [0, 0, 0, 0, Piece(4, 4, WHITE, (1,)), 0, 0, 0, ],
              [0, 0, 0, 0, 0, 0, 0, 0, ],
              [0, 0, Piece(6, 2, WHITE, (1,)), 0, 0, 0, 0, 0, ],
              [0,Piece(7, 1, BLACK, (-1,)), 0, 0, 0, 0, 0, 0, ],
              ]
    game = GameState(BLACK, WIN)
    game.board.board=board1
    moves=game.get_valid_moves((-1,),[7,1])
    print("moves",moves)

if __name__ == '__main__':
    main()
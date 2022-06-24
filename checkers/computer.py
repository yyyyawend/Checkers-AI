import random


class randomPlayer:
    def __init__(self, color):
        self.player_tag = 'Random'
        self.win_count = 0
        self.color = color

    def get_next_move(self, game):
        next_move_options = game.get_valid_moves()
        next_move = random.choice(next_move_options)
        return next_move
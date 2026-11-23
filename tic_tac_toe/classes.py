import random
from collections import Counter


class Square:
    min_side = 3

    def __init__(self, side):
        self.side = side
        self.area = self.side ** 2

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, side):
        if not isinstance(side, int):
            raise TypeError(f"The side must be 'int' not '{type(side)}'")
        if side < Square.min_side:
            raise ValueError(f"The side must be greater or equal '{Square.min_side}'")
        self._side = side



class Board(Square):
    def __init__(self, side):
        super().__init__(side)
        self.grid = self.build_grid()

    def build_grid(self):
        grid = []
        count = 1
        for _ in range(self.side):
            row = []
            for _ in range(self.side):
                row.append(str(count))
                count += 1
            grid.append(row)
        return grid

    def validate_cell_num(self, cell_num):
        try:
            cell_num = int(cell_num)
        except ValueError:
            raise ValueError("Cell number must be an integer!")
        
        if not (1 <= cell_num <= self.area):
            raise IndexError(f"Cell number must be only from '1' to '{self.area}'!")
        
        return str(cell_num)

    def get_position(self, cell_num):
        for row, row_value in enumerate(self.grid):
            for col, col_value in enumerate(row_value):
                if col_value == cell_num:
                    return row, col
                
        raise IndexError(f"Cell number at postion '{cell_num}' is not available anymore!")

    def update(self, cell_num, symbol):
        cell_num = self.validate_cell_num(cell_num)
        row, col = self.get_position(cell_num)
        self.grid[row][col] = symbol
        return row, col

    def __str__(self):
        just_len = len(str(self.area))
        return "\n".join([" | ".join([col.rjust(just_len) for col in row]) for row in self.grid])



class Player:
    symbols = set()

    def __init__(self, symbol):
        self.symbol = symbol
        self.is_turn = False
        self.moves = []
        self.score = 0

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        if symbol.isnumeric() or len(symbol) != 1:
            raise ValueError("The symbol must be one alphabetical character!")
        elif symbol in Player.symbols:
            raise ValueError(f"The symbol {symbol} is already taken!")
        Player.symbols.add(symbol)
        self._symbol = symbol

    def switch_turn(self):
        self.is_turn = not self.is_turn

    def update_moves(self, move):
        self.moves.append(move)

    def update_score(self):
        self.score += 1

    def reset_moves(self):
        self.moves.clear()

    def __str__(self):
        return f"player '{self.symbol}'"


    
class Refree:
    def __init__(self, *players):
        self.players = players

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, players):
        for i, player in enumerate(players):
            if not isinstance(player, Player):
                raise TypeError(f"You must pass a Player object at position '{i}'!")
        self._players = players

    def determine_starter(self):
        starter = random.choice(self.players)
        starter.is_turn = True

    def whose_turn(self):
        for player in self.players:
            if player.is_turn:
                return player
        
    def switch_players(self, current_player):
        next_index = (self.players.index(current_player) + 1) % len(self.players)
        current_player.switch_turn()
        self.players[next_index].switch_turn()

    def reset_players_turns(self):
        for player in self.players:
            if player.is_turn:
                player.switch_turn()

    def reset_players_moves(self):
        for player in self.players:
            if player.moves:
                player.reset_moves()

    @staticmethod
    def row_case(board_side, player_moves):
        rows = [move[0] for move in player_moves]
        counter = Counter(rows)
        return board_side == max(counter.values())

    @staticmethod
    def col_case(board_side, player_moves):
        cols = [move[1] for move in player_moves]
        counter = Counter(cols)
        return board_side == max(counter.values())

    @staticmethod
    def main_diameter_case(board_side, player_moves):
        filtred = list(filter(lambda move: move[0] == move[1], player_moves))
        return len(filtred) == board_side

    @staticmethod
    def rev_diameter_case(board_side, player_moves):
        filtred = list(filter(lambda move: move[0] + move[1] == board_side - 1
                              , player_moves))
        return len(filtred) == board_side

    @staticmethod
    def game_logic(board_side, player_moves):
        if len(player_moves) >= board_side:
            return any((Refree.row_case(board_side, player_moves),
            Refree.col_case(board_side, player_moves),
            Refree.main_diameter_case(board_side, player_moves),
            Refree.rev_diameter_case(board_side, player_moves)))
        return False

    def determine_winner(self, board_side):
        for player in self.players:
            if self.game_logic(board_side, player.moves):
                return player
        return False 

    def __str__(self):
        return " | ".join(map(lambda player: f"{player}: {player.score}",
                                   self.players))
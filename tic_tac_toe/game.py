from classes import Board, Player, Refree

PLAYERS_NUM = 2
BOARD_SIDE = 4

def main():
    # 1- create players
    players = (create_player(i+1) for i in range(PLAYERS_NUM))

    # 2- create refree
    refree = Refree(*players)


    # - display board and turn until a player win
    while True:

        # 3- create board
        board = Board(BOARD_SIDE)

        # 4- determine the starter
        refree.determine_starter()

        for _ in range(board.area):
            # 5- display board
            print(board)

            # 6- determine current player
            current_player = refree.whose_turn()
            print(f"{current_player}, your turn")

            # 7- get player move
            row, col = get_place(board, current_player.symbol)
            current_player.update_moves((row, col))
            
            # winning logic
            winner = refree.determine_winner(board.side)
            if winner:
                print(board)
                winner.update_score()
                print(f"Congratulation, the {winner} win!")
                break

            refree.switch_players(current_player)

        else:
            print(board)
            print("draw, no one wins")

        refree.reset_players_turns()
        refree.reset_players_moves()

        print(refree)

        answer = input("continue? y/n: ").strip().lower()
        if answer == "n":
            print("End game.")
            break


def create_player(n):
    while True:
        try:
            return Player(input(f"Player {n}, enter your symbol: ").strip().upper())
        except ValueError as error:
            print(error)

def get_place(board, symbol):
    while True:
        try:
            cell_num = input(
                f"Choose a place from '1' to '{board.area}': ").strip()
            return board.update(cell_num, symbol)
        except (ValueError, IndexError) as error:
            print(error)

if __name__ == "__main__":
    main()
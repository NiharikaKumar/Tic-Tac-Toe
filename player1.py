import socket
from gameboard import BoardClass

# PLAYER 1 WILL ACT AS THE CLIENT


def p1_instructions():
    """
    Define the instructions to play the game.
    """
    print("Let's play Tic-Tac_Toe!")
    print("Input a number between 1 and 9 to place X on the board.")
    print("The numbers on the following board show the position associate with them.")
    print("\t[1,2,3]")
    print("\t[4,5,6]")
    print("\t[7,8,9]")
    print()



def p2_details() -> tuple[str, int]:
    """
    Obtain the host and port information from user and return it as a 2-tuple.

    Returns:
        p2_address: a 2-tuple containing host and port information for player 2.
        
    Raises:
        ValueError: value error if the port input is not an integer value.
    """
    
    p2_host_input = input('Enter the host name/IP address of player 2: ')
    p2_port_input = int(input('Enter the port number: '))
    
    return (p2_host_input, p2_port_input)


   
def p2_connection() -> tuple[str, object]:
    """
    Establish a successful connection to player 2.

    Returns:
        A 2-tuple containing player 2's username, and the socket object.
    """
    
    conn = True
    p2_username = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while conn:
        try:
            p2_host, p2_port = p2_details()   
            print(f"Establishing connection to player 2 at {p2_host, p2_port}")
            s.connect((p2_host, p2_port))
            print('Connection successfully established\n')
            
            p1_username = 'Player 1'
            s.sendall(p1_username.encode())
            p2_username = s.recv(1024).decode()
            print(f"Player 2's username: {p2_username}\n")
            conn = False
        except:
            print('Unable to connect to Player 2')
            retry = input('Do you want to try again? (y/n): ')
            print()

            while retry not in ['y', 'Y', 'n', 'N']:
                retry = input("Invalid input. Input 'y' or 'n': ")
            
            if retry in ['y', 'Y']:
                continue
            elif retry in ['n', 'N']:
                conn = False    #end the program


    # if p2_username = '' then that means the user didn't want to try again
    # otherwise p2_username will should equal 'Player 2'

    return (p2_username, s)

    

def check_game_over(move: int, player: str, board: list[list[str, str, str]], instance: object) -> bool:
    """
    Check if game is over by seeing if the game resulted in a win or a tie.

    Args:
        move: an integer specifying where to place the recent X/O.
        player: username of the player who made the move.
        board: a list of a list of rows storing the tic-tac-toe board.
        instance: Boardclass object for player 1.

    Returns:
        game_over: a boolean value indicating if the game is over.
    """
    
    game_won = instance.isWinner(player, board)
    game_tied = instance.boardIsFull(board)
    game_over = False
    
    if game_won:
        instance.updateGamesPlayed()
        
        if player == 'Player 1':
            instance.incrementWins()
        elif player == 'Player 2':
            instance.incrementLosses()
            
        print(f'{player} won!')
        game_over = True

    elif game_tied:
        instance.updateGamesPlayed()
        instance.incrementTies()
        
        print('game tied!')
        game_over = True

    return game_over



def check_valid_move(move: int, current_board: list[list[str, str, str]]) -> bool:
    """
    Check if a move is valid.

    A move is valid if there is no existing X/O at the move position

    Args:
        move: an integer specifying where to place the recent X/O.
        current_board: a list of a list of rows storing the tic-tac-toe board.

    Returns:
        valid: a boolean value indicating if the move is valid.
    """
    
    valid = True

    if 1 <= move <= 3:
        if current_board[0][move-1] != '_':
            valid = False
    elif 4 <= move <= 6:
        if current_board[1][move-4] != '_':
            valid = False
    elif 7 <= move <= 9:
        if current_board[2][move-7] != '_':
            valid = False
            
    return valid



def update_valid_board(move: str, player: str, board: list[list[str, str, str]], p1_obj: object) -> str:
    """
    Obtain valid moves, and update the tic-tac-toe board.

    Args:
        move: an integer specifying where to place the recent X/O.
        player: username of the player who made the move.
        board: a list of a list of rows storing the tic-tac-toe board.
        p1_obj: Boardclass object for player 1.

    Returns:
        move: a string containing the integer value of where to place the X/O 
    """
    
    get_input = True

    while get_input:
        try:
            move = int(move)

            if move <= 0 or move >= 10:
                move = input('Invalid move. Try again: ')
            else:
                valid = check_valid_move(move, board)
                if valid:
                    get_input = False
                else:
                    move = input('Invalid move. Try again: ')
        except:
            move = input('Invalid move. Try again: ')

    p1_obj.updateGameBoard(move, player, board)
    p1_obj.printBoard(board)

    return str(move)

    

def end_game(move: int, player: str, board: list[list[str, str, str]], instance: object, s: object) -> tuple[list[list[str, str, str]], bool, bool]:
    """
    Specify whether to play again or not, and reset the game accordingly.

    Args:
        move: an integer specifying where to place the recent X/O.
        player: username of the player who made the move.
        board: a list of a list of rows storing the tic-tac-toe board.
        instance: Boardclass object for player 1.
        s: socket object

    Returns:
        A 3-tuple containing a list of a list of rows for the tic-tac-toe board,
            and two boolean values indicating whether to end and reset the game.
    """
    
    reset_game = False
    end = False

    if check_game_over(move, player, board, instance):
        retry = input("Do you want to play again?")
        
        if retry in ['y', 'Y']:
            s.sendall('Play Again'.encode())
            board = instance.resetGameBoard(board)
            reset_game = True
        elif retry in ['n', 'N']:
            s.sendall('Fun Times'.encode())
            instance.printStats()
            end = True

    return board, end, reset_game



def run_player1() -> None:
    """
    Run the game for player 1.
    """
    p2_username, s = p2_connection()
    p1 = BoardClass(user='Player 1')

    p1_board = [
         ['_','_','_'],
         ['_','_','_'],
         ['_','_','_']
                   ]
    
    game = True
    
    if p2_username == 'Player 2':
        p1_instructions()
        while game:            
            p1_move = input("Player 1's move: ")
            p1.setPrevious('Player 1')

            p1_move = update_valid_board(p1_move, 'Player 1', p1_board, p1)
            
            s.sendall(p1_move.encode())
            
            p1_board, end, reset_game = end_game(p1_move, 'Player 1', p1_board, p1, s)
            if end:
                game = False
                continue
            if reset_game:
                continue
                
            
            p2_move = s.recv(1024).decode()
            p1.setPrevious('Player 2')
            
            print(f"Player 2's move: {p2_move}")

            p1.updateGameBoard(int(p2_move), 'Player 2', p1_board)
            p1.printBoard(p1_board)
            
            p1_board, end, reset = end_game(p2_move, 'Player 2', p1_board, p1, s)
            if end:
                game = False
                continue
            if reset_game:
                continue
            
                    

if __name__ == "__main__":
    run_player1()
    

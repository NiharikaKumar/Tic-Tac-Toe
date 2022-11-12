import socket
from gameboard import BoardClass


# PLAYER 2 WILL ACT AS THE SERVER

def p2_instructions():
    """
    Define the instructions to play the game.
    """
    print("Let's play Tic-Tac_Toe!")
    print("Input a number between 1 and 9 to place O on the board.")
    print("The numbers on the following board show the position associate with them.")
    print("\t[1,2,3]")
    print("\t[4,5,6]")
    print("\t[7,8,9]")
    print()



def p1_details() -> tuple[str, int]:
    """
    Obtain the host and port information from user and return it as a 2-tuple.

    Returns:
        p1_address: a 2-tuple containing the host and port information.
        
    Raises:
        ValueError: value error if the port input is not an integer value.
    """
    
    p1_host_input = input('Enter the host name/IP address: ')
    p1_port_input = input('Enter the port number: ')

    if p1_port_input.isnumeric():
        p1_port_input = int(p1_port_input)
    else:
        raise ValueError

    return (p1_host_input, p1_port_input)



def correct_connection() -> tuple[str, int]:
    """
    Ask the address information until user inputs correct values.

    Returns: A 2-tuple containing valid host and port information.
    """
    
    correct_port = False

    while not correct_port:
        try:
            p1_host, p1_port = p1_details()
            correct_port = True
        except ValueError:
            print('Please input a valid port number: ')
            print()

    return (p1_host, p1_port)



def p1_connection() -> object:
    """
    Bind my host with my port number.

    Returns:
        s: a socket object.
    """
    
    connect = False

    while not connect:
        try:
            p1_host, p1_port = correct_connection()
            print(f"Establishing socket connection at {p1_host, p1_port}")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((p1_host, p1_port))
            print('Connection successfully established\n')
            connect = True
        except:
            print('Unable to connect to Player 1. Try again.\n')

    return s



def exchange_usernames() -> tuple[str, object, object]:
    """
    Send player 2's username and recieve player 1's username.

    Returns:
        A 3-tuple containing player 1's username, socket object, connection address. 
    """
    
    s = p1_connection()
    s.listen(1)

    conn, addr = s.accept()
    p1_username = conn.recv(1024).decode()
    print(f"Player 1's username: {p1_username}")
    print()

    if p1_username:
        p2_username = 'Player 2'
        conn.sendall(p2_username.encode())

    return (p1_username, s, conn)



def check_game_over(move: int, player: str, board: list[list[str, str, str]], instance: object) -> bool:
    """
    Check if game is over by seeing if the game resulted in a win or a tie.

    Args:
        move: an integer specifying where to place the recent X/O.
        player: username of the player who made the move.
        board: a list of a list of rows storing the tic-tac-toe board.
        instance: Boardclass object for player 2.

    Returns:
        game_over: a boolean value indicating if the game is over.
    """
    
    game_won = instance.isWinner(player, board)
    game_tied = instance.boardIsFull(board)
    game_over = False
    
    if game_won:
        instance.updateGamesPlayed()

        if player == 'Player 1':
            instance.incrementLosses()
        elif player == 'Player 2':
            instance.incrementWins()
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



def update_valid_board(move: str, player: str, board: list[list[str, str, str]], p2_obj: object) -> str:
    """
    Obtain valid moves, and update the tic-tac-toe board.

    Args:
        move: an integer specifying where to place the recent X/O.
        player: username of the player who made the move.
        board: a list of a list of rows storing the tic-tac-toe board.
        p2_obj: Boardclass object for player 2.

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

    p2_obj.updateGameBoard(move, player, board)
    p2_obj.printBoard(board)

    return str(move)



def end_game(move: int, player: str, board: list[list[str, str, str]], instance: object, conn: object) -> tuple[list[list[str, str, str]], bool, bool]:
    """
    Find out from Player 1 whether to play again, and reset the game accordingly.

    Args:
        move: an integer specifying where to place the recent X/O.
        player: username of the player who made the move.
        board: a list of a list of rows storing the tic-tac-toe board.
        instance: Boardclass object for player 2.
        conn: socket connection

    Returns:
        A 3-tuple containing a list of a list of rows for the tic-tac-toe board,
            and two boolean values indicating whether to end and reset the game.
    """
    
    reset_game = False
    end = False

    if check_game_over(move, player, board, instance):
        play_again = conn.recv(1024).decode()
        
        if play_again == 'Play Again':
            board = instance.resetGameBoard(board)
            reset_game = True
        if play_again == 'Fun Times':
            instance.printStats()
            end = True

    return (board, end, reset_game)



def run_player2() -> None:
    """
    Run the game for player 2.
    """
    
    p1_username, s, conn = exchange_usernames()
    p2 = BoardClass(user='Player 2')

    p2_board = [
         ['_','_','_'],
         ['_','_','_'],
         ['_','_','_']
                   ]
    
    game = True

    p2_instructions()
    
    while game:
        p1_move = conn.recv(1024).decode()
        print("Player 1's move: ")
        p2.setPrevious('Player 1')

        p2.updateGameBoard(int(p1_move), 'Player 1', p2_board)
        p2.printBoard(p2_board)

        p2_board, end, reset_game = end_game(p1_move, 'Player 1', p2_board, p2, conn)
        if end:
            game = False
            continue
        if reset_game:
            continue
        
        p2_move = input("Player 2's move: ")
        p2.setPrevious('Player 2')
        
        p2_move = update_valid_board(p2_move, 'Player 2', p2_board, p2)
        conn.sendall(p2_move.encode())

        p2_board, end, reset_game = end_game(p2_move, 'Player 2', p2_board, p2, conn)
        if end:
            game = False
            continue
        if reset_game:
            continue


      
if __name__ == "__main__":
    run_player2()



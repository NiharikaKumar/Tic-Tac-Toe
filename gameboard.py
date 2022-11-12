class BoardClass:
    """
    A simple class to store and handle information about tic-tac-toe game.
    
    Attributes:
        user (str): Player's user name.
        previous (str): User name of the last player to have a turn.
        wins (int): Number of wins.
        ties (int): Number of ties.
        losses (int): Number of losses.
        games (int): Number of games started.
    """



    def __init__(self, user: str = '', previous: str = '', wins: int = 0,
                 ties: int = 0, losses: int = 0, games: int = 0) -> None:
        """
        Initialize the Boardclass object's attributes.

        Args:
            user: Player's user name.
            previous: User name of the last player to have a turn.
            wins: The number of wins.
            ties: The number of ties.
            losses: The number of losses.
            games: The number of games started.
        """
        
        self.setUser(user)
        self.setPrevious(previous)
        self.wins = wins
        self.ties = ties
        self.losses = losses
        self.games = games



    def setUser(self, user: str) -> None:
        """
        Set the player's user name.

        Args:
            user: User name of the player.
        """
        
        self.user = user



    def setPrevious(self, previous: str) -> None:
        """
        Set the user name of the last player to have a turn.

        Args:
            previous: User name of the previous player.
        """

        self.previous = previous



    def incrementWins(self) -> None:
        """
        Increment the number of wins by 1.
        """

        self.wins += 1


        
    def incrementTies(self) -> None:
        """
        Increment the number of ties by 1.
        """

        self.ties += 1



    def incrementLosses(self) -> None:
        """
        Increment the number of losses by 1.
        """
    
        self.losses += 1


    
    def updateGamesPlayed(self) -> None:
        """
        Increment the number of games by 1.
        """
        
        self.games += 1
        


    def boardIsFull(self, board: list) -> bool:
        """
        Check if the board is full, to check if the game has tied.

        Args:
            board: a list containing a list of rows.

        Returns:
            game_tied: a boolean value indicating whether a game is tied or not.
        """
        
        game_tied = False
        
        if '_' not in board[0]:
            if '_' not in board[1]:
                if '_' not in board[2]:
                    game_tied = True
        
        return game_tied
                    


        
    def isWinner(self, player: str, board: list) -> bool:
        """
        Check if the recent move resulted in a win.

        Args:
            player: User name of the player who made the most recent move.
            board: a list containing a list of rows with the updated move. 

        Returns:
            game_won: a boolean value indicating whether the specified player won
                        the game or not.
        """
        
        game_won = False

        if player == 'Player 1':
            mark = 'X'
        elif player == 'Player 2':
            mark = 'O'

        #checking horizontal rows of the tic-tac-toe board
        if [mark,mark,mark] in board:
            game_won = True

        #checking diagonal rows of the tic-tac-toe board
        if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark:
            game_won = True
        elif board[2][0] == mark and board[1][1] == mark and board[0][2] == mark:
            game_won = True

        #checking vertical rows of the tic-tac-toe board
        for i in range(3):
            if board[0][i]==mark and board[1][i]==mark and board[2][i]==mark:
                game_won = True

        return game_won
    


    def resetGameBoard(self, board: list) -> list:
        """
        Clear all the moves from game board.

        Args:
            board: a list containing a list of rows.
            
        Returns:
            board: a list containing a list of rows with blank columns. An empty board.
        """
        
        board = [
         ['_','_','_'],
         ['_','_','_'],
         ['_','_','_']
                   ]
        
        return board



    def updateGameBoard(self, move: int, player: str, current_board: list) -> None:
        """
        Update the gameboard with the current move by the specified player.

        Args:
            move: an integer specifiying the row and column on the current_board
                    to put the player's mark.
            player: User name of the player who made the move
            current_board: a list containing a list of rows of current game moves
            
        """
        
        if player == 'Player 1':
            mark = 'X'
        elif player == 'Player 2':
            mark = 'O'
        
        if 1 <= move <= 3:
            current_board[0][move-1] = mark
        elif 4 <= move <= 6:
            current_board[1][move-4] = mark
        elif 7 <= move <= 9:
            current_board[2][move-7] = mark


        
    def printBoard(self, board: list) -> None:
        """
        Print the game board in a matrix format.

        Args:
            board: a list containing a list of rows.
        """
        
        print('\t',board[0])
        print('\t',board[1])
        print('\t',board[2])
        print()
        
        
    
    def printStats(self) -> None:
        """
        Print the Stats for the player if the game is not to be played again
        """
        
        print()
        print(f"Player's user name: {self.user}")
        print(f"Previous player: {self.previous}")
        print(f"Number of games: {self.games}")
        print(f"Number of wins: {self.wins}")
        print(f"Number of ties: {self.ties}")
        print(f"Number of losses: {self.losses}")


"""Implement your own custom search agent using any combination of techniques
you choose.  This agent will compete against other students (and past
champions) in a tournament.

         COMPLETING AND SUBMITTING A COMPETITION AGENT IS OPTIONAL
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    opponent = game.get_opponent(player)
    moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(opponent)

    cut_moves = [m for m in filter(lambda move: move in moves, opponent_moves)]

    return float(game.utility(player) + (len(moves) - len(opponent_moves) * 0.5) + len(cut_moves))


class CustomPlayer:
    """Game-playing agent to use in the optional player vs player Isolation
    competition.

    You must at least implement the get_move() method and a search function
    to complete this class, but you may use any of the techniques discussed
    in lecture or elsewhere on the web -- opening books, MCTS, etc.

    **************************************************************************
          THIS CLASS IS OPTIONAL -- IT IS ONLY USED IN THE ISOLATION PvP
        COMPETITION.  IT IS NOT REQUIRED FOR THE ISOLATION PROJECT REVIEW.
    **************************************************************************

    Parameters
    ----------
    data : string
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted.  Note that
        the PvP competition uses more accurate timers that are not cross-
        platform compatible, so a limit of 1ms (vs 10ms for the other classes)
        is generally sufficient.
    """

    def __init__(self, data=None, timeout=1.):
        self.score = custom_score
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = (-1, -1)

        try:
            best_move = self.alphabeta(game)
        except SearchTimeout:
            pass

        return best_move

    def terminaltest(self, game, legal_moves):
        if len(legal_moves) < 1: # or depth <= 0: ignore deth limit
            return True
        else:
            return False

    def terminalmove(self, legal_moves):
        if len(legal_moves) == 1:
            return legal_moves[0]
        else:
            return (-1, -1)

    def minvalue(self, game, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            return (0, (-1, -1))

        legal_moves = game.get_legal_moves()
        if self.terminaltest(game, legal_moves):
            return (self.score(game, self), self.terminalmove(legal_moves))

        v = float("+inf")
        best_move = (-1, -1)
        for move in legal_moves:
            max_v,_ = self.maxvalue(game.forecast_move(move), alpha, beta)
            if max_v < v or best_move[0] < 0:
                best_move = move
                v = max_v

            if v <= alpha:
                return (v, move)

            beta = min(beta, v)
        return (v, best_move)

    def maxvalue(self, game, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            return (0, (-1, -1))

        legal_moves = game.get_legal_moves()
        if self.terminaltest(game, legal_moves):
            return (self.score(game, self), self.terminalmove(legal_moves))

        v = float("-inf")
        best_move = (-1, -1)
        for move in legal_moves:
            min_v, _ = self.minvalue(game.forecast_move(move), alpha, beta)
            if min_v > v or best_move[0] < 0:
                best_move = move
                v = min_v

            if v >= beta:
                return (v, move)

            alpha = max(alpha, v)
        return (v, best_move)

    def alphabeta(self, game, alpha=float("-inf"), beta=float("inf")):
        move = (-1, -1)
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        _, move = self.maxvalue(game, alpha, beta)
        return move

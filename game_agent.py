import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    opponent = game.get_opponent(player)
    moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(opponent)
    return float(game.utility(player) + (len(moves) - len(opponent_moves) * 2))

def custom_score_2(game, player):
    opponent = game.get_opponent(player)
    moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(opponent)

    cut_moves = [m for m in filter(lambda move: move in moves, opponent_moves)]

    return float(game.utility(player) + (len(moves) - len(opponent_moves)) + len(cut_moves))

def custom_score_3(game, player):
    opponent = game.get_opponent(player)
    moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(opponent)

    cut_moves = [m for m in filter(lambda move: move in moves, opponent_moves)]

    return float(game.utility(player) + (len(moves) - len(opponent_moves) * 0.5) + len(cut_moves))

class IsolationPlayer:
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    def get_move(self, game, time_left):
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def terminaltest(self, depth, legal_moves):
        if len(legal_moves) < 1 or depth <= 0:
            return True
        else:
            return False

    def terminalmove(self, legal_moves):
        if len(legal_moves) == 1:
            return legal_moves[0]
        else:
            return (-1, -1)

    def maxvalue(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD * 1.2:
            return (0, (-1, -1))

        legal_moves = game.get_legal_moves()

        if self.terminaltest(depth, legal_moves):
            return (self.score(game, self), self.terminalmove(legal_moves))

        v = float("-inf")
        best_move = (-1, -1)
        for move in legal_moves:
            min_v,_ = self.minvalue(game.forecast_move(move), depth - 1)
            if min_v > v or best_move[0] < 0:
                best_move = move
                v = min_v
        return (v, best_move)

    def minvalue(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD * 1.2:
            return (0, (-1, -1))

        legal_moves = game.get_legal_moves()

        if self.terminaltest(depth, legal_moves):
            return (self.score(game, self), self.terminalmove(legal_moves))

        v = float("+inf")
        best_move = (-1, -1)
        for move in legal_moves:
            max_v, _ = self.maxvalue(game.forecast_move(move), depth - 1)
            if max_v < v or best_move[0] < 0:
                best_move = move
                v = max_v
        return (v, best_move)

    def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        _, move = self.maxvalue(game, depth)
        return move


class AlphaBetaPlayer(IsolationPlayer):
    def get_move(self, game, time_left):
        self.time_left = time_left

        best_move = (-1, -1)

        try:
            i = 0
            while self.time_left() > self.TIMER_THRESHOLD:
                best_move = self.alphabeta(game, self.search_depth + i)
                i += 1
        except SearchTimeout:
            pass

        return best_move

    def terminaltest(self, game, depth, legal_moves):
        if depth <= 0 or len(legal_moves) < 1:
            return True
        else:
            return False

    def terminalmove(self, legal_moves):
        if len(legal_moves) == 1:
            return legal_moves[0]
        else:
            return (-1, -1)

    def minvalue(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            return (0, (-1, -1))

        legal_moves = game.get_legal_moves()
        if self.terminaltest(game, depth, legal_moves):
            return (self.score(game, self), self.terminalmove(legal_moves))

        v = float("+inf")
        best_move = (-1, -1)
        for move in legal_moves:
            max_v,_ = self.maxvalue(game.forecast_move(move), depth - 1, alpha, beta)
            if max_v < v or best_move[0] < 0:
                best_move = move
                v = max_v

            if v <= alpha:
                return (v, move)

            beta = min(beta, v)
        return (v, best_move)

    def maxvalue(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            return (0, (-1, -1))

        legal_moves = game.get_legal_moves()
        if self.terminaltest(game, depth, legal_moves):
            return (self.score(game, self), self.terminalmove(legal_moves))

        v = float("-inf")
        best_move = (-1, -1)
        for move in legal_moves:
            min_v, _ = self.minvalue(game.forecast_move(move), depth - 1, alpha, beta)
            if min_v > v or best_move[0] < 0:
                best_move = move
                v = min_v

            if v >= beta:
                return (v, move)

            alpha = max(alpha, v)
        return (v, best_move)

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        move = (-1, -1)
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        _, move = self.maxvalue(game, depth, alpha, beta)
        return move

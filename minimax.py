import math
from copy import deepcopy

AI = -1
PLAYER = 1


def is_valid(row, col):
    return 0 <= row < 6 and 0 <= col < 7


class State:
    def __init__(self, board, moves, ai_score, player_score, ai_potential_score, player_potential_score,
                 player_potentials, ai_potentials, game_over, player):

        self.board = board
        self.moves = moves
        self.ai_score = ai_score
        self.player_score = player_score
        self.ai_potential_score = ai_potential_score
        self.player_potential_score = player_potential_score
        self.player = player
        self.player_potentials = player_potentials
        self.ai_potentials = ai_potentials
        self.game_over = game_over

    def generate_child(self, col):
        # create new board
        row = self.moves[col]
        board = deepcopy(self.board)
        board[row][col] = self.player

        # update moves
        moves = deepcopy(self.moves)
        moves[col] += 1

        # change player
        player = AI if self.player == PLAYER else PLAYER


        player_potentials = deepcopy(self.player_potentials)
        ai_potentials = deepcopy(self.ai_potentials)
        score, potential = self.check_score(row, col, player_potentials, ai_potentials, True)
        ai_score = self.ai_score
        player_score = self.player_score
        ai_potential_score = self.ai_potential_score
        player_potential_score = self.player_potential_score


        # update score and potential
        if self.player == PLAYER:
            player_potential_score += potential
            player_score += score
        else:
            ai_potential_score += potential
            ai_score += score

        return State(board, moves, ai_score, player_score, ai_potential_score, player_potential_score,
                     self.player_potentials, self.ai_potentials, self.game_over, player)

    def check_score(self, row, col, player_potentials=None, ai_potentials=None, potential=False):

        # Check for a winning condition (horizontal, vertical, diagonal)
        return [sum(x) for x in zip(
            self.check_line(row, col, 0, 1, player_potentials, ai_potentials, potential),  # -
            self.check_line(row, col, 1, 0, player_potentials, ai_potentials, potential),  # |
            self.check_line(row, col, 1, 1, player_potentials, ai_potentials, potential),  # /
            self.check_line(row, col, -1, 1, player_potentials, ai_potentials, potential)  # \
        )]

    def check_line(self, row, col, row_change, col_change, player_potentials=None, ai_potentials=None, potential=True):
        count = 1

        # keep track of original play
        r = row
        c = col

        # count consecutive pieces in the positive direction from the dropped piece
        row += row_change
        col += col_change
        iter = 1
        while is_valid(row, col) and self.board[row][col] == self.player and iter < 3:
            # count consecutive pieces of the same color
            count += 1
            iter += 1
            row += row_change
            col += col_change

        right_gap = None
        if is_valid(row, col):
            if self.board[row][col] == 0:
                right_gap = (row, col)
            elif is_valid(row, col) and self.board[row][col] == self.player:
                count += 1

        # reset to starting position
        row = r - row_change
        col = c - col_change

        # check in the opposite direction
        iter = 1
        while is_valid(row, col) and self.board[row][col] == self.player and iter < 3:
            # count consecutive pieces of the same color
            count += 1
            iter += 1
            row -= row_change
            col -= col_change

        left_gap = None
        if is_valid(row, col):
            if self.board[row][col] == 0:
                left_gap = (row, col)
            elif is_valid(row, col) and self.board[row][col] == self.player:
                count += 1

        score = max(0, count - 3)

        if potential:
            right_potential, left_potential = 0, 0
            if right_gap:
                right_potential = self.check_score(right_gap[0], right_gap[1], False)[0]
                temp = right_potential
                if self.player == PLAYER:
                    right_potential = right_potential - player_potentials[right_gap[0]][right_gap[1]]
                    player_potentials[right_gap[0]][right_gap[1]] = temp
                else:
                    right_potential = right_potential - ai_potentials[right_gap[0]][right_gap[1]]
                    ai_potentials[right_gap[0]][right_gap[1]] = temp

            if left_gap:
                left_potential = self.check_score(left_gap[0], left_gap[1], False)[0]
                temp = left_potential
                if self.player == PLAYER:
                    left_potential = left_potential - player_potentials[left_gap[0]][left_gap[1]]
                    player_potentials[left_gap[0]][left_gap[1]] = temp
                else:
                    left_potential = left_potential - ai_potentials[left_gap[0]][left_gap[1]]
                    ai_potentials[left_gap[0]][left_gap[1]] = temp

            return score, right_potential + left_potential
        else:
            return [score]

    def utility(self):
        return self.ai_score - self.player_score + 0.75 * (self.ai_potential_score - self.player_potential_score)


class Minimax:
    def __init__(self, game, depth):
        self.game = game
        self.depth = depth

    def minimax(self, state, depth):
        print(f"depth: {depth}, player: {state.player}, score: {state.utility()}")
        if depth == 0 or state.game_over == 0:
            return state.utility(), None

        if state.player == AI:
            best_value = -math.inf
            best_move = None
            for i, move in enumerate(state.moves):
                # skip if column is full
                if move >= 6:
                    continue

                value, _ = self.minimax(state.generate_child(i), depth - 1)
                if value > best_value:
                    best_value = value
                    best_move = i
            return best_value, best_move
        else:
            best_value = math.inf
            best_move = None
            for i, move in enumerate(state.moves):
                # skip if column is full
                if move >= 6:
                    continue

                value, _ = self.minimax(state.generate_child(i), depth - 1)
                if value < best_value:
                    best_value = value
                    best_move = i
            return best_value, best_move

    def play(self):
        state = State(self.game.board, self.game.moves, self.game.ai_score, self.game.player_score,
                      self.game.ai_potential_score, self.game.player_potential_score, self.game.player_potentials,
                      self.game.ai_potentials, self.game.game_over, AI)
        # get the best move
        _, move = self.minimax(state, self.depth)

        return move
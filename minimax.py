import math
import treelib
from copy import deepcopy, copy

def my_print(str):
    pass

AI = -1
PLAYER = 1
VERBOSE = False
# ID_COUNTER = 0
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
        row = 5 - self.moves[col]
        board = deepcopy(self.board)
        board[row][col] = self.player

        # update moves
        moves = copy(self.moves)
        moves[col] += 1

        # check for game over
        game_over = self.game_over
        if moves[col] == 6:
            game_over -= 1

        # change player
        player = -self.player

        # update potentials
        player_potentials = deepcopy(self.player_potentials)
        ai_potentials = deepcopy(self.ai_potentials)
        my_print(self.board)
        self.board[row][col] = self.player
        score, potential = self.check_score(row, col, player_potentials, ai_potentials, True)
        self.board[row][col] = 0
        my_print(f"score: {score}, potential: {potential} at {row}, {col}")
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


        # check for score and potential score for opposite color
        # self.player = -self.player
        # result = self.check_score(row, col, potential=False)
        # self.player = -self.player

        if self.player == PLAYER:
            ai_potential_score -= player_potentials[row][col]
        else:
            player_potential_score -= ai_potentials[row][col]

        my_print(f"score: {score}, potential: {potential} at {row}, {col}, aipo: {ai_potential_score}, "
              f"pipo: {player_potential_score}")
        return State(board, moves, ai_score, player_score, ai_potential_score, player_potential_score,
                     player_potentials, ai_potentials, game_over, player)

    def check_score(self, row, col, player_potentials=None, ai_potentials=None, potential=False):
        # Check for a winning condition (horizontal, vertical, diagonal)
        a = self.check_line(row, col, 0, 1, player_potentials, ai_potentials, potential)  # -
        b = self.check_line(row, col, 1, 0, player_potentials, ai_potentials, potential)  # |
        c = self.check_line(row, col, 1, 1, player_potentials, ai_potentials, potential)  # /
        d = self.check_line(row, col, -1, 1, player_potentials, ai_potentials, potential)           # \
        return [sum(x) for x in zip(a, b, c, d)]

    def check_line(self, row, col, row_change, col_change, player_potentials=None, ai_potentials=None, potential=True):
        # my_print(f"row: {row}, col: {col}, row_change: {row_change}, col_change: {col_change}", '-' * 50)
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
            elif self.board[row][col] == self.player:
                count += 1
        # my_print(f"right: {right_gap}")
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
        # my_print(f"left: {left_gap}")

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
            my_print(f"right: {right_potential} at {right_gap}, left: {left_potential} at {left_gap}")
            return score, right_potential + left_potential
        else:
            return [score]

    def utility(self):
        # my_print(f"aipot: {self.ai_potential_score}, pipot: {self.player_potential_score}")
        return self.ai_score - self.player_score + 0.5 * (self.ai_potential_score - self.player_potential_score)


class Minimax:
    ID_COUNTER = 1
    def __init__(self, game, depth, pruning=True, expectimax=False):
        self.game = game
        self.depth = depth
        self.pruning = pruning
        self.expectimax = expectimax

        if pruning:
            self.alpha = -math.inf
            self.beta = math.inf

    def minimax(self, state, depth, alpha=-math.inf, beta=math.inf, parent_id=0, pruning=True):
        if parent_id == None:
            self.tree.create_node(state.board, 0)
            id = 0
        else:
            self.tree.create_node(state.board, self.ID_COUNTER, parent_id)
            id = self.ID_COUNTER
            self.ID_COUNTER += 1

        if VERBOSE:
            my_print(f"depth: {depth}, player: {state.player}, score: {state.utility()}")

        if depth == 0 or state.game_over == 0:
            return state.utility(), None

        if self.expectimax:
            values = [0] * 7

        if state.player == AI:
            best_value = -math.inf

            best_move = None

            for i, move in enumerate(state.moves):
                # skip if column is full
                if move >= 6:
                    continue

                if pruning:
                    values, _ = self.minimax(state.generate_child(i), depth - 1, alpha, beta, parent_id=id)
                    my_print(f"current move -> move: {i}, value: {values}")
                    # print(f"alpha: {alpha}, beta: {beta}, value: {values}")

                    if self.expectimax:
                        if type(values) is float:
                            value = values
                        else:
                            v1 = values[i] * 0.6
                            v2 = values[(i - 1) % 7] * 0.2
                            v3 = values[(i + 1) % 7] * 0.2

                            value = (v1 + v2 + v3) / 3
                    else:
                        value = values

                    alpha = max(alpha, value)
                    if alpha >= beta:
                        return value, i
                elif self.expectimax:
                    values, _ = self.minimax(state.generate_child(i), depth - 1,  parent_id=id, pruning=False)
                    if type(values) is float:
                        value = values
                    else:
                        v1 = values[i] * 0.6
                        v2 = values[(i-1) % 7] * 0.2
                        v3 = values[(i+1) % 7] * 0.2

                        value = (v1+v2+v3) / 3

                else:
                    value, _ = self.minimax(state.generate_child(i), depth - 1,  parent_id=id, pruning=False)

                if value > best_value or best_move == None:
                    best_value = value
                    best_move = i

            return best_value, best_move
        else:
            best_value = math.inf
            best_move = None
            for i, move in enumerate(state.moves):
                # skip if column is full
                if move >= 6:
                    if self.expectimax:
                        values[i] = -math.inf
                    continue

                if pruning:
                    value, _ = self.minimax(state.generate_child(i), depth - 1, alpha, beta,  parent_id=id)# (10, 4)
                    # (12, 3)
                    beta = min(beta, value)                                                 # (15, 5)
                    if alpha >= beta:
                        return value, i
                elif self.expectimax:
                    values[i], _ = self.minimax(state.generate_child(i), depth - 1,  parent_id=id, pruning=False)
                    value = values[i]
                else:
                    value, _ = self.minimax(state.generate_child(i), depth - 1,  parent_id=id, pruning=False)

                # update best value and move
                if value < best_value or best_move == None:
                    best_value = value
                    best_move = i
            # return all values if expectimax
            if self.expectimax:
                return values, best_move

            return best_value, best_move


    def play(self):
        state = State(self.game.board, self.game.moves, self.game.ai_score, self.game.player_score,
                      self.game.ai_potential_score, self.game.player_potential_score, self.game.player_potentials,
                      self.game.ai_potentials, self.game.game_over, AI)
        self.tree = treelib.Tree()
        # get the best move
        if self.pruning:
            v, move = self.minimax(state, self.depth, self.alpha, self.beta, parent_id=None)
        else:
            v, move = self.minimax(state, self.depth, parent_id=None, pruning=False)

        # my_print(f"move: {move}, value: {v}")
        self.ID_COUNTER = 1
        self.tree.show()
        return move
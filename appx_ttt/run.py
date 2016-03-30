import random
import numpy as np
from tic_tac_toe import Game
import copy


ALPHA = 0.001
GAMMA = 0.7


class Weights(object):

    def __init__(self):
        self.shape = None
        self.w = None

    def get_weights(self):
        return self.w

    def update_weights(self, w):
        self.w = w
        self.shape = w.shape

    def save_weights(self):
        # TODO: Implement save and load functions.
        return


w = Weights()


def get_features(game, state, action):
    g = copy.deepcopy(game)
    if action is not None:
        g.play(action, 1)
    else:
        pass

    s_ = g.linear_board()

    f = np.asarray(s_)
    shape = f.shape

    if w.get_weights() is None:
        W = np.random.random(shape)
        w.update_weights(W)

    return f


def Q(game, state, action):
    f = get_features(game, state, action)
    wt = w.get_weights()
    if action is None:
        return 0
    return np.dot(f, wt.T)


def reward(game, state, action):
    status = game.check_status()

    if status == 10:
        return 0
    elif status == 1:
        return 100
    elif status == -1:
        return -100
    elif status == 0:
        return 10


def calculate_new_weights(game, state, action, diff):
    f = get_features(game, state, action)
    wt = w.get_weights()

    for wx in range(wt.shape[0]):
        wt[wx] = wt[wx] + ALPHA*diff*f[wx]

    return wt



def run_main(n_ep):

    overall_reward = 0

    for ix in xrange(n_ep):
        game = Game()
        s = tuple(game.linear_board())
        rew = 0

        while game.check_status() == 10:
            # Move by the reinforcement learning agent
            actions = game.available_moves()
            # print actions
            best = []
            q_best = None

            for rx in actions:
                rq = Q(game, s, rx)

                if rq > q_best:
                    q_best = rq
                    best = [rx]
                elif rq == q_best:
                    best.append(rx)

            nxt = random.choice(best)
            game.play(nxt, 1)

            # other player plays
            if game.check_status() == 10:
                game.play(random.choice(game.available_moves()), -1)
            
            s_ = tuple(game.linear_board())

            nxt_actions = game.available_moves()
            nq_best = None

            # For all actions a', get max Q-value
            for rx in nxt_actions:
                rq = Q(game, s_, rx)
                nq_best = max(nq_best, rq)

            if len(nxt_actions) == 0:
                # Game completed
                rq = Q(game, s_, None)
                nq_best = max(nq_best, rq)

            # Update weights here
            D = reward(game, s, nxt) + GAMMA*nq_best - Q(game, s, nxt)

            wts = calculate_new_weights(game, s, nxt, D)
            w.update_weights(wts)
            
            rew += reward(game, s, nxt)
            overall_reward += rew
            s = s_

        print 'iteration:', ix, 'reward:', rew

    print w.get_weights()
    print "Overall reward:", float(overall_reward)/n_ep
    print "Complete..."



if __name__ == '__main__':
    import sys

    n = 1000
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    run_main(n_ep=n)
    # main()

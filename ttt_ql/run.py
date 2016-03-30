import random
import numpy as np
from tic_tac_toe import Game

Q = dict()
R = dict()

ALPHA = 0.001
GAMMA = 0.5


def main():
    n_episodes = 20

    observations = 100

    for i in xrange(n_episodes):
        pos = 0
        length = 0

        while not pos == GOAL:
        # for ox in xrange(observations):
            # print pos

            # get possible actions
            actions = get_actions(pos)
            best = []
            q_best = None
            for rx in actions:
                rq = Q.setdefault((pos, rx), 0)
                if rq > q_best:
                    q_best = rq
                    best = [rx]
                elif rq == q_best:
                    best.append(rx)
            # Select best action out of all
            nxt = random.choice(actions)
            # print actions

            nxt_actions = get_actions(nxt)
            nq_best = None

            # For all actions, update Q-value
            for rx in nxt_actions:
                rq = Q.setdefault((nxt, rx), 0)
                nq_best = max(nq_best, rq)

            Q[(pos, nxt)] = (1 - ALPHA)*Q[(pos, nxt)] + ALPHA*(R[(pos, nxt)] +
                    GAMMA*nq_best)

            pos = nxt
        print 'episode:', i, 'end at position:', pos
        print Q


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


def run_main(n_ep):

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
                rq = Q.setdefault((s, rx), 0)

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
                rq = Q.setdefault((s_, rx), 0)
                nq_best = max(nq_best, rq)

            if len(nxt_actions) == 0:
                # Game completed
                rq = Q.setdefault((s_, None), 0)
                nq_best = max(nq_best, rq)

            Q[(s, nxt)] = (1 - ALPHA)*Q[(s, nxt)] + ALPHA*(reward(game, s,
                nxt) + GAMMA*nq_best)
            rew = reward(game, s, nxt)
            s = s_

        print 'iteration:', ix, 'reward:', rew

    print len(Q.keys())
    d = []
    for key in Q.keys():
        d.append(Q[key])
    print max(d)
    print "Complete..."



if __name__ == '__main__':
    import sys

    n = 1000
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    run_main(n_ep=n)
    # main()

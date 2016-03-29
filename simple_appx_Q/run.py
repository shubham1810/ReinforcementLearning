import random
import numpy as np

NODES = 6
GOAL = 5

ALPHA = 0.5
GAMMA = 0.5

R = {
    (0, 1): 0,
    (1, 0): 0, (1, 2): 0, (1, 3): 0,
    (2, 1): 0, (2, 4): 0, (2, 5): 100,
    (3, 1): 0, (3, 4): 0,
    (4, 2): 0, (4, 3): 0, (4, 5): 100,
    (5, 2): 0, (5, 4): 0, (5, 5): 100,
}

Q = {}


def get_actions(current):
    actions = []
    for rx in xrange(NODES):
        if (current, rx) in R:
            actions.append(rx)
    return actions


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


if __name__ == '__main__':
    main()

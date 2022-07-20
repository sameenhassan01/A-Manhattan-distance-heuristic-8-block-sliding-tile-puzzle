import numpy as np
from copy import deepcopy
from collections import defaultdict


# Manhattan distance for each digit as per goal
def mh_each_digit(s, g):
    return sum((abs(s // 3 - g // 3) + abs(s % 3 - g % 3))[1:])


# solve the board
def creat_board(board, goal):
    moves = np.array(
        [
            ('x', [0, 1, 2], -3),
            ('y', [6, 7, 8], 3),
            ('z', [0, 3, 6], -1),
            ('w', [2, 5, 8], 1)
        ],
        dtype=[
            ('move', str, 1),
            ('pos', list),
            ('delta', int)
        ]
    )

    STATE = [
        ('board', list),
        ('parent', int),
        ('gn', int),
        ('hn', int)
    ]

    PRIORITY = [
        ('pos', int),
        ('fn', int)
    ]

    previous_boards = defaultdict(bool)

    goalc = rang(goal)
     # initial state values
    hn = mh_each_digit(rang(board), goalc)
    state = np.array([(board, -1, 0, hn)], STATE)
    priority = np.array( [(0, hn)], PRIORITY)
   
   #priority queue initialization
    while True:
        # sort priority queue
        priority = np.sort(priority, kind='mergesort', order=['fn', 'pos']) 
       # pick the first from sorted to explore
        pos = priority[0][0]
         # remove queue what we exploring
        priority = np.delete(priority, 0, 0)
        board = state[pos][0]
        gn = state[pos][2] + 1
        # locate '0' (blank)
        loc = int(np.where(board == 0)[0])

        for m in moves:
            if loc not in m['pos']:
                 # generate current state as new copy
                succ = deepcopy(board)
                delta_loc = loc + m['delta']
                succ[loc], succ[delta_loc] = succ[delta_loc], succ[loc]
                succ_t = tuple(succ)

                if previous_boards[succ_t]:
                    continue

                previous_boards[succ_t] = True

                hn = mh_each_digit(rang(succ_t), goalc)
                state = np.append(
                    state,
                    np.array([(succ, pos, gn, hn)], STATE),
                    0
                )
                priority = np.append(
                    priority,
                    np.array([(len(state) - 1, gn + hn)], PRIORITY),
                    0
                )

                if np.array_equal(succ, goal):
                    return state, len(priority)

# assign each digit the coordinate to calculate Manhattan distance
def rang(s):
    c = np.array(range(9))
    for x, y in enumerate(s):
        c[y] = x
    return c

# check the initial state is solvable or not by inversion 
def inversions(s):
    k = s[s != 0]
    return sum(
        len(np.array(np.where(k[i+1:] < k[i])).reshape(-1))
        for i in range(len(k) - 1)
    )
# optimized steps in sequence 
def optimized_steps(state):
    optimal = np.array([], int).reshape(-1, 9)
    last = len(state) - 1
    while last != -1:
        optimal = np.insert(optimal, 0, state[last]['board'], 0)
        last = int(state[last]['parent'])
    return optimal.reshape(-1, 3, 3)

def main():
    
    goal = np.array([1, 2, 3, 4, 5, 6, 7, 8,0])
    string = input('Enter board numbers : ')
    board = np.array(list(map(int, string)))

    if sorted(string) != sorted('012345678'):
        print('incorrect input')
        return
    if inversions(board) % 2:
        print('not solvable')
        return

    state, explored = creat_board(board, goal)
    optimal = optimized_steps(state)

    print((
        'sliding puzzle \n'
        '\n'
        'Total generated: {}\n'
        'Total explored:  {}\n'
        '\n'
        'Total optimized steps: {}\n'
        '{}\n'
        '\n'
    ).format(len(state), len(state) - explored, len(optimal) - 1, optimal))

if __name__== '__main__':
    main()

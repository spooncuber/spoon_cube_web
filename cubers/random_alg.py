#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from alg_set_generator import alg_set_generator
from code_trans import group_recog, code_trans
from ce import chichu2ce, conn2ce

# input data
buffer = 'O'
corner_alg, edge_alg = alg_set_generator('O', 'a')
train_algs = corner_alg[0:378]

# shuffle the train_algs
random.shuffle(train_algs)
# recognize the group of buffer
div, index_num = group_recog(buffer)
# corner has max code counts with 6. edge has 10.
if div == 3:
    max_len = 6
else:
    max_len = 10

train_times = {}

# initial train times of every alg
for x in train_algs:
    train_times[x] = 0

# global state
init_state = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
              'W', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'X', 'Y', 'Z',
              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
              'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y', 'z',
              '1', '2', '3', '4', '5', '6']

# initial variables
current_pos = []
current_code = []
scramblers = []

# loop with 10 times
for i in range(10):
    # min train times of all algs
    min_times = min(train_times.values())
    print(train_times.values())

    # loop the train algs
    for x in train_algs:
        # if current_code is empty,  the first codes inside must have min train times
        # if current_code not empty, take codes with minus little than 2 (keep train times stable for every alg)
        if (len(current_code) == 0 and train_times[x] == min_times) or (current_code and train_times[x] < min_times + 2):
            # get the position numbers of the two codes.
            code = list(x)
            pos_1 = (global_state.index(code[0]) - index_num) // div
            pos_2 = (global_state.index(code[1]) - index_num) // div
            # if the positions don't overlap with current group, then append the codes
            if pos_1 not in current_pos and pos_2 not in current_pos:
                current_pos.append(pos_1)
                current_pos.append(pos_2)
                current_code.append(code[0])
                current_code.append(code[1])
                # increase train times
                train_times[x] = train_times[x] + 1
                # if the len of codes get max len, then push these codes to CE and get the scramble of this state
                if len(current_code) == max_len:
                    # turn list to str
                    input_code = ''.join([buffer, ''.join(current_code)])
                    # get state in chichu code from these codes
                    output_state = code_trans(input_code, init_state)
                    # turn chichu codes to CE codes and push it to CE
                    scramblers.append(conn2ce(chichu2ce(output_state)))
                    # empty the positions and codes
                    current_pos = []
                    current_code = []

print(min(train_times.values()), max(train_times.values()))

1+1

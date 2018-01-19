#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from code_trans import *
from ce import *

def alg_set_generator(buffer):

    # global cube state(0-23 mean corners; 24-47 mean edges; 48-55 mean centre). It's a constant.
    global_state = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'W', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'X', 'Y', 'Z',
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y', 'z',
                    '1', '2', '3', '4', '5', '6')

    div, index_num = group_recog(buffer)

    # relative positions of two buffers in global_state
    buffer_pos = (global_state.index(buffer) - index_num) // div

    alg_set = []

    # add corner alg set
    for i in range(24):
        first_pos = i // div
        # first code
        if first_pos != buffer_pos:
            for j in range(24):
                second_pos = j // div
                if second_pos != first_pos and second_pos != buffer_pos:
                    alg_set.append(''.join([global_state[i+index_num], global_state[j+index_num]]))

    return(alg_set)

# decide if input codes are already in current_pos
def ispos_repeat(x, current_pos, init_state, index_num, div):
    # get the position numbers of the two codes.
    code = list(x)
    pos_0 = (init_state.index(code[0]) - index_num) // div
    pos_1= (init_state.index(code[1]) - index_num) // div
    code_and_pos = [code[0], code[1], pos_0, pos_1]
    # if the positions don't overlap with current group, then return true
    if pos_0 not in current_pos and pos_1 not in current_pos:
        not_repeat = 1
    else:
        not_repeat = 0
    return not_repeat, code_and_pos

def add_codes(x, code_and_pos, current_code, current_pos, train_times, max_len, buffer):
    current_code.append(code_and_pos[0])
    current_code.append(code_and_pos[1])
    current_pos.append(code_and_pos[2])
    current_pos.append(code_and_pos[3])
    # reset the miss counter
    miss_counter = 0
    # increase train times
    if x in train_times.keys():
        train_times[x] = train_times[x] + 1

    input_code = []
    # if the len of codes get max len, then push these codes to CE and get the scramble of this state
    if len(current_code) == max_len:
        # turn list to str
        input_code = ''.join([buffer, ''.join(current_code)])

        # # get state in chichu code from these codes
        # output_state = code_trans(input_code, init_state)
        # # turn chichu codes to CE codes and push it to CE
        # scramblers.append(conn2ce(chichu2ce(output_state)))

        # empty the positions and codes
        current_pos = []
        current_code = []

    return input_code, current_code, current_pos, train_times, miss_counter

def random_codes(buffer, all_algs, train_algs, train_times):

    # shuffle the algs
    random.shuffle(train_algs)
    random.shuffle(all_algs)
    # recognize the group of buffer
    div, index_num = group_recog(buffer)
    # corner has max code counts with 6. edge has 10.
    if div == 3:
        max_len = 6
    else:
        max_len = 10

    # init state
    init_state = 'ABCDEFGHIJKLWMNOPQRSTXYZabcdefghijklmnopqrstwxyz123456'
    init_state = list(init_state)

    # initial variables
    current_pos = []
    current_code = []
    miss_counter = 0
    # loop with 10 times
    for i in range(10):
        # min train times of all algs
        min_times = min(train_times.values())

        # loop the train algs
        for x in train_algs:
            # if current_code is empty,  the first codes inside must have min train times
            # if current_code not empty, take codes with minus little than 2 (keep train times stable for every alg)
            if (len(current_code) == 0 and train_times[x] == min_times) or (current_code and train_times[x] < min_times + 2):
                not_repeat, code_and_pos = ispos_repeat(x, current_pos, init_state, index_num, div)
                # if the positions are not in current positions, then append the codes
                if not_repeat:
                    input_code, current_code, current_pos, train_times, miss_counter = \
                        add_codes(x, code_and_pos, current_code, current_pos, train_times, max_len, buffer)
                    # if input_code isn't empty, then return it
                    if input_code:
                        return input_code, train_times
                else:
                    # if they'are repeat codes, then add 1 to missing times
                    miss_counter += 1
                    # if miss_counter sum to the len of train_algs, then get other codes from all_algs
                    if miss_counter == len(train_algs):
                        random.shuffle(all_algs)
                        for y in all_algs:
                            not_repeat, code_and_pos = ispos_repeat(y, current_pos, init_state, index_num, div)
                            # if the positions are not in current positions, then append the codes
                            if not_repeat:
                                input_code, current_code, current_pos, train_times, miss_counter = \
                                    add_codes(y, code_and_pos, current_code, current_pos, train_times, max_len, buffer)
                                # if input_code isn't empty, then return it
                                if input_code:
                                    return input_code, train_times

# integrate two input_codes to output a state
def integrete_code(first_input, second_input):

    init_state = 'ABCDEFGHIJKLWMNOPQRSTXYZabcdefghijklmnopqrstwxyz123456'
    init_state = list(init_state)
    output_state = code_trans(first_input, init_state)
    output_state = code_trans(second_input, output_state)

    return output_state


if __name__ == '__main__':

    # input data
    buffer = 'O'
    all_algs = alg_set_generator('O')
    train_algs = all_algs[0:27]
    train_times = {}
    # initial train times of every alg
    for x in train_algs:
        train_times[x] = 0

    input_code, train_times = random_codes(buffer, all_algs, train_algs, train_times)


    output_state = integrete_code('OBRFLIN', 'acegi')
    scrambler = (conn2ce(chichu2ce(output_state)))

    # print(input_code, train_times, output_state)
    print(scrambler)

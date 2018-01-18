#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this function generator algorithms set from input buffers

def alg_set_generator(corner_buffer, edge_buffer):

    # global cube state(0-23 mean corners; 24-47 mean edges; 48-55 mean centre). It's a constant.
    global_state = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'W', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'X', 'Y', 'Z',
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y', 'z',
                    '1', '2', '3', '4', '5', '6')

    # relative positions of two buffers in global_state
    c_buffer_pos = global_state.index(corner_buffer) // 3
    e_buffer_pos = (global_state.index(edge_buffer) - 24) // 2

    # add corner alg set
    corner_alg = []
    for i in range(24):
        first_pos = i // 3
        # first code
        if first_pos != c_buffer_pos:
            for j in range(24):
                second_pos = j // 3
                if second_pos != first_pos and second_pos != c_buffer_pos:
                    corner_alg.append(''.join([global_state[i], global_state[j]]))

    # add edge alg set
    edge_alg = []
    for i in range(24):
        first_pos = i // 2
        if first_pos != e_buffer_pos:
            for j in range(24):
                second_pos = j // 2
                if second_pos != first_pos and second_pos != e_buffer_pos:
                    edge_alg.append(''.join([global_state[i+24], global_state[j+24]]))

    return(corner_alg, edge_alg)

# test input data
# corner_buffer = 'O'
# edge_buffer = 'a'
# print(alg_set_generator(corner_buffer, edge_buffer))
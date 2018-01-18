#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('./lib')
sys.path.append('./cubers')

from ex_code import ex_code

# this function transfer state with input code and input state

input_code = 'OIY'
input_state = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'W', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'X', 'Y', 'Z',
               'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y', 'z',
               '1', '2', '3', '4', '5', '6']

# first code(generally it's the buffer)
first_code = input_code[1]

output_state = input_state[:len(input_state)]

for x in range(1, len(input_code)):
    output_state = ex_code([input_code[0], input_code[1]], output_state)
    output_state = ex_code([input_code[0], input_code[2]], output_state)

print(output_state)

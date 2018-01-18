#!/usr/bin/env python
# -*- coding: utf-8 -*-


# this function transfer state with input code and input state

def code_trans(input_code, input_state):

    """
    # test input data
    input_code = 'angqy'
    input_state = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'W', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'X', 'Y', 'Z',
                   'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                   'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y', 'z',
                   '1', '2', '3', '4', '5', '6']
    """

    # first assign input to output
    output_state = input_state[:len(input_state)]

    # transfer code by exchanging every two code. (1 a-n; 2 a-g; 3 a-q; 4 a-y)
    for x in range(1, len(input_code)):
        output_state = ex_code([input_code[0], input_code[x]], output_state)

    return output_state


# Input two codes and state and output the state with exchanging of the two codes
def ex_code(input_code, input_state):

    """
    # test input data
    input_code = 'OI'
    # input_code = 'af'
    # input_code = '12'
    input_state = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                   'W', 'M', 'N', 'Y', 'Z', 'X', 'R', 'S', 'T', 'Q', 'O', 'P',
                   'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                   'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y', 'z',
                   '1', '2', '3', '4', '5', '6']
    """

    # global cube state(0-23 mean corners; 24-47 mean edges; 48-55 mean centre). It's a constant.
    global_state = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'W', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'X', 'Y', 'Z',
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y', 'z',
                    '1', '2', '3', '4', '5', '6')

    # recognize which group current code is.(corner, edge or centre)
    div, index_num = group_recog(input_code[0])


    # the indexes of two code in global_state
    index_1 = global_state.index(input_code[0]) - index_num
    index_2 = global_state.index(input_code[1]) - index_num

    # assign input_state to output_state
    output_state = input_state[:len(input_state)]
    # exchange two position of codes with new order
    for x in range(0, div):
        output_state[re_order(index_1, div)[x] + index_num] = input_state[re_order(index_2, div)[x] + index_num]
        output_state[re_order(index_2, div)[x] + index_num] = input_state[re_order(index_1, div)[x] + index_num]

    # test output
    # print(output_state)
    return output_state


# this function defines the exchanging order
# input a number and divisor, output a list with new order
# for example, input(1,3) to output [1 2 0];(17,3) to [17 15 16]; (5,2) to output (5,4).
def re_order(num, div):
    # if input (17, 3) the first of list will be 15
    order_first = (num // div) * div

    if div == 3:
        # extend 17 to [15 16 17 15 16 17]
        order_double = [order_first, order_first + 1, order_first + 2,
                        order_first, order_first + 1, order_first + 2]
        # re_order list from 17, and output 17 15 16&
        order_output = [order_double[order_double.index(num)],
                        order_double[order_double.index(num) + 1],
                        order_double[order_double.index(num) + 2]]
    elif div == 2:
        order_double = [order_first, order_first + 1,
                        order_first, order_first + 1]
        order_output = [order_double[order_double.index(num)],
                        order_double[order_double.index(num) + 1]]
    else:
        order_double = [order_first,
                        order_first]
        order_output = [order_double[order_double.index(num)]]
    return order_output

def group_recog(input_code):
    # if it's corner code, then the divisor(orientations) will be 3 and it's first num is 0. edge's are 2 and 24....
    if ord(input_code) >= 65 and ord(input_code) <= 90:
        div = 3
        index_num = 0
    elif ord(input_code) >= 97 and ord(input_code) <= 122:
        div = 2
        index_num = 24
    else:
        div = 1
        index_num = 48

    return div, index_num


# testing script
"""
input_code = 'angqy'
input_state = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'W', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'X', 'Y', 'Z',
               'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y', 'z',
               '1', '2', '3', '4', '5', '6']
print(code_trans(input_code, input_state))
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request

# this function input ce_code to CE and calculate moves of this state

def conn2ce(url_input):

    url_head = 'http://127.0.0.1:8081/?'
    url_all = ''.join([url_head, ''.join(url_input)])

    str = urllib.request.urlopen(url_all).read()
    moves = str[14:-18]

    return moves

# this function tranform chichu's code to CE's code for calculate moves with CE(cube explorer)
# (some variables are pasted from matlab, so ignore the abnormal variables' names)

def chichu2ce(input_state):

    # cube's code in chichu with chichu's order
    final = 'ABCDEFGHIJKLWMNOPQRSTXYZabcdefghijklmnopqrstwxyz123456'
    # cube's code in CE with chichu's order
    color = 'uflulbubrurfdlfdbldrbdfrufuluburdfdldbdrfrflblbrudfbrl'
    # code's code in chichu with CE's order (the face's order is urfdlb）
    order = 'DeGc1gAaJKhIr5zZpSBbLs3qNjYWiXk2oOmREdCx6tQlMHfFy4wTnP'
    # DeGc1gAaJ KhIr5zZpS BbLs3qNjY WiXk2oOmR EdCx6tQlM HfFy4wTnP (this line is set to check clearly)

    chichu = []
    ce_code = []

    for x in range(0, len(input_state)):
        chichu.append(input_state[final.index(order[x])])
        ce_code.append(color[final.index(chichu[x])])

    # output is cube's code in CE with CE's order
    return(ce_code)

"""
input_state = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'W', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'X', 'Y', 'Z',
               'y', 'z', 'c', 'd', 'e', 'f', 'n', 'm', 'i', 'j', 'k', 'l',
               'b', 'a', 'o', 'p', 'g', 'h', 's', 't', 'w', 'x', 'q', 'r',
               '1', '2', '3', '4', '5', '6']

print(conn2ce(chichu2ce(input_state)))
"""

import sys
sys.path.append('./lib')
sys.path.append('./cubers')

from flask import Flask, request, g
app = Flask(__name__)

# import tiny db
from tiny_db import TinyDb

# import all cubers algorithm in the file "cuber_algorithm.py"
from cuber_algorithm import *
from random_alg import *
from ce import *


def get_db():
    '''
    return the tiny db instance.
    if not initialized, instantiate and bind it to the flask's global variable(aka g) 
    '''
    if not hasattr(g, "tiny_db"):
        g.tiny_db = TinyDb("./data/")
    return g.tiny_db

@app.route('/user_age/<name>')
def user_email(name):
    # doing the exact same work as db.execute(xxxxxx)
    # first get the tiny db instance
    db = get_db()
    # then query the specified user's information
    result = db.find("user", name)
    # get the age from result
    age = result["age"]
    # make sure age is a float type
    age = float(age)
    # call the function written in the cuber_algorithm.py
    years = 10
    age_later = age_after(age, years)
    return "%s's current age: %d; after %d years: %d" %(name, age, years, age_later)

@app.route('/user_alg/<name>/<range>')
def user_alg(name, range):
    # first get the tiny db instance
    db = get_db()
    # then query the specified user's information
    result = db.find("user", name)
    # get the age from result
    age = result["age"]
    # make sure age is a float type
    age = int(age)

    # buffer is constant in db. every user have different buffer. (there will be two buffers for corner and edge)
    buffer = 'O'
    # back-stage calculate all the all algs from buffer
    all_algs = alg_set_generator('O')
    # user need to input, upload or choose the algs they want to train.
    # I didn't have idea about interaction yet. so I simple this part to input range in all_algs
    train_algs = all_algs[0:int(range)]

    # initial the training times for every alg in train_algs. (there will be more than one train_algs)
    train_times = {}
    for x in train_algs:
        train_times[x] = 0

    # cube's init_state
    init_state = 'ABCDEFGHIJKLWMNOPQRSTXYZabcdefghijklmnopqrstwxyz123456'
    init_state = list(init_state)

    # get a input_code for CE to calculate scrambler, and get the training times for every training alg
    input_code, train_times = random_codes(buffer, all_algs, train_algs, train_times)
    # transform input_code to the cube's state in chichu
    output_state = code_trans(input_code, init_state)
    # transform chichu state to CE state, and push it to CE to get scrambler
    scrambler = conn2ce(chichu2ce(output_state))

    # the content user need to see is the scramble
    # and they can also check how many times they trained for a specific alg
    return "%s's training scarmble is %s with alg training set as following <br /> <br /> <br />%s" % (name, scrambler, train_algs)

if __name__ == '__main__':
    app.run()
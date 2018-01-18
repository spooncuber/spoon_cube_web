import sys
sys.path.append('./lib')
sys.path.append('./cubers')

from flask import Flask, request, g
app = Flask(__name__)

# import tiny db
from tiny_db import TinyDb

# import all cubers algorithm in the file "cuber_algorithm.py"
from cuber_algorithm import *


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
    

if __name__ == '__main__':
    app.run()
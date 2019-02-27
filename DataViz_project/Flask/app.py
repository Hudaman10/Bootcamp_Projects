import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, jsonify, render_template

#################################################
# Database Setup
#################################################
#Creating Database Connection
connection_string = "root:Piccolo7979@localhost/ncaa_db"
engine = create_engine(f'mysql://{connection_string}')


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
players = Base.classes.ncaa_info
geography = Base.classes.geo_states

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



### Webpage routes

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/index.html")
def index2():
    """Additional homepage landing"""
    return render_template("index.html")

@app.route("/data.html")
def data():
    """Return data page"""
    return render_template("data.html")

@app.route("/visualizations.html")
def viz():
    """Return data page"""
    return render_template("visualizations.html")

@app.route("/about.html")
def about():
    """Return about page"""
    return render_template("about.html")



@app.route("/states")
def by_state():

    #Grabbing state retention numbers
    player_count = session.query(players.birth_state, func.count(players.birth_state),\
        geography.latitude, geography.longitude).join(geography, geography.name == players.birth_state).\
        group_by(players.birth_state, geography.latitude, geography.longitude).all()

    #Converting to dictionary and exporting as json
    player_dic_list = []
    for item in player_count:
        player_dic = {}
        player_dic["state"] = item[0]
        player_dic["count"] = item[1]  
        player_dic["latitude"] = item[2]
        player_dic["longitude"] = item[3]
        player_dic_list.append(player_dic)

    return jsonify(player_dic_list)

@app.route("/colleges")
def by_college():

    #Grabbing colleges with the most pros
    college_count = session.query(players.college, func.count(players.college)).\
        group_by(players.college).order_by(func.count(players.college).desc()).all()
    
    #Converting to dictionary to export as json
    college_dic_list2 = []
    for item in college_count:
        college2_dic = {}
        college2_dic["college"] = item[0]
        college2_dic["player_count"] = item[1]
        college_dic_list2.append(college2_dic)

    return jsonify(college_dic_list2)


@app.route("/state_retention")
def state_retention():

    #Grabbing number of players who played college ball in their homestate
    state_ret = session.query(players.college_state, func.count(players.college_state),\
        geography.latitude, geography.longitude).join(geography, geography.name == players.college_state)\
        .filter(players.birth_state == players.college_state).\
        group_by(players.college_state, geography.latitude, geography.longitude).all()
    
   #Converting to dictionary to export as json
    state_dic_list = []
    for item in state_ret:
        state_dic = {}
        state_dic["college"] = item[0]
        state_dic["player_count"] = item[1]  
        state_dic["latitude"] = item[1]
        state_dic["longitude"] = item[2]
        state_dic_list.append(state_dic)

    return jsonify(state_dic_list)

@app.route("/college_retention")
def college_retention():

    #Grabbing colleges in-state retention numbers
    college_ret = session.query(players.college, func.count(players.college), players.college_state)\
        .filter(players.birth_state == players.college_state).group_by(players.college, players.college_state).all()

    #Converting to dictionary to export as json
    college_dic_list = []
    for item in college_ret:
        college_dic = {}
        college_dic["college"] = item[0]
        college_dic["player_count"] = item[1]
        college_dic["college_state"] = item[2]
        college_dic_list.append(college_dic)

    return jsonify(college_dic_list)


@app.route("/leaftest.html")
def leaf():
    """Additional homepage landing"""
    return render_template("leaftest.html")

@app.route("/charttest.html")
def chart():
    """Additional homepage landing"""
    return render_template("charttest.html")



if __name__ == "__main__":
    app.run()

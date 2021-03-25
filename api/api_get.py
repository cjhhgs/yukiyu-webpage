from flask import Flask
from flask import request
import json
import os
import sys
 
import bilibili

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/bangumi')
def get_bangumi_info():
    bangumi = bilibili.get_all()
    return bangumi
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
    target_url = 'https://bangumi.bilibili.com/web_api/timeline_global'
    # !You should modify this when the working directory changed
    img_folder = os.path.abspath('./upload/bangumi_img')
    apis = bilibili.api_get(target_url)
    bangumi_list = bilibili.get_today_list(apis)
    bangumi = bilibili.get_bangumi(bangumi_list)
    bilibili.img_save(bangumi, img_folder)
    return bangumi

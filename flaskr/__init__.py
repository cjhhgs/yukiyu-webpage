import os
from flask import Flask, render_template, request, redirect, session, flash
import get_last_week
from user import userVerify
from databaseCURD import getDatabase

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'div'
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/yukiyu')
    def index_page():
        return render_template('index.html')

    @app.route('/yukiyu/main')
    def main_page():
        return render_template('main.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        if request.method == 'POST':
            if userVerify(request.form.get('username'), request.form.get('password')):              
                session['user'] = (request.form.get('username'), request.form.get('password'))
                return render_template('main.html', user = session['user'])
            else:
                flash('用户不存在或密码错误')
                return redirect('/login')

    @app.route('/yukiyu/database', methods=['GET', 'POST'])
    def database_page():
        if request.method == 'GET':
            agrs = request.args
            if agrs:
                res = getDatabase(agrs)
                return res
            return render_template('database.html')
        else:



    @app.route('/bangumi')
    def get_bangumi_info():
        bangumi = get_last_week.get_last_week()
        return bangumi

    # @app.route('/lastweek')
    # def get_last_week_info():
    #     last_week = get_last_week.get_last_week()
    #     return last_week

    # @app.route('/login', methods=['POST'])


    return app



if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=80,
        debug=True
    )
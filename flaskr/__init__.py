import os
from flask import Flask, render_template, request, redirect, session, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import get_last_week
from user import userVerify, User, get_user, create_user
from databaseCURD import getDatabase, commitChangeToDatabase
import json

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'div'
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )
    login_manager = LoginManager()  # 实例化登录管理对象
    login_manager.init_app(app)  # 初始化应用
    login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint
    
    @login_manager.user_loader  # 定义获取登录用户的方法
    def load_user(user_id):
        return User.get(user_id)

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
        print('main_page func called')
        userame = None
        if hasattr(current_user, 'username'):
            userame = current_user.username
        print('current user: ', userame)
        return render_template('main.html', user = userame)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html', target = '/login', way = '登陆')
        if request.method == 'POST':
            user_name = request.form.get('username')
            password = request.form.get('password')
            user_info = get_user(user_name)
            emsg = None
            if user_info is None:
                emsg = '该用户名不存在'
            else:
                user = User(user_info)
                if user.verify_password(password):  # 校验密码
                    login_user(user)  # 创建用户 Session
                    # return redirect(request.args.get('next') or url_for('main_page'))
                else:
                    emsg = "密码有误"

            if emsg is None:
                return redirect(request.args.get('next') or '/yukiyu/main')
                # return render_template(request.args.get('next') or 'main.html', user = current_user.username)
            else:
                flash(emsg)
                return redirect('/login')
            # if userVerify(request.form.get('username'), request.form.get('password')):              
            #     session['user'] = (request.form.get('username'), request.form.get('password'))
            #     return render_template('main.html', user = session['user'])
            # else:
            #     flash('用户不存在或密码错误')
            #     return redirect('/login')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('login.html', target = '/register', way = '注册')
        else:
            user_name = request.form.get('username')
            password = request.form.get('password')
            create_user(user_name, password)
            flash('创建用户成功，请登陆')
            return redirect('/login')

    
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect('/yukiyu')

    @app.route('/yukiyu/database', methods=['GET', 'POST'])
    @login_required
    def database_page():
        if request.method == 'GET':
            agrs = request.args
            if agrs:
                res = getDatabase(agrs)
                return res
            return render_template('database.html')
        else:           
            res = json.loads(request.data)
            print('get data:')
            print(res)
            returnStatus = commitChangeToDatabase(res['oldInfo'], res['newInfo'], res['tableName'])
            return 'return status: ' + str(returnStatus)



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
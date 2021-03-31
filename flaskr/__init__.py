import os
from flask import Flask, render_template
import get_last_week


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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
    def main_page():
        return render_template('index.html')

    @app.route('/bangumi')
    def get_bangumi_info():
        bangumi = get_last_week.get_last_week()
        return bangumi

    # @app.route('/lastweek')
    # def get_last_week_info():
    #     last_week = get_last_week.get_last_week()
    #     return last_week

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=80,
        debug=True
    )
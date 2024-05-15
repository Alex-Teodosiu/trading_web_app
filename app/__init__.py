import os

from flask import Flask, render_template, redirect, session, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
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

    # Make the the session variable globally available to all templates using the context processor
    @app.context_processor
    def inject_token():
        return dict(token=session.get('token'))

    @app.route('/')
    def landing():
        return render_template('landing.html')
    
    @app.route('/home/profile')
    def profile():
        return render_template('home/profile.html')
    
    #register blueprint as part of the factory function
    from app.models import auth
    app.register_blueprint(auth.bp)

    from app.models import home 
    app.register_blueprint(home.bp)

    from app.models import tradingaccount
    app.register_blueprint(tradingaccount.bp)

    from app.models import market
    app.register_blueprint(market.bp)

    from app.models import algorithm
    app.register_blueprint(algorithm.bp)

    from app.models import historicaltrades
    app.register_blueprint(historicaltrades.bp)


    return app

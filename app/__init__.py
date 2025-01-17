import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)
    cors = CORS(app)

    # set configz
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from .views.views import views
    from .api.api import api

    app.register_blueprint(views)
    app.register_blueprint(api)

    #The thing to handle the error 400 as a message.
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            "status":"error",
            "error":e.description
        }), 400

    #The thing to handle the error 404 as a message.
    @app.errorhandler(404)
    def not_found_error(e):
        return jsonify({
            "status":"error",
            "error":e.description
        }), 404

    #The thing to handle the error 500 as a message.
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({
            "status":"error",
            #This wasn't suppose to happen. HAHA, LOL
            "error":"this wasn't suppose to happen"
        })

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app

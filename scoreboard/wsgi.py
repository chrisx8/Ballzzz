import os
import api
import config
from flask import Flask
from flask_restful import Api
from views import views

# create the webapp and api instances
app = Flask(__name__, instance_relative_config=True)
app_api = Api(app)

# load the instance config
app.config.from_mapping(
    SECRET_KEY=config.SECRET_KEY
)

# add api resources
app_api.add_resource(api.PublishScore, '/api/score/')

# register views
app.register_blueprint(views)


# serve static files
@views.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

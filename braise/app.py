#!/usr/bin/env python
import os
from flask import Flask, abort, request, jsonify, g, url_for, render_template
from flask_restful import Api
from flask.ext.cors import CORS
from models.db import db
from controllers.health import Health
from controllers.users import UserController, UserAuthController
from controllers.documents import DocumentController,\
                                DocumentClassifyController
from controllers.predictions import PredictionController
from controllers.news import NewsController
import config
import requests

##
## Initialization
##
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

##
## Extensions
##
db.init_app(app)

##
## API Routing
##
api.add_resource(Health, '/api/health')
api.add_resource(UserController, '/api/users')
api.add_resource(DocumentController, '/api/documents')
api.add_resource(DocumentClassifyController,
                 '/api/documents/<document_id>/classify')
api.add_resource(PredictionController, '/api/predictions')
api.add_resource(NewsController, '/api/news')

##
## Template Rendering
##
articles = [
    {'id': 0, 'title': 'article 1', 'body': 'here is some text'},
    {'id': 1, 'title': 'article 2', 'body': 'more text'},
]
@app.route('/')
def hello(name=None):
    r = requests.get('http://localhost:5000/api/news')
    articles = r.json()['data']
    generating = None
    if 'generating' in articles:
        articles = []
        generating = True
    return render_template('index.html',
                           articles=articles,
                           generating=generating)

##
## Run App
##
if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        with app.app_context():
            print 'creating db'
            db.create_all()
    app.run(debug=True, threaded=True, host='0.0.0.0')

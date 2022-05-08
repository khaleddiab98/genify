from flask import Flask, request
from flask_restful import Resource, Api
from api.predicter import Run_Model
import json

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'message':'Hello World!'}

api.add_resource(HelloWorld, '/')
api.add_resource(Run_Model, '/run_model/')

if __name__ == '__main__':
    app.run(debug = True)
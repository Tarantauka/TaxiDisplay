# Import the framework
from flask import Flask, g, jsonify, render_template
from flask_restful import Resource, Api, reqparse
from json import dumps
import TaxiPoses

app = Flask(__name__,static_url_path='')
api = Api(app)



@app.route('/')
def index():
    
    return render_template('map.html')


@app.route('/all')
def allPoses():
    
    return render_template('mapyu.html')

class UberPoses(Resource):
    def get(self):
         return jsonify(TaxiPoses.getUpdatedPosits("uberx"))

class YandexPoses(Resource):
    def get(self):
         return jsonify(TaxiPoses.getUpdatedPosits("econom"))

class SplitPoses(Resource):
    def get(self):
         return jsonify(
             uber = TaxiPoses.getUpdatedPosits("uberx"), 
             yandex = TaxiPoses.getUpdatedPosits("econom"))

class UnitedPoses(Resource):
    def get(self):
        result = TaxiPoses.getUpdatedPosits("uberx") + TaxiPoses.getUpdatedPosits("econom")
        return jsonify(result)

api.add_resource(UberPoses, '/uberposes')
api.add_resource(SplitPoses, '/splitposes')
api.add_resource(UnitedPoses, '/poses')
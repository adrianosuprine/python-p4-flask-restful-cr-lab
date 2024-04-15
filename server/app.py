#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        response_dict_list = [plant.to_dict() for plant in Plant.query.all()] 
        return jsonify(response_dict_list)
    
    def post(self):
        data = request.get_json()
        if not data or 'name' not in data or 'image' not in data or 'price' not in data:
            return make_response(jsonify({"error": "Missing required data"}), 400)

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(jsonify(new_plant.to_dict()), 201)
api.add_resource(Plants, '/plants')
class PlantByID(Resource):
    def get(self,id):
        plant = Plant.query.filter_by(id = id).first()
        if plant:
            return jsonify(plant.to_dict())
        else:
            return jsonify({'message':'Plant not found'}), 404
        

api.add_resource(PlantByID, '/plants/<int:id>')
if __name__ == '__main__':
    app.run(port=5555, debug=True)

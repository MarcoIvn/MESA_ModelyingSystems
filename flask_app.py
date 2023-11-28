from flask import Flask, jsonify, request
from agents import Car
from server import get_model_instance
from threading import Thread

app = Flask(__name__)

@app.route('/get_car_positions', methods=['GET'])
def get_car_positions():
    model = get_model_instance()
    car_positions = []
    for agent in model.schedule.agents:
        if isinstance(agent, Car):
            car_positions.append({"id": agent.unique_id, "position": agent.pos})
    return jsonify(car_positions)
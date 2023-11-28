from flask import Flask, jsonify, request
from agents import Car
from server import get_model_instance
from server import server
from threading import Thread

app = Flask(__name__)

@app.route('/get_car_positions', methods=['GET'])
def get_car_positions():
    model = get_model_instance()
    model.step()
    car_positions = []
    for agent in model.schedule.agents:
        if isinstance(agent, Car):
            car_positions.append({"id": agent.unique_id, "position": agent.pos})
    return jsonify(car_positions)

def run_mesa():
    server.launch(open_browser=True)

def run_flask():
    app.run(port=5000, debug=True, use_reloader=False)

if __name__ == '__main__':

    # Thread for the Flask app
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    flask_thread.join()

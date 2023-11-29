from flask import Flask, jsonify, request
from agents import Car
from server import get_model_instance
from server import server
from threading import Thread

app = Flask(__name__)

@app.route('/get_car_positions', methods=['GET'])
def get_car_positions():
    model = get_model_instance()
    car_positions = []
    for agent in model.schedule.agents:
        if isinstance(agent, Car):
            car_positions.append({"id": agent.unique_id, "position": agent.pos})
    model.step()
    return jsonify(car_positions)

@app.route('/get_semaphore', methods=['GET'])
def get_semaphore():
    model = get_model_instance()
    semaphore_status = model.get_semaphore_status()
    return jsonify(semaphore_status)

def run_mesa():
    server.launch(open_browser=True)

def run_flask():
    app.run(port=5000, debug=True, use_reloader=False)

if __name__ == '__main__':

    # Thread for the Flask app
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    flask_thread.join()

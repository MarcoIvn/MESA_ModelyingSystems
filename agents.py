import mesa
import numpy as np
import heapq
import math
import random

class Buildings(mesa.Agent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

class ParkingSpots(mesa.Agent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

class RoundAbout(mesa.Agent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

class Stop(mesa.Agent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

class Go(mesa.Agent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

class Car(mesa.Agent):
    def __init__(self, unique_id, pos, model, destination_parking_lot,directions):
        super().__init__(unique_id, model)
        self.pos = pos
        self.destination_parking_lot = destination_parking_lot
        self.path = []  # Path to follow
        self.directions = directions
        self.color = self.generate_random_color()

    def generate_random_color(self):
        while True:
            r = random.randint(20, 100)
            g = random.randint(20, 100)
            b = random.randint(20, 100)
            if r > g and r > b and g > 50 and b > 50:
                continue

            return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def dijkstra(self, start, goal, avoid_position=None):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while frontier:
            current_cost, current_node = heapq.heappop(frontier)

            if current_node == goal:
                break

            for next_node in self.neighbors(current_node, avoid_position):
                new_cost = cost_so_far[current_node] + 1
                if (
                    next_node not in cost_so_far
                    or new_cost < cost_so_far[next_node]
                ):
                    cost_so_far[next_node] = new_cost
                    heapq.heappush(frontier, (new_cost, next_node))
                    came_from[next_node] = current_node

        # Reconstruct path from goal to start
        path = []
        current = goal
        while current != start:
            if current not in came_from:
                # Path not founded, car must wait
                return []
            current = came_from[current]
            path.append(current)

        path.reverse()

        # Last coord to path
        path.append(goal)

        return path


    def neighbors(self, node, avoid_position=None):
        available_directions = self.directions[node[0]][node[1]].split(',')
        neighbors = []
        for direction in available_directions:
            new_neighbor = None
            if direction == 'UP':
                new_neighbor = (node[0], node[1] + 1)
            elif direction == 'DOWN':
                new_neighbor = (node[0], node[1] - 1)
            elif direction == 'LEFT':
                new_neighbor = (node[0] - 1, node[1])
            elif direction == 'RIGHT':
                new_neighbor = (node[0] + 1, node[1])

            if new_neighbor and new_neighbor != avoid_position:
                neighbors.append(new_neighbor)

        neighbors = [(x, y) for (x, y) in neighbors if 0 <= x < self.model.width and 0 <= y < self.model.height]
        return neighbors

    
    def find_alternative_path(self, avoid_position):
        start = self.pos
        goal = self.destination_parking_lot
        return self.dijkstra(start, goal,avoid_position)

    def move_towards_destination(self):
        if not self.path:
            # If the path is empty, generate a new path to the destination
            start = self.pos
            goal = self.destination_parking_lot
            self.path = self.dijkstra(start, goal)
            print(self.path)

        # Check if the next position has a Stop agent
        next_position = self.path[0] if self.path else self.pos
        stop_agents = [
            agent for agent in self.model.schedule.agents
            if isinstance(agent, Stop) and agent.pos == next_position
        ]

        if stop_agents:
            return
        # Check if the next position is occupied by another car
        car_agents = [
            agent for agent in self.model.schedule.agents
            if isinstance(agent, Car) and agent.pos == next_position and agent != self
        ]

        if car_agents:
            print(f"Car {self.unique_id} encontró otro carro en su próxima posición.")
            avoid_position = car_agents[0].pos if car_agents else None
            alternative_path = self.find_alternative_path(avoid_position)
            if alternative_path != []:
                self.path = alternative_path
                print(f"Car {self.unique_id} ha encontrado un camino alternativo.")
            else:
                print(f"Car {self.unique_id} está esperando a que el otro coche se mueva.")
                return
        # Move along the path
        if self.path:
            next_position = self.path.pop(0)
            self.model.grid.move_agent(self, next_position)

    def step(self):
        self.move_towards_destination()
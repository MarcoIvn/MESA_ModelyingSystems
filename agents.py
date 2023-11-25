import mesa
import numpy as np
import heapq
import math

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
    def __init__(self, unique_id, pos, model, destination_parking_lot):
        super().__init__(unique_id, model)
        self.pos = pos
        self.destination_parking_lot = destination_parking_lot
        self.path = []  # Path to follow

    def dijkstra(self, start, goal, obstacles):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while frontier:
            current_cost, current_node = heapq.heappop(frontier)

            if current_node == goal:
                break

            for next_node in self.neighbors(current_node, obstacles):
                new_cost = cost_so_far[current_node] + 1
                if (
                    next_node not in cost_so_far
                    or new_cost < cost_so_far[next_node]
                ):
                    cost_so_far[next_node] = new_cost
                    heapq.heappush(frontier, (new_cost, next_node))
                    came_from[next_node] = current_node

        # Reconstruct path from goal to start
        path = [goal]
        current = goal
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def neighbors(self, node, obstacles):
        if node in obstacles:
            return []  # No permitir movimiento desde obstáculos
        return self.model.grid.get_neighborhood(node, moore=True, include_center=False)

    def move_towards_destination(self):
        if not self.path:
            # If the path is empty, generate a new path to the destination
            start = self.pos
            goal = self.destination_parking_lot
            obstacles = [
                agent.pos for agent in self.model.schedule.agents
                if isinstance(agent, (Buildings, ParkingSpots, RoundAbout))
            ]
            self.path = self.dijkstra(start, goal, obstacles)
            print(self.path)

        # Check if the next position has a Stop agent
        next_position = self.path[0] if self.path else self.pos
        stop_agents = [
            agent for agent in self.model.schedule.agents
            if isinstance(agent, Stop) and agent.pos == next_position
        ]

        if stop_agents:
            # There is a Stop agent at the next position, so don't move
            return

        # Move along the path
        if self.path:
            next_position = self.path.pop(0)
            self.model.grid.move_agent(self, next_position)

    def step(self):
        self.move_towards_destination()
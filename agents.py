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

    def heuristic(self, a, b):
        """Calculate the Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar(self, start, goal):
        """A* algorithm to find the path from start to goal."""
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while frontier:
            current_cost, current_node = heapq.heappop(frontier)

            if current_node == goal:
                break

            for next_node in self.model.grid.get_neighborhood(
                current_node, moore=True, include_center=False
            ):
                new_cost = cost_so_far[current_node] + 1
                if (
                    next_node not in cost_so_far
                    or new_cost < cost_so_far[next_node]
                ):
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current_node

        # Reconstruct path from goal to start
        path = [goal]
        current = goal
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def move_towards_destination(self):
        if not self.path:
            # If the path is empty, generate a new path to the destination
            start = self.pos
            goal = self.destination_parking_lot
            self.path = self.astar(start, goal)
            print(self.path)

        # Move along the path
        if self.path:
            next_position = self.path.pop(0)
            self.model.grid.move_agent(self, next_position)

    def step(self):
        self.move_towards_destination()

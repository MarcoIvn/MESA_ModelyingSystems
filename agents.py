import mesa
import numpy as np

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
    def __init__(self, unique_id, pos, model,destination_parking_lot):
        super().__init__(unique_id, model)
        self.pos = pos
        self.destination_parking_lot = destination_parking_lot

    def step(self):
        # Get the current position
        x, y = self.pos

        # Check if the next position is within the grid
        if x + 1 < self.model.width:
            new_x = x + 1
            new_y = y
        else:
            # If at the end of the road, wrap around to the beginning
            new_x = 0
            new_y = y

        # Check if the next position is not blocked by another agent   THIS PART OF THE CODE IS TO TEMPORARILY IGNORE STOP AND GO AGENTS AS OBSTACLES
        next_cell_contents = self.model.grid.get_cell_list_contents([(new_x, new_y)])
        if len(next_cell_contents) == 0:
            self.model.grid.move_agent(self, (new_x, new_y))
        else:
            next_agent = next_cell_contents[0]  # Assuming only one agent can be in a cell
            if isinstance(next_agent, (Stop, Go)):
                if isinstance(next_agent, Stop):
                    print("STOP")
                    self.model.grid.move_agent(self, (new_x, new_y))
                    pass
                elif isinstance(next_agent, Go):
                    print("GO")
                    self.model.grid.move_agent(self, (new_x, new_y))
                    pass
        
        '''
        # Check if the next position is not blocked by another agent
        if self.model.grid.is_cell_empty((new_x, new_y)):
            # Move the car to the new position
            self.model.grid.move_agent(self, (new_x, new_y))
        '''
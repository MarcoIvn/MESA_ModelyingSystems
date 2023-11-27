import mesa
from agents import *
from scheduler import RandomActivationByTypeFiltered
import csv

class StreetView(mesa.Model):

    description = "MESA Visualization of the street cross simulation."
    def step(self):
         # Check if it's time to switch the lights every 20 steps
        if self.step_count > 25 :
            self.switch_lights()
            self.step_count = 0
            

        self.schedule.step()  # Call the step method for all agents
        self.datacollector.collect(self)  # Collect data for visualization
        self.step_count += 1
    
    def switch_lights(self):
        for agent in self.schedule.agents:
            if isinstance(agent, Stop):
                agent.__class__ = Go  # Change the class to Go
            elif isinstance(agent, Go):
                agent.__class__ = Stop  # Change the class to Stop
    
    def load_directions(self, filename="Directions - Hoja 1.csv"):
        directions = []

        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row

            rows = list(reader)

            for col in range(1, len(rows[0])):  # Iterate over columns, starting from the second column
                direction_col = [row[col].strip() for row in rows]
                direction_col.reverse()  # Invertir el orden de los datos en cada subarray
                directions.append(direction_col)

        return directions



    def __init__(
        self,
        width=25,
        height=25,
        building_positions=[(2, 21), (3, 21), (4, 21), (5, 21), (6, 21), (7, 21), (8, 21), (9, 21),           (11, 21), (12, 21),                   (17, 21), (18, 21),                (21, 21), (22, 21),
                                     (3, 20), (4, 20), (5, 20), (6, 20), (7, 20), (8, 20), (9, 20), (10, 20), (11, 20), (12, 20),                   (17, 20),                          (21, 20), (22, 20),
                            (2, 19), (3, 19), (4, 19), (5, 19), (6, 19), (7, 19), (8, 19), (9, 19), (10, 19), (11, 19),                             (17, 19), (18, 19),                          (22, 19),
                            (2, 18), (3, 18), (4, 18), (5, 18), (6, 18),          (8, 18), (9, 18), (10, 18), (11, 18), (12, 18),                   (17, 18), (18, 18),                (21, 18), (22, 18),
                            
                            (2, 15), (3, 15), (4, 15),                   (7, 15),          (9, 15), (10, 15), (11, 15), (12, 15),                   (17, 15), (18, 15),                (21, 15), (22, 15),
                            (2, 14), (3, 14), (4, 14),                   (7, 14), (8, 14), (9, 14), (10, 14), (11, 14), (12, 14),                   (17, 14), (18, 14),                (21, 14),
                            (2, 13), (3, 13),                            (7, 13), (8, 13), (9, 13), (10, 13), (11, 13),                                       (18, 13),                (21, 13), (22, 13),
                            (2, 12), (3, 12), (4, 12),                   (7, 12), (8, 12), (9, 12), (10, 12), (11, 12), (12, 12),                   (17, 12), (18, 12),                (21, 12), (22, 12),
                            
                            
                            
                            
                            (2, 7), (3, 7), (4, 7), (5, 7),                           (8, 7), (9, 7), (10, 7), (11, 7), (12, 7),                    (17, 7), (18, 7), (19, 7), (20, 7), (21, 7), (22, 7),
                                    (3, 6), (4, 6), (5, 6),                           (8, 6), (9, 6), (10, 6), (11, 6), (12, 6),                    (17, 6),          (19, 6),          (21, 6), (22, 6),
                            (2, 5), (3, 5), (4, 5), (5, 5),                           (8, 5), (9, 5), (10, 5), (11, 5), (12, 5),
                            (2, 4), (3, 4), (4, 4), (5, 4),                           (8, 4), (9, 4), (10, 4), (11, 4), (12, 4),
                            (2, 3), (3, 3), (4, 3),                                           (9, 3), (10, 3), (11, 3), (12, 3),                    (17, 3), (18, 3), (19, 3),          (21, 3), (22, 3),
                            (2, 2), (3, 2), (4, 2), (5, 2),                           (8, 2), (9, 2), (10, 2), (11, 2), (12, 2),                    (17, 2), (18, 2), (19, 2), (20, 2), (21, 2), (22, 2)],

        parkingSpots_positions=[(10, 21), (2, 20), (12, 19), (7, 18), (8, 15), (4, 13), (12, 13), (2, 6), (5, 3), (8, 3), (18, 20), (17, 13), (18, 6), (21, 19), (22, 14), (20, 6), (20, 3)],

        roundAbout_positions = [(14, 10), (15, 10), (14, 9), (15, 9)],
        stop_positions = [(15, 21), (16, 21), (5, 15), (6, 15), (0, 12), (1, 12), (23, 7), (24, 7), (13, 2), (14, 2), (15, 3), (16, 3)],
        go_positions = [(17, 23), (17, 22), (7, 17), (7, 16), (2, 11), (2, 10), (22, 9), (22, 8), (17, 5), (17, 4), (12, 1), (12, 0)],
        car_positions=[((14, 8), (18,20)),((14,7), (2,6)),((5,10), (10,21)),((0,0), (8,15)),((24,23), (5,3)),((0,1),(8,3)),((0,23),(21,19)),((2,8),(18,6))], 
    ):
        self.step_count = 0

        self.directions = self.load_directions()
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.building_positions = building_positions if building_positions else []
        self.parkingSpots_positions = parkingSpots_positions if parkingSpots_positions else []
        self.roundAbout_positions = roundAbout_positions if roundAbout_positions else []
        self.stop_positions = stop_positions if stop_positions else []
        self.go_positions = go_positions if go_positions else []
        self.car_positions = car_positions if car_positions else []

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=False)
        self.datacollector = mesa.DataCollector(
            {
                "Buildings": lambda b: b.schedule.get_type_count(Buildings),
                "Parking Spots": lambda p: p.schedule.get_type_count(ParkingSpots),
                "Round About": lambda r: r.schedule.get_type_count(RoundAbout),
                "Stop": lambda s: s.schedule.get_type_count(Stop),
                "Go": lambda g: g.schedule.get_type_count(Go),
                "Cars": lambda c: c.schedule.get_type_count(Car),
            }
        )

        # Create buildings at specified positions
        for pos in reversed(self.building_positions):
            x, y = pos
            building = Buildings(self.next_id(), (x, y), self)
            self.grid.place_agent(building, (x, y))
            self.schedule.add(building)

        # Create parking spots at specified positions
        for pos in reversed(self.parkingSpots_positions):
            x, y = pos
            parkingSpot = ParkingSpots(self.next_id(), (x, y), self)
            self.grid.place_agent(parkingSpot, (x, y))
            self.schedule.add(parkingSpot)

        # Create round about
        for pos in reversed(self.roundAbout_positions):
            x, y = pos
            roundAbout = RoundAbout(self.next_id(), (x, y), self)
            self.grid.place_agent(roundAbout, (x, y))
            self.schedule.add(roundAbout)

        # Create stop 
        for pos in reversed(self.stop_positions):
            x, y = pos
            stop = Stop(self.next_id(), (x, y), self)
            self.grid.place_agent(stop, (x, y))
            self.schedule.add(stop)

        # Create go
        for pos in reversed(self.go_positions):
            x, y = pos
            go = Go(self.next_id(), (x, y), self)
            self.grid.place_agent(go, (x, y))
            self.schedule.add(go)

        # Create car
        for (pos, destination_parking_lot) in reversed(self.car_positions):
            x, y = pos
            car = Car(self.next_id(), (x, y), self, destination_parking_lot,self.directions)
            self.grid.place_agent(car, (x, y))
            self.schedule.add(car)

        self.running = True
        self.datacollector.collect(self)
        

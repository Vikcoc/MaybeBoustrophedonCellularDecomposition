from combine_event import CombineEvent
from destroy_event import DestroyEvent
from map_obstacle_vertex import MapObstacleVertex
from spawn_event import SpawnEvent
from split_event import SplitEvent


class MapObstacle:
    def __init__(self, points: [[]]):
        # points are assumed to be in trigonometric order
        self.Points = [MapObstacleVertex(y[0], y[1]) for y in points]
        self.Points[-1].NextPoint = self.Points[0]
        self.Points[-1].PrevPoint = self.Points[-2]

        for i in range(len(self.Points) - 1):
            self.Points[i].PrevPoint = self.Points[i - 1]
            self.Points[i].NextPoint = self.Points[i + 1]

        self.SplitEvents = []
        self.generate_split_events()

        self.CombineEvents = []
        self.generate_combine_events()

        self.SpawnEvents = []
        self.generate_spawn_events()

        self.DestroyEvents = []
        self.generate_destroy_events()

    def generate_split_events(self):
        cycled = False
        i = 0
        while not cycled:
            j = i + 1
            if j >= len(self.Points):
                j = 0
                cycled = True
            while self.Points[i].X == self.Points[j].X:
                j = j + 1
                if j >= len(self.Points):
                    j = 0
                    cycled = True

            if self.Points[i].PrevPoint.X > self.Points[i].X and self.Points[j].X > self.Points[i].X \
                    and self.collision_parity(self.Points[i]) == 0:
                self.SplitEvents.append(SplitEvent(self.Points[i], self.Points[j - 1]))

            i = j

    def generate_combine_events(self):
        cycled = False
        i = 0
        while not cycled:
            j = i + 1
            if j >= len(self.Points):
                j = 0
                cycled = True
            while self.Points[i].X == self.Points[j].X:
                j = j + 1
                if j >= len(self.Points):
                    j = 0
                    cycled = True

            if self.Points[i].PrevPoint.X < self.Points[i].X and self.Points[j].X < self.Points[i].X \
                    and (self.collision_parity(self.Points[i]) == 1 and not self.Points[i].is_protrusion()
                         or self.collision_parity(self.Points[i]) == 0 and self.Points[i].is_protrusion()):
                self.CombineEvents.append(CombineEvent(self.Points[j - 1], self.Points[i]))

            i = j

    def __str__(self):
        return f'Obstacle made of the points {self.Points} \nWith the split events {self.SplitEvents} \nWith combine ' \
               f'events {self.CombineEvents} '

    def __repr__(self):
        return self.__str__()

    def collision_parity(self, point: MapObstacleVertex):
        if point.is_protrusion():
            collision_count = 2
        elif point.Y == point.NextPoint.Y and point.X < point.NextPoint.X:  # special case for bottom left split
            collision_count = 2
        else:
            collision_count = 1
        for other in self.Points:
            if point == other:
                continue
            collision_count = collision_count + point.intersections(other)
        # split protrusion always even
        # spawn protrusion always odd
        # normal split always even
        # normal spawn always odd

        # combine protrusion always even
        # destroy protrusion always odd
        # normal combine always odd
        # normal destroy always even

        return (collision_count // 1) % 2

    def generate_spawn_events(self):
        cycled = False
        i = 0
        while not cycled:
            j = i + 1
            if j >= len(self.Points):
                j = 0
                cycled = True
            while self.Points[i].X == self.Points[j].X:
                j = j + 1
                if j >= len(self.Points):
                    j = 0
                    cycled = True

            if self.Points[i].PrevPoint.X > self.Points[i].X and self.Points[j].X > self.Points[i].X \
                    and self.collision_parity(self.Points[i]) == 1:
                self.SpawnEvents.append(SpawnEvent(self.Points[j - 1], self.Points[i]))

            i = j

    def generate_destroy_events(self):
        cycled = False
        i = 0
        while not cycled:
            j = i + 1
            if j >= len(self.Points):
                j = 0
                cycled = True
            while self.Points[i].X == self.Points[j].X:
                j = j + 1
                if j >= len(self.Points):
                    j = 0
                    cycled = True

            if self.Points[i].PrevPoint.X < self.Points[i].X and self.Points[j].X < self.Points[i].X \
                    and (self.collision_parity(self.Points[i]) == 0 and not self.Points[i].is_protrusion()
                         or self.collision_parity(self.Points[i]) == 1 and self.Points[i].is_protrusion()):
                self.DestroyEvents.append(DestroyEvent(self.Points[i], self.Points[j - 1]))

            i = j

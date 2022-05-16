from map_obstacle_vertex import MapObstacleVertex


class SplitEvent:
    def __init__(self, top: MapObstacleVertex, bot: MapObstacleVertex):
        self.X = top.X
        self.PointOnTop = top
        self.PointOnBottom = bot

    def __str__(self):
        return f'Split: Top: {self.PointOnTop}, Bot: {self.PointOnBottom}'

    def __repr__(self):
        return self.__str__()

# just a dto as far as i think

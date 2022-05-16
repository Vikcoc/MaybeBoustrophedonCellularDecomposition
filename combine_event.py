from map_obstacle_vertex import MapObstacleVertex


class CombineEvent:
    def __init__(self, top: MapObstacleVertex, bot: MapObstacleVertex):
        self.X = top.X
        self.PointOnTop = top
        self.PointOnBottom = bot
        self.CellOnTop = None
        self.CellOnBottom = None

    # def __str__(self):
    #     return f'Combine: Top: {self.PointOnTop}, Bot: {self.PointOnBottom}, TopCell: {self.CellOnTop}' \
    #            f', BotCell: {self.CellOnBottom}'

    def __str__(self):
        return f'Combine: Top: {self.PointOnTop}, Bot: {self.PointOnBottom}'

    def __repr__(self):
        return self.__str__()


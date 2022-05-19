from map_obstacle_vertex import MapObstacleVertex


class SearchSpace:
    def __init__(self, corners):
        self.TopLeft = MapObstacleVertex(*corners[0])
        self.BotLeft = MapObstacleVertex(*corners[1])
        self.TopRight = MapObstacleVertex(*corners[2])
        # adding for the off chance that an obstacle ends on the search space
        self.TopRight.NextPoint = self.TopRight
        self.BotRight = MapObstacleVertex(*corners[3])
        self.BotRight.PrevPoint = self.BotRight

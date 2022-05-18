from map_obstacle_vertex import MapObstacleVertex


class SearchSpace:
    def __init__(self, top_left: [], bot_left: [], top_right: [], bot_right: []):
        self.TopLeft = MapObstacleVertex(*top_left)
        self.BotLeft = MapObstacleVertex(*bot_left)
        self.TopRight = MapObstacleVertex(*top_right)
        # adding for the off chance that an obstacle ends on the search space
        self.TopRight.NextPoint = self.TopRight
        self.BotRight = MapObstacleVertex(*bot_right)
        self.BotRight.PrevPoint = self.BotRight

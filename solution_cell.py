from map_obstacle_vertex import MapObstacleVertex


class SolutionCell:
    def __init__(self, top_left: MapObstacleVertex, bot_left: MapObstacleVertex, max_top_right: MapObstacleVertex,
                 max_bot_right: MapObstacleVertex):
        self.TopLeft = top_left
        self.BotLeft = bot_left
        self.MaxTopRight = max_top_right
        self.MaxBotRight = max_bot_right
        self.TopRight = None
        self.BotRight = None
        self.Children = []
        self.TopCombineEvent = None
        self.BotCombineEvent = None

    def __str__(self):
        return f'[{self.TopLeft}, {self.BotLeft}, {self.BotRight}, {self.TopRight},:, {self.MaxBotRight}, ' \
               f'{self.MaxTopRight}]'

    def __repr__(self):
        return '\n' + self.__str__()

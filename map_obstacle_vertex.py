class MapObstacleVertex:
    def __init__(self, x: float, y: float):
        self.X = x
        self.Y = y
        self.PrevPoint = None
        self.NextPoint = None

    def __str__(self):
        return f'[{self.X}, {self.Y}]'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

    def intersections(self, bot_point):
        if bot_point == self or bot_point.Y >= self.Y:
            return 0
        # if bot_point.Y == self.Y:
        #     intersections = 0
        #     if self.X <= bot_point.PrevPoint.X and bot_point.PrevPoint.Y == self.Y:
        #         intersections = intersections + 1
        #     if self.X <= bot_point.NextPoint.X and bot_point.NextPoint.Y == self.Y:
        #         intersections = intersections + 1
        #     return intersections

        intersections = 0
        if bot_point.PrevPoint is not None and bot_point.PrevPoint.Y >= self.Y and bot_point.PrevPoint != self:
            percent = (self.Y - bot_point.Y) / (bot_point.PrevPoint.Y - bot_point.Y)
            new_point_x = bot_point.X * (1 - percent) + bot_point.PrevPoint.X * percent
            if new_point_x >= self.X:
                intersections = intersections + 1

        if bot_point.NextPoint is not None and bot_point.NextPoint.Y >= self.Y and bot_point.NextPoint != self:
            percent = (self.Y - bot_point.Y) / (bot_point.NextPoint.Y - bot_point.Y)
            new_point_x = bot_point.X * (1 - percent) + bot_point.NextPoint.X * percent
            if new_point_x >= self.X:
                intersections = intersections + 1
        return intersections

    def is_protrusion(self):
        return self.PrevPoint.Y > self.Y and self.NextPoint.Y > self.Y or \
                self.PrevPoint.Y < self.Y and self.NextPoint.Y < self.Y

from map_obstacle import MapObstacle
from map_obstacle_vertex import MapObstacleVertex
from solution_cell import SolutionCell


class CellAlgorithm:
    def __init__(self, search_space):
        self.SearchSpace = search_space
        self.SplitEventsOrdered = []
        self.CombineEventsOrdered = []
        self.SpawnEventsOrdered = []
        self.DestroyEventsOrdered = []
        self.Obstacles = []
        self.CellQueue = []
        self.FatherlessCells = []

    def add_obstacles(self, obstacles):
        self.Obstacles = [MapObstacle(x) for x in obstacles]
        for obstacle in self.Obstacles:
            self.SplitEventsOrdered.extend(obstacle.SplitEvents)
            self.CombineEventsOrdered.extend(obstacle.CombineEvents)
            if any(obstacle.SpawnEvents):
                self.SpawnEventsOrdered.extend(obstacle.SpawnEvents)
            if any(obstacle.DestroyEvents):
                self.DestroyEventsOrdered.extend(obstacle.DestroyEvents)

        self.SplitEventsOrdered.sort(key=lambda x: x.X)
        self.CombineEventsOrdered.sort(key=lambda x: x.X)
        self.SpawnEventsOrdered.sort(key=lambda x: x.X)
        self.DestroyEventsOrdered.sort(key=lambda x: x.X)

    def __str__(self):
        return f'Splits: {self.SplitEventsOrdered}\nCombines: {self.CombineEventsOrdered}\n' \
               f'Spawns: {self.SpawnEventsOrdered}\nDestroys: {self.DestroyEventsOrdered}'

    def create_cell_from_space(self):
        cell = SolutionCell(self.SearchSpace.TopLeft, self.SearchSpace.BotLeft, self.SearchSpace.TopRight,
                            self.SearchSpace.BotRight)
        self.FatherlessCells.append(cell)
        self.CellQueue.append(cell)

    def create_fatherless_cells(self):
        for event in self.SpawnEventsOrdered:
            cell = SolutionCell(event.PointOnTop, event.PointOnBottom, event.PointOnTop.NextPoint,
                                event.PointOnBottom.PrevPoint)
            self.FatherlessCells.append(cell)
            self.CellQueue.append(cell)

    @staticmethod
    def if_in_trapezoid(top_left, bottom_left, top_right, bottom_right, point: MapObstacleVertex):
        if top_left.X > point.X or top_right.X < point.X:
            return False
        if max(top_left.Y, top_right.Y) < point.Y or min(bottom_left.Y, bottom_right.Y) > point.Y:
            return False
        percent = (point.X - top_left.X) / (top_right.X - top_left.X)
        if top_left.Y * (1 - percent) + top_right.Y * percent < point.Y \
                or bottom_left.Y * (1 - percent) + bottom_right.Y * percent > point.Y:
            return False
        return True

    @staticmethod
    def get_cell_provisional_end(cell: SolutionCell):
        if cell.MaxTopRight.X == cell.MaxBotRight.X:
            return cell.MaxTopRight, cell.MaxBotRight
        if cell.MaxTopRight.X < cell.MaxBotRight.X:
            percent = (cell.MaxTopRight.X - cell.BotLeft.X) \
                      / (cell.MaxBotRight.X - cell.BotLeft.X)
            y = cell.BotLeft.Y * (1 - percent) + cell.MaxBotRight.Y * percent
            return cell.MaxTopRight, MapObstacleVertex(cell.MaxTopRight.X, y)
        else:
            percent = (cell.MaxBotRight.X - cell.TopLeft.X) \
                      / (cell.MaxTopRight.X - cell.TopLeft.X)
            y = cell.TopLeft.Y * (1 - percent) + cell.MaxTopRight.Y * percent
            return MapObstacleVertex(cell.MaxBotRight.X, y), cell.MaxBotRight

    @staticmethod
    def make_cell_end(cell: SolutionCell, x: float):
        percent = (x - cell.BotLeft.X) \
                  / (cell.MaxBotRight.X - cell.BotLeft.X)
        bot_y = cell.BotLeft.Y * (1 - percent) + cell.MaxBotRight.Y * percent
        percent = (x - cell.TopLeft.X) \
                  / (cell.MaxTopRight.X - cell.TopLeft.X)
        top_y = cell.TopLeft.Y * (1 - percent) + cell.MaxTopRight.Y * percent
        cell.TopRight = MapObstacleVertex(x, top_y)
        cell.BotRight = MapObstacleVertex(x, bot_y)

    def find_splits_in_cell(self, cell: SolutionCell):
        cell_end = self.get_cell_provisional_end(cell)
        splits = [e for e in self.SplitEventsOrdered if cell.TopLeft.X < e.X < cell_end[0].X and
                  self.if_in_trapezoid(cell.TopLeft, cell.BotLeft, cell_end[0], cell_end[1], e.PointOnTop)]
        if not any(splits):
            return splits
        min_x = min(splits, key=lambda x: x.X).X
        return [e for e in splits if e.X == min_x]

    def process_next_cell(self):
        first_cell = self.CellQueue[0]
        self.CellQueue.pop(0)
        splits = self.find_splits_in_cell(first_cell)
        if not any(splits):
            cell_end = self.get_cell_provisional_end(first_cell)
            first_cell.TopRight = cell_end[0]
            first_cell.BotRight = cell_end[1]
            destroy_event = next((e for e in self.DestroyEventsOrdered if cell_end[0] == e.PointOnTop
                                  or cell_end[1] == e.PointOnBottom), None)
            if destroy_event is not None:
                return first_cell

            if first_cell.TopRight == self.SearchSpace.TopRight and first_cell.BotRight == self.SearchSpace.BotRight:
                return first_cell

            combine_event_top = next((e for e in self.CombineEventsOrdered if cell_end[0] == e.PointOnBottom), None)
            combine_event_bot = next((e for e in self.CombineEventsOrdered if cell_end[1] == e.PointOnTop), None)

            if combine_event_top is not None:
                combine_event_top.CellOnBottom = first_cell
                first_cell.TopCombineEvent = combine_event_top
                while combine_event_top.CellOnTop is not None \
                        and combine_event_top.CellOnTop.TopCombineEvent:
                    combine_event_top = combine_event_top.CellOnTop.TopCombineEvent
            if combine_event_bot is not None:
                combine_event_bot.CellOnTop = first_cell
                first_cell.BotCombineEvent = combine_event_bot
                while combine_event_bot.CellOnBottom is not None \
                        and combine_event_bot.CellOnBottom.BotCombineEvent:
                    combine_event_bot = combine_event_bot.CellOnBottom.BotCombineEvent

            if (combine_event_top is None or combine_event_top.CellOnTop is not None
                    and combine_event_top.CellOnTop.TopCombineEvent is None) and \
                (combine_event_bot is None or combine_event_bot.CellOnBottom is not None
                    and combine_event_bot.CellOnBottom.BotCombineEvent is None):
                first_cell.Children.append(
                    SolutionCell(first_cell.TopRight if combine_event_top is None
                                 else combine_event_top.CellOnTop.TopRight,

                                 first_cell.BotRight if combine_event_bot is None
                                 else combine_event_bot.CellOnBottom.BotRight,

                                 #  if it is not in a combine event, the max can also be the end of the cell
                                 (first_cell.MaxTopRight
                                  if first_cell.MaxTopRight is not first_cell.TopRight
                                  else first_cell.MaxTopRight.NextPoint)
                                 if combine_event_top is None
                                 else combine_event_top.CellOnTop.MaxTopRight,

                                 (first_cell.MaxBotRight
                                  if first_cell.MaxBotRight is not first_cell.BotRight
                                  else first_cell.MaxBotRight.PrevPoint)
                                 if combine_event_bot is None
                                 else combine_event_bot.CellOnBottom.MaxBotRight))
        else:
            self.make_cell_end(first_cell, splits[0].X)
            splits.sort(key=lambda x: x.PointOnTop.Y, reverse=True)
            first_cell.Children.append(SolutionCell(first_cell.TopRight, splits[0].PointOnTop, first_cell.MaxTopRight,
                                                    splits[0].PointOnTop.PrevPoint))
            for i in range(len(splits) - 1):
                first_cell.Children.append(SolutionCell(splits[i].PointOnBottom, splits[i + 1].PointOnTop,
                                                        splits[i].PointOnBottom.NextPoint,
                                                        splits[i + 1].PointOnTop.PrevPoint))
            first_cell.Children.append(SolutionCell(splits[-1].PointOnBottom, first_cell.BotRight,
                                                    splits[-1].PointOnBottom.NextPoint,
                                                    first_cell.MaxBotRight))
        self.CellQueue.extend(first_cell.Children)
        return first_cell

    # def complete_first_cell_and_start_new(self):
    # @staticmethod
    # def get_cell_end_x(cell):
    # def check_if_first_cell_will_split(self): or get_first_cell_split(self)
    # def check_if_first_cell_will_combine(self): or get_first_cell_split(self)
    # @staticmethod
    # def set_cell_missing_corner(cell):
    # def split_first_cell_in_two(self, splitEvent):
    # def combine_first_cell_in_one(self, combineEvent): with the other cell saved in combineEvent
    # def move_first_cell_to_next(self):
# do not forget vertical checks if there are more split events on the same x or combine events
# and cells that die
# and how tf do you differentiate between split and spawn

class SpawnEvent:
    def __init__(self, top, bot):
        self.X = top.X
        self.PointOnTop = top
        self.PointOnBottom = bot

    def __str__(self):
        return f'Spawn: Top: {self.PointOnTop}, Bot: {self.PointOnBottom}'

    def __repr__(self):
        return self.__str__()

# just a dto as far as i think

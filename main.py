from cell_algorithm import CellAlgorithm
from search_space import SearchSpace
from solution_cell import SolutionCell
from plot_layout import Map


def dfs_cells(cell_algorithm: CellAlgorithm):
    for cell in cell_algorithm.FatherlessCells:
        dfs_recursion(cell)


def dfs_recursion(cell: SolutionCell):
    print(cell)
    for child in cell.Children:
        dfs_recursion(child)


if __name__ == "__main__":
    #obstacles = [[0, 2], [-2, 0], [3, 0], [3, 2]]
    space = [[-3, 6], [-3, -5], [3.5, 6], [3.5, -5]]
    #obstacles = [[0, 0], [2.9, 0], [2, 0.5], [2, 1.5], [3, 2], [0, 2], [1, 1.5], [1, 0.5]]
    obstacles = [[[-2.5, -2], [0.5, -2.5], [-1, 1], [0, 5.5], [-1.5, 5]], [[-0.5, 0.5], [2, -1], [3, 5], [2, 5.5], [2.5, 4.5]]]
    x = CellAlgorithm(SearchSpace(space))
    x.add_obstacles(obstacles)
    Map.__init__(space[1], space[2])
    Map.BuildLayout(space)
    Map.MapPoints(obstacles)
    x.create_cell_from_space()
    x.create_fatherless_cells()
    Cells = []
    while any(x.CellQueue):
        cell = x.process_next_cell()
        topLeft = [cell.TopLeft.X, cell.TopLeft.Y]
        topRight = [cell.TopRight.X, cell.TopRight.Y]
        botLeft = [cell.BotLeft.X, cell.BotLeft.Y]
        botRight = [cell.BotRight.X, cell.BotRight.Y]
        maxBotRight = [cell.MaxBotRight.X, cell.MaxBotRight.Y]
        maxTopRight = [cell.MaxTopRight.X, cell.MaxTopRight.Y]
        Cells.append([topLeft, botLeft, topRight, botRight, maxTopRight, maxBotRight])
        #Map.PlotCells([topLeft, botLeft, topRight, botRight, maxTopRight, maxBotRight])
        
    Map.PlotFromCells(Cells)
    dfs_cells(x)
    Map.Show()

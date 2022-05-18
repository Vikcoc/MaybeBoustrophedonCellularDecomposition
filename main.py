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
    x = CellAlgorithm(SearchSpace([-5, 10], [-5, -10], [5, 10], [5, -10]))
    x.add_obstacles([
        [[0, 0], [2.9, 0], [2, 0.5], [2, 1.5], [3, 2], [0, 2], [1, 1.5], [1, 0.5]]
    ])
    Map.__init__()
    Map.BuildLayout([[-5, 10], [-5, -10], [5, 10], [5, -10]])
    Map.MapPoints([[0, 0], [2.9, 0], [2, 0.5], [2, 1.5], [3, 2], [0, 2], [1, 1.5], [1, 0.5]])
    #Map.Show()
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
        #print(list(map(float, str(TopLeft).strip('][').split(', '))))
        # print(x.CellQueue)
        # print()
    Map.PlotFromCells(Cells)
    dfs_cells(x)
    Map.Show()

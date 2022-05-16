from cell_algorithm import CellAlgorithm
from search_space import SearchSpace
from solution_cell import SolutionCell


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
    x.create_cell_from_space()
    x.create_fatherless_cells()
    while any(x.CellQueue):
        x.process_next_cell()
        # print(x.CellQueue)
        # print()

    dfs_cells(x)

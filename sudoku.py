import pathlib
import typing as tp
from random import sample

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    b = len(values)//n
    a = []
    for i in range(1, n+1):
        a.append(values[b*(i-1):b*i:])
    return a


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    a = []
    for i in range(0, len(grid)):
        a.append(grid[i][pos[1]])
    return a


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    pos_x_0 = (pos[0]//3)*3
    pos_y_0 = (pos[1]//3)*3
    a = []
    for i in range(3):
        for j in range(3):
            a.append(grid[pos_x_0+i][pos_y_0+j])
    return a


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if(grid[i][j] == '.'):
                return (i, j)


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    values = set(str(i) for i in range(1, 10))
    values = values - set(get_row(grid, pos))
    values = values - set(get_col(grid, pos))
    values = values - set(get_block(grid, pos))
    return values


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    emptypositions = find_empty_positions(grid)
    if(not emptypositions):
        return grid
    else:
        row, col = emptypositions
    for i in range(1, 10):
        if(str(i) in find_possible_values(grid, (row, col))):
            grid[row][col] = str(i)
            if(solve(grid)):
                return grid
            grid[row][col] = '.'
    return False


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    for i in solution:
        if sorted(list(set(i))) != sorted(i):
            return False
    columns = []
    for j in range(len(solution)):
        for k in range(len(solution)):
            if(solution[j][k] == '.'):
                return False
        for i in solution:
            columns += [i[j]]
        if sorted(list(set(columns))) != sorted(columns):
            return False
        columns = []
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """

    return None


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)

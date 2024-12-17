from queue import Queue

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines

# load maze from file
file_path = "maze.txt"
imported_maze = load_file(file_path)

maze = []
# maze = [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
#     [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
#     [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]

# convert the maze to an array
for line in imported_maze:
    row = []
    for char in line.strip():
        if char == '#':
            row.append(1)
        elif char == '.':
            row.append(0)
        elif char == 'E':
            start = (len(maze), len(row))
            row.append(0)
        elif char == 'S':
            end = (len(maze), len(row))
            row.append(0)
            print(end)
    maze.append(row)

# movement directions
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Right, Left, Down, Up

# BFS algorithm
def bfs(maze, start, end):
    queue = Queue()
    visited = set()

    # Initialize
    queue.put(start)
    visited.add(start)

    while not queue.empty():
        x, y = queue.get()
        if (x, y) == end:
            return f"Reached end at {end}!"

        # Explore all directions
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid(maze, new_x, new_y) and (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                queue.put((new_x, new_y))

    return "No path found."

def is_valid(maze, x, y):
    rows, cols = len(maze), len(maze[0])
    return 0 <= x < cols and 0 <= y < rows and maze[y][x] == 0

# Start BFS
print(bfs(maze, start, end))
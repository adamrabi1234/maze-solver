from queue import Queue
import matplotlib.pyplot as plt
import numpy as np

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines

# load maze from file
file_path = "maze.txt"
imported_maze = load_file(file_path)

maze = []

# Draw the maze by chatGPT
def draw_maze(maze, start, end):
    plt.figure(figsize=(10, 10))
    
    # Scale up each square by repeating the maze elements
    scale = 10  # Increase this value to make squares larger
    maze_large = np.kron(maze, np.ones((scale, scale)))
    
    # Display the maze with inverted colors
    plt.imshow(maze_large, cmap="gray_r", origin="upper")
    
    # Adjust start and end positions to the new scaled size
    start_scaled = (start[0] * scale + scale // 2, start[1] * scale + scale // 2)
    end_scaled = (end[0] * scale + scale // 2, end[1] * scale + scale // 2)
    
    # Mark the start (green) and end (red) points with smaller dots
    plt.scatter(start_scaled[1], start_scaled[0], c='green', s=50)  # Smaller size
    plt.scatter(end_scaled[1], end_scaled[0], c='red', s=50)        # Smaller size
    
    # Remove the axes
    plt.xticks([]), plt.yticks([])
    plt.show()


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
            new_x = x + dx
            new_y = y + dy
            if is_valid(maze, new_x, new_y) and (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                queue.put((new_x, new_y))

    return "No path found."

def is_valid(maze, x, y):
    rows = len(maze)
    cols = len(maze[0])
    return 0 <= x < cols and 0 <= y < rows and maze[y][x] == 0

# Start BFS
print(bfs(maze, start, end))
draw_maze(maze, start, end)
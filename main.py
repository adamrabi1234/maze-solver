import argparse
from queue import Queue
import matplotlib.pyplot as plt
import numpy as np

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines

# Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Solve a maze using BFS.")
    parser.add_argument("file_path", type=str, help="Path to the maze file.")
    return parser.parse_args()

# Draw the maze by chatGPT
def draw_maze(maze, start, end, path=None):
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
    
    # Plot the path if available
    if path:
        path_scaled = [(p[0] * scale + scale // 2, p[1] * scale + scale // 2) for p in path]
        path_x, path_y = zip(*path_scaled)
        plt.plot(path_y, path_x, c='blue', linewidth=2)  # Draw the path
    
    # Remove the axes
    plt.xticks([]), plt.yticks([])
    plt.show()

# Parse maze file and initialize maze structure
def initialize_maze(file_path):
    imported_maze = load_file(file_path)
    maze = []
    for line in imported_maze:
        row = []
        for char in line.strip():
            if char == '#':
                row.append(1)
            elif char == '.':
                row.append(0)
            elif char == 'S':
                start = (len(maze), len(row))
                row.append(0)
            elif char == 'E':
                end = (len(maze), len(row))
                row.append(0)
        maze.append(row)
    return maze, start, end

# movement directions
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up

# BFS algorithm
def bfs(maze, start, end):
    queue = Queue()
    visited = {}  # Use a dictionary to track visited nodes and their parent nodes
    
    # Initialize
    queue.put(start)
    visited[start] = None  # Start has no parent

    while not queue.empty():
        y, x = queue.get()  # Correctly use (row, column) order
        if (y, x) == end:
            return reconstruct_path(visited, start, end)

        # Explore all directions
        for dy, dx in directions:
            new_y = y + dy
            new_x = x + dx
            if is_valid(maze, new_y, new_x) and (new_y, new_x) not in visited:
                visited[(new_y, new_x)] = (y, x)  # Record the parent
                queue.put((new_y, new_x))

    return "No path found."

def reconstruct_path(visited, start, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = visited[current]  # Traverse backwards using the parent nodes
    path.reverse()
    return path

def is_valid(maze, y, x):
    rows = len(maze)
    cols = len(maze[0])
    return 0 <= y < rows and 0 <= x < cols and maze[y][x] == 0

# Main execution block
if __name__ == "__main__":
    args = parse_arguments()
    maze, start, end = initialize_maze(args.file_path)
    path = bfs(maze, start, end)
    print(f"Path: {path}")
    draw_maze(maze, start, end, path=path)

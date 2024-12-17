import argparse
from heapq import heappush, heappop
import matplotlib.pyplot as plt
import numpy as np

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines

# Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Solve a maze with minimal turns using BFS.")
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
    start, end = None, None
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

# Modified BFS to minimize turns
def bfs(maze, start, end):
    queue = []
    heappush(queue, (0, 0, start[0], start[1], (0, 1)))  # (total_score, steps, y, x, facing)
    visited = {}  # Track visited states with direction
    visited[(start[0], start[1], (0, 1))] = None

    while queue:
        total_score, steps, y, x, facing = heappop(queue)

        if (y, x) == end:
            print(f"Final Score: {total_score}")
            return reconstruct_path(visited, (y, x, facing))

        for dy, dx in directions:
            new_y, new_x = y + dy, x + dx
            turn_penalty = 1000 if (dy, dx) != facing else 0
            new_score = total_score + 1 + turn_penalty  # +1 for step, +1000 for turn
            new_steps = steps + 1

            if is_valid(maze, new_y, new_x) and (new_y, new_x, (dy, dx)) not in visited:
                visited[(new_y, new_x, (dy, dx))] = (y, x, facing)
                heappush(queue, (new_score, new_steps, new_y, new_x, (dy, dx)))
    
    return "No path found."

def reconstruct_path(visited, current):
    path = []
    while current:
        y, x, _ = current
        path.append((y, x))
        current = visited.get(current)
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
    draw_maze(maze, start, end, path=path)
import heapq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def heuristic(a, b):
    """Calculates the Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(came_from, current):
    """Reconstructs the path from the came_from dictionary."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def astar(grid, start, goal, visualize=True):
    """
    A* search algorithm with visualization.

    Args:
        grid: A NumPy array representing the grid (0 for open, 1 for obstacle).
        start: A tuple (row, col) representing the start coordinates.
        goal: A tuple (row, col) representing the goal coordinates.
        visualize: A boolean indicating whether to visualize the search.

    Returns:
        A tuple containing:
            - path: A list of (row, col) tuples representing the path, or None if no path is found.
            - visited: A set of (row, col) tuples representing the visited nodes.
            - animation_frames: (If visualize=True) A list of NumPy arrays representing the animation frames.

    """
    rows, cols = grid.shape
    open_set = [(0, start)]  # Priority queue: (f_score, node)
    came_from = {}  # Dictionary to reconstruct the path
    g_score = np.full(grid.shape, np.inf)
    g_score[start] = 0
    f_score = np.full(grid.shape, np.inf)
    f_score[start] = heuristic(start, goal)
    visited = set()
    animation_frames = [] if visualize else None

    while open_set:
        f, current = heapq.heappop(open_set)
        if current == goal:
            path = reconstruct_path(came_from, current)
            if visualize: animation_frames.append(np.copy(grid))  #Add final state
            return path, visited, animation_frames

        visited.add(current)
        if visualize: animation_frames.append(np.copy(grid))  #Add frame before expanding
        grid[current] = 2  # Mark as visited (2)

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Four directions
            neighbor = (current[0] + dr, current[1] + dc)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor] != 1:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, visited, animation_frames


def animate_search(frames, grid_shape):
    """Animates the A* search."""
    fig, ax = plt.subplots()
    im = ax.imshow(frames[0], cmap='gray', interpolation='nearest', vmin=0, vmax=2) # cmap='viridis'

    def update(i):
        im.set_array(frames[i])
        return im,

    ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=200, blit=True)
    plt.show()


# Example usage:
grid = np.zeros((10, 10), dtype=int)
# Add some random obstacles (adjust as needed)
obstacles = [(1, 2), (1, 4), (2, 1), (2, 6), (3, 3), (3, 7), (4, 4), (5, 1), (5, 8), (6, 5), (7, 2), (7, 9), (8, 6), (9, 3), (9, 8)]
for obs in obstacles:
    grid[obs] = 1

start = (0, 0)
goal = (9, 9)

path, visited, frames = astar(np.copy(grid), start, goal)

if path:
    print("Path found:", path)
    if frames:
        animate_search(frames, grid.shape)
else:
    print("No path found.")
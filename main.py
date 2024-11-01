import math
from scipy.optimize import linear_sum_assignment
import matplotlib.pyplot as plt
import numpy as np

lines = {
    (0, 0): (2, 3),
    (2, 1): (5, 2),
    (3, 4): (5, 5),
    (3, 6): (5, 5)
}

v = 0.00874714

blocked = [
    [(2, 3), (5,2)],
    [(5,2), (3,4)],
    [(3, 6), (5, 2)]
]

all_points = [item for pair in lines.items() for item in pair]

start_points = list(lines.keys())
end_points = list(lines.values())

def compare_points(point1, point2):
    return point1[0] == point2[0] and point1[1] == point2[1]

def generate_distances_matrix():
    times = [[0 for _ in range(len(all_points))] for _ in range(len(all_points))]
    points_list = list(all_points)
    for i, current_point in enumerate(points_list):
        for j, comparing_point in enumerate(points_list):

            distance = math.sqrt((current_point[0] - comparing_point[0]) ** 2 + (current_point[1] - comparing_point[1]) ** 2)
            time = distance / v
            indices = [i for i, x in enumerate(end_points) if x == current_point]

            times[i][j] = time

            if any(current_point == pair[0] and comparing_point == pair[1] for pair in blocked) or any(current_point == pair[1] and comparing_point == pair[0] for pair in blocked):
                times[i][j] = 1000000000000000  # or any other value to indicate it's blocked
                continue

            # if i == j:
            #     times[i][j] = 0
            #     continue
            if lines.get(current_point) and compare_points(comparing_point, lines.get(current_point)):
                times[i][j] = 0.01
                continue
            elif len(indices) > 0:
                for index in indices:
                    if start_points[index] == comparing_point:
                        times[i][j] = 0.01
                        break
                continue


    return times

matrix = np.array(generate_distances_matrix())

# Define the Nearest Neighbor Algorithm
def nearest_neighbor(distances):
    n = distances.shape[0]
    route = [0] # Start at city A
    visited = {0}
    while len(visited) < n:
        current_city = route[-1]
        nearest_city = min([(i, distances[current_city][i]) for i in range(n) if i not in visited], key=lambda x: x[1])[0]
        route.append(nearest_city)
        visited.add(nearest_city)
    route.append(0) # Return to city A
    return route

print(nearest_neighbor(matrix))
from collections import deque
from datetime import datetime
from pathlib import Path

import numpy as np

path = Path('data.txt')


def read_points():
    points = path.read_text().strip().split('\n')
    triangles = [eval(triangle) for triangle in points]
    return np.array(triangles)


def np_array_to_tuple(np_array):
    return (np_array[0], np_array[1])


def find_intersection(edges_list, point_index):
    intersections = [0 for a in edges_list]
    queue = deque()
    queue.append(point_index)
    visited_list = []
    for vertex in range(len(edges_list)):
        if vertex == point_index:
            visited_list.append(True)
        else:
            visited_list.append(False)
    # import pdb; pdb.set_trace()
    while queue:
        point = int(queue.popleft())
        for index in edges_list[point]:
            # import pdb; pdb.set_trace()
            if not visited_list[index]:
                intersections[index] = intersections[point] + 1
                visited_list[index] = True
                queue.append(index)
    return int(np.argmax(intersections))


def graph(triangles):
    edges_list = []
    indexes = make_indexes_for_edges(triangles)
    for (index, triangle) in enumerate(triangles):
        for first_edge_point in triangle:
            first_edge_point = np_array_to_tuple(first_edge_point)
            for second_edge_point in triangle:
                second_edge_point = np_array_to_tuple(second_edge_point)
                if first_edge_point[0] < second_edge_point[0]:  #Возможно ошибка в сортировке
                    edges_list.append((indexes[first_edge_point],
                                       indexes[second_edge_point], index))
                elif first_edge_point[0] == second_edge_point[0] \
                        and first_edge_point[1] > second_edge_point[1]:

                    edges_list.append((indexes[first_edge_point],
                                       indexes[second_edge_point], index))

    edges_list = sorting_edges(edges_list)

    new_edges = [[] for a in range(triangles.shape[0])]
    for i in range(len(edges_list) - 1):
        if edges_list[i][:-1] == edges_list[i + 1][:-1]:
            new_edges[edges_list[i][-1]].append(edges_list[i + 1][-1])
            new_edges[edges_list[i + 1][-1]].append(edges_list[i][-1])
    return new_edges


def sorting_edges(edges_list):
    number_of_elements = len(edges_list)
    middle_index = number_of_elements // 2
    half_of_edges = [0] * middle_index

    sorted_edges = [0 for a in range(number_of_elements)]

    for sorting_id in reversed(range(0, 2)):
        for i in range(number_of_elements):
            key = edges_list[i][sorting_id]
            half_of_edges[key % middle_index] += 1

        for i in range(1, middle_index):
            half_of_edges[i] += half_of_edges[i - 1]

        for i in range(number_of_elements):
            key = edges_list[i][sorting_id]
            sorted_edges[number_of_elements - half_of_edges[key
                         % middle_index]] = edges_list[i]
            half_of_edges[key % middle_index] -= 1
    return sorted_edges


def make_indexes_for_edges(triangles):
    indexes = {}
    index = 0
    for row in triangles:
        for column in row:
            point = np_array_to_tuple(column)
            if point not in indexes:
                indexes[point] = index
                index += 1
    return indexes


def main():
    triangles = read_points()
    start_time = datetime.now()
    edges_list = graph(triangles)
    intersection_number = find_intersection(edges_list, 0)
    print(f"time: {(datetime.now() - start_time).total_seconds() * 1000.0} msc")
    print(f"Maximum intersections: {intersection_number}")


if __name__ == '__main__':
    main()

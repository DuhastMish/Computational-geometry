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

    while queue:
        point = queue.popleft()
        for index in edges_list[point]:
            if not visited_list[index]:
                intersections[index] = intersections[point] + 1
                visited_list[index] = True
                queue.append(index)
    return np.array(intersections)


def graph(triangles):
    edges_list = []
    indexes = make_indexes_for_edges(triangles)
    for (index, triangle) in enumerate(triangles):
        for first_edge_point in triangle:
            first_edge_point = indexes[np_array_to_tuple(first_edge_point)]
            for second_edge_point in triangle:
                second_edge_point = indexes[np_array_to_tuple(second_edge_point)]
                if first_edge_point < second_edge_point:  #Возможно ошибка в сортировке
                    edges_list.append((first_edge_point, second_edge_point, index))
                # elif first_edge_point[0] == second_edge_point[0] \
                #         and first_edge_point[1] > second_edge_point[1]:

                #     edges_list.append((indexes[first_edge_point],
                #                        indexes[second_edge_point], index))
    sorted_edges_list = sorting_edges(edges_list)
    # assert edges_list_v1 == edges_list_v2
    new_edges = [[] for a in range(triangles.shape[0])]
    for i in range(len(sorted_edges_list) - 1):
        if sorted_edges_list[i][:-1] == sorted_edges_list[i + 1][:-1]:
            new_edges[sorted_edges_list[i][-1]].append(sorted_edges_list[i + 1][-1])
            new_edges[sorted_edges_list[i + 1][-1]].append(sorted_edges_list[i][-1])
    return new_edges


def sorting_edges(edges_list):
    queue = deque()
    queue.append([edges_list, 1])
    while queue:
        list_for_sorting, sorting_id = queue.pop()
        number_of_elements = len(list_for_sorting)
        middle_index = number_of_elements // 2
        half_of_edges = [0] * middle_index

        sorted_edges = [0 for a in range(number_of_elements)]
        for i in range(number_of_elements):
            key = list_for_sorting[i][sorting_id]
            half_of_edges[key % middle_index] += 1

        for i in range(1, middle_index):
            half_of_edges[i] += half_of_edges[i - 1]

        for i in range(number_of_elements):
            key = list_for_sorting[i][sorting_id]
            sorted_edges[number_of_elements - half_of_edges[key
                         % middle_index]] = list_for_sorting[i]
            half_of_edges[key % middle_index] -= 1
        if sorting_id == 0:
            return sorted_edges
        queue.append([sorted_edges, 0])

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
    intersection_number = np.argmax(find_intersection(edges_list, 0))
    # import pdb; pdb.set_trace()
    # test = np.argmax(intersection_number)
    intersection_number = max(find_intersection(edges_list, intersection_number))
    print(f"time: {(datetime.now() - start_time).total_seconds() * 1000.0} msc")
    print(f"Maximum intersections: {intersection_number}")


if __name__ == '__main__':
    main()

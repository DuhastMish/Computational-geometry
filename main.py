from pathlib import Path
import numpy as np

path = Path('data.txt')


def read_points():
    points = path.read_text().strip().split('\n')
    triangles = [eval(triangle) for triangle in points]
    return np.array(triangles)


def np_array_to_tuple(np_array):
    return (np_array[0], np_array[1])


def graph(triangles):
    edges_list = []
    indexes = make_indexes_for_edges(triangles)
    for index, triangle in enumerate(triangles):
        for first_edge_point in triangle:
            first_edge_point = np_array_to_tuple(first_edge_point)
            for second_edge_point in triangle:
                second_edge_point = np_array_to_tuple(second_edge_point)
                if first_edge_point[0] < second_edge_point[0]:  # Возможно здесь ошибка. Неправильная сортировка
                    edges_list.append((indexes[first_edge_point], indexes[second_edge_point], index))
                elif (first_edge_point[0] == second_edge_point[0]) and (
                        first_edge_point[1] > second_edge_point[1]):
                    edges_list.append((indexes[first_edge_point], indexes[second_edge_point], index))

    return edges_list


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
    edges_list = graph(triangles)


if __name__ == "__main__":
    main()

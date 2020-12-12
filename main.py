from pathlib import Path
import numpy as np

path = Path('data.txt')


def read_points():
    points = path.read_text().strip().split('\n')
    triangles = [eval(triangle) for triangle in points]
    return np.array(triangles)


def numpy_array_to_tuple(numpy_array):
    return (numpy_array[0], numpy_array[1])


def graph(triangles):
    edges_list = []
    for index, triangle in enumerate(triangles):
        edge = []
        for first_edge_point in triangle:
            first_edge_point = numpy_array_to_tuple(first_edge_point)
            for second_edge_point in triangle:
                second_edge_point = numpy_array_to_tuple(second_edge_point)
                if first_edge_point[0] < second_edge_point[0]:  # Возможно здесь ошибка. Неправильная сортировка
                    edge.append((first_edge_point, second_edge_point, index))
                elif (first_edge_point[0] == second_edge_point[0]) and (
                        first_edge_point[1] > second_edge_point[1]):
                    edge.append((first_edge_point, second_edge_point, index))

        edges_list.append(edge)

    return edges_list


def main():
    triangles = read_points()
    edges_list = graph(triangles)


if __name__ == "__main__":
    main()

from typing import List, Tuple
import networkx as nx
import matplotlib.pyplot as plt
from algorithmics.utils.coordinate import Coordinate
from algorithmics.enemy.asteroids_zone import AsteroidsZone
from algorithmics.enemy.black_hole import BlackHole
from algorithmics.enemy.enemy import Enemy
from algorithmics.enemy.radar import Radar
from algorithmics.helper import does_line_slice
from algorithmics.utils.coordinate import Coordinate
import dwave_networkx as dnx
from dwave_networkx.utils import binary_quadratic_model_sampler
import collections
from collections import deque

SIDES_OF_BLACK_HOLE = 30
POINTS_PER_UNIT_AREA = 1
DIST_IN_RADAR = 3

def get_weight(point1: Coordinate, point2):
    return point1.distance_to(point2)


# Navigator
def get_hashaka_points(black_holes: List[BlackHole]) -> List[Coordinate]:
    hasaka_points: List[Coordinate] = []
    for j in range(len(black_holes)):
        for i in range(j+1, len(black_holes)):
            if (black_holes[i].radius + black_holes[j].radius) == black_holes[i].center.distance_to(black_holes[j].center):
                hole1 = black_holes[i]
                hole2 = black_holes[j]
                hasaka_points.append(
                    Coordinate((hole1.radius*hole2.center.x + hole2.radius*hole1.center.x)/(hole1.radius + hole2.radius),
                               (hole1.radius*hole2.center.y + hole2.radius*hole1.center.y)/(hole1.radius + hole2.radius)))

    return hasaka_points


def create_paths_graph(source: Coordinate, targets: List[Coordinate],
                       enemies: List[Enemy]) -> nx.Graph():
    result_graph = nx.Graph()
    result_graph.add_node(source)

    radar_list = []
    for target in targets:
        result_graph.add_node(target)
    for enemy in enemies:
        if type(enemy) == Radar:
            radar_list.append(enemy)
            enemy.spray_points(POINTS_PER_UNIT_AREA)

        result_graph.add_nodes_from(enemy.get_borders(SIDES_OF_BLACK_HOLE))


    # creates edges:
    for point1 in result_graph.nodes:
        for point2 in result_graph.nodes:
            if point1 != point2:
                legal = True
                for enemy in enemies:
                    # checks if the path is legal and adds edge
                    if does_line_slice(point1, point2, enemy):
                        legal = False
                        break
                if legal:
                    result_graph.add_edge(point1, point2,
                                          weight=get_weight(point1, point2))

    for radar in radar_list:
        radar_points = radar.points + radar.borders

        for point in result_graph.nodes:
            if point not in radar_points:
                radar_points.append(point)

        for point1 in radar_points:
            for point2 in radar_points:
                if point1 != point2:
                    dist_between_points = get_weight(point1, point2)
                    if dist_between_points <= DIST_IN_RADAR:
                        legal = True
                        for enemy in enemies:
                            # checks if the path is legal and adds edge
                            if enemy not in radar_list and does_line_slice(point1, point2, enemy):
                                legal = False
                                break

                        if legal:
                            for radar in radar_list:
                                if point1.distance_to(radar.center) <= radar.radius or point2.distance_to(radar.center) <= radar.radius:
                                    if not radar.is_good_angle(point1, point2):
                                        legal = False
                                        break
                        if legal:
                            if point1 not in result_graph.nodes:
                                result_graph.add_nodes_from([point1])

                            if point2 not in result_graph.nodes:
                                result_graph.add_nodes_from([point2])

                            result_graph.add_edge(point1, point2,
                                                  weight=dist_between_points)


    return result_graph


def find_source_in_path(path: List[Coordinate], source: Coordinate):
    for i in range(len(path)):
        if path[i] == source:
            return i


def get_neighbor_from_the_right(path, targets):
    for i in range(1, len(path)):
        if path[i] in targets:
            return i


def get_neighbor_from_the_left(path, targets):
    for i in range(len(path) - 1, 0, -1):
        if path[i] in targets:
            return i


def path_length1(path, i):
    """returns the weight of the path from the source to the neighbor from the right"""
    path_to_point = path[:i]
    weight = 0
    for j in range(len(path_to_point)-1):
        weight += get_weight(path_to_point[j], path_to_point[j + 1])
    return weight


def path_length2(path, i):
    """returns the weight of the path from the source to the neighbor from the left"""
    path_to_point = path[i:]
    path_to_point.append(path[0])
    weight = 0
    for j in range(len(path_to_point)-1):
        weight += get_weight(path_to_point[j], path_to_point[j + 1])
    return weight


def calculate_path_mult_targets(G, source: Coordinate, targets: List[Coordinate], enemies: List[Enemy]):
    targets_with_start = targets[::]
    targets_with_start.append(source)
    tsp = nx.approximation.traveling_salesman_problem
    round_path = tsp(G, weight='weight', nodes=targets_with_start, cycle=True, method=None)

    source_index = find_source_in_path(round_path, source)
    # taking off the last coord so that it doesn't finish at the starting position:
    round_path_without_double = round_path[:len(round_path) - 1]
    round_path_deque = deque(round_path_without_double)
    # rotating the list so that the source is in the beginning:
    round_path_deque.rotate(len(round_path_without_double) - source_index)
    round_path_ordered_deque = round_path_deque

    # figuring out which branch should be removed
    round_path_ordered = list(collections.deque(round_path_ordered_deque))
    right_neighbor = get_neighbor_from_the_right(round_path_ordered, targets)
    left_neighbor = get_neighbor_from_the_left(round_path_ordered, targets)

    if path_length1(round_path_ordered, right_neighbor) > path_length2(round_path_ordered, left_neighbor):
        without_extra = round_path_ordered[right_neighbor:]
        without_extra_flipped = without_extra[::-1]
        final_path = without_extra_flipped.insert(0, source)
    else:
        final_path = round_path_ordered[:left_neighbor + 1]

    return final_path


def calculate_path(source: Coordinate, targets: List[Coordinate], enemies: List[Enemy], allowed_detection: float = 0) \
        -> Tuple[List[Coordinate], nx.Graph]:
    """Calculates a path from source to target without any detection

    Note: The path must start at the source coordinate and end at the target coordinate!

    :param source: source coordinate of the spaceship
    :param targets: target coordinate of the spaceship
    :param enemies: list of enemies along the way
    :param allowed_detection: maximum allowed distance of radar detection
    :return: list of calculated path waypoints and the graph constructed
    """
    try:
        G = create_paths_graph(source, targets, enemies)
        if len(targets) > 1:
            return calculate_path_mult_targets(G, source, targets, enemies), G
        else:
            return nx.shortest_path(G, source, targets[0], "weight"), G
    except:
        return [source] + targets, G

def combine_graph(radar_graph: nx.Graph(), all_graph: nx.Graph()) -> nx.Graph():
    """combines radar graph to regular graph"""
    new_graph = nx.compose(radar_graph, all_graph)
    return new_graph










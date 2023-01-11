from typing import List, Tuple

import networkx as nx

from algorithmics.enemy.asteroids_zone import AsteroidsZone
from algorithmics.enemy.black_hole import BlackHole
from algorithmics.enemy.enemy import Enemy
from algorithmics.enemy.radar import Radar
from algorithmics.helper import does_line_slice
from algorithmics.utils.coordinate import Coordinate

SIDES_OF_BLACK_HOLE = 30
POINTS_PER_UNIT_AREA = 1
DIST_IN_RADAR = 3

def get_weight(point1: Coordinate, point2):
    return point1.distance_to(point2)


# Navigator

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


def calculate_path(source: Coordinate, targets: List[Coordinate],
                   enemies: List[Enemy], allowed_detection: float = 0) \
        -> Tuple[List[Coordinate], nx.Graph]:
    """Calculates a path from source to target without any detection

    Note: The path must start at the source coordinate and end at the target coordinate!

    :param source: source coordinate of the spaceship
    :param targets: target coordinate of the spaceship
    :param enemies: list of enemies along the way
    :param allowed_detection: maximum allowed distance of radar detection
    :return: list of calculated path waypoints and the graph constructed
    """
    G = create_paths_graph(source, targets, enemies)

    return nx.shortest_path(G, source, targets[0], "weight"), G
    # return [source] + targets, nx.DiGraph()

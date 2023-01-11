from typing import List, Tuple

import networkx as nx

from algorithmics.enemy.asteroids_zone import AsteroidsZone
from algorithmics.enemy.black_hole import BlackHole
from algorithmics.enemy.enemy import Enemy
from algorithmics.enemy.radar import Radar
from algorithmics.utils.coordinate import Coordinate


def get_weight(point1: Coordinate, point2):
    return point1.distance_to_squared(point2)


# Navigator

def create_paths_graph(source: Coordinate, targets: List[Coordinate], enemies: List[Enemy]) -> nx.Graph():
    result_graph = nx.Graph()
    result_graph.add_node(source)
    for target in targets:
        result_graph.add_node(target)
    for enemy in enemies:
        if type(enemy) == Radar:
            pass
            # to be added
        # enemy is astroid or black hole
        else:
            result_graph.add_nodes_from(enemy.get_borders())

    # creates edges:
    for point1 in result_graph.nodes:
        for point2 in result_graph.nodes:
            if point1 != point2:
                # checks if the path is legal and adds edge
                if does_line_slice(point1, point2, enemies[0]) == False:
                    result_graph.add_edge(point1, point2, weight=get_weight(point1, point2))
    return result_graph


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
    G = create_paths_graph(source, targets, enemies)

    return nx.bidirectional_shortest_path(G, source, targets[0])
    # return [source] + targets, nx.DiGraph()

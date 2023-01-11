from typing import List, Tuple

import networkx as nx
import matplotlib.pyplot as plt

from algorithmics.enemy.asteroids_zone import AsteroidsZone
from algorithmics.enemy.black_hole import BlackHole
from algorithmics.enemy.enemy import Enemy
from algorithmics.enemy.radar import Radar
from algorithmics.helper import does_line_slice
from algorithmics.utils.coordinate import Coordinate


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


def create_paths_graph(source: Coordinate, targets: List[Coordinate], enemies: List[Enemy]) -> nx.Graph():
    result_graph = nx.Graph()
    result_graph.add_node(source)
    hole_sides = 30
    for target in targets:
        result_graph.add_node(target)
    for enemy in enemies:
        if type(enemy) == Radar:
            pass
            # to be added
        # enemy is astroid or black hole
        else:
            result_graph.add_nodes_from(enemy.get_borders(hole_sides))


    # creates edges:
    for point1 in result_graph.nodes:
        for point2 in result_graph.nodes:
            if point1 != point2:
                legal = True
                for baddy in enemies:
                    # checks if the path is legal and adds edge
                    if does_line_slice(point1, point2, baddy, hole_sides):
                        legal = False
                        break
                if legal:
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

    return nx.shortest_path(G, source, targets[0], "weight"), G
    # return [source] + targets, nx.DiGraph()
#

def combine_graph(radar_graph: nx.Graph(), all_graph: nx.Graph()) -> nx.Graph():
    """combines radar graph to regular graph"""
    R = nx.compose(radar_graph, all_graph)
    return R










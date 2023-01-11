from algorithmics.enemy.enemy import Enemy
from algorithmics.utils.coordinate import Coordinate
import math


class Radar(Enemy):

    def __init__(self, center: Coordinate, radius: float):
        """Initializes a radar object at the location with the given detection radius

        :param center: location of the radar
        :param radius: detection radius of the radar
        """
        self.center = center
        self.radius = radius

    def small_steps(self, src: Coordinate, dst: Coordinate, dx: float):
        self.path_dict[(src, dst)] = []
        cur_node = src
        i = 0
        while not cur_node == dst:
            theta = cur_node.direction_to(dst) - cur_node.direction_to(self.center)
            if abs(theta) < math.pi/4:
                if theta > 0:
                    cur_node = self.go(cur_node, dx, math.pi/4)
                else:
                    cur_node = self.go(cur_node, dx, -math.pi/4)
            elif abs(math.pi-theta) < math.pi/4:
                if theta > math.pi:
                    cur_node = self.go(cur_node, dx, math.pi*5/4)
                else:
                    cur_node = self.go(cur_node, dx, math.pi * 5 / 4)
            # Can go dooch
            else:
                if cur_node.distance_to(dst) < dx:
                    cur_node = dst
                    weight = i*dx + cur_node.distance_to(dst)
                else:
                    cur_node = self.go(cur_node, dx, theta)
            # Doesn't add the source point
            self.path_dict[(src, dst)].append(cur_node)
            i += 1
        return weight

    @staticmethod
    def go(cur_node: Coordinate, dx: float, theta: float):
        x = cur_node.x + dx * math.cos(theta)
        y = cur_node.y + dx * math.cos(theta)
        return Coordinate(x, y)

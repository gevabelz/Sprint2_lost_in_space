import random

from algorithmics.enemy.enemy import Enemy
from algorithmics.utils.coordinate import Coordinate
import math
from typing import List


class Radar(Enemy):

    def __init__(self, center: Coordinate, radius: float):
        """Initializes a radar object at the location with the given detection radius

        :param center: location of the radar
        :param radius: detection radius of the radar
        """
        self.center = center
        self.radius = radius
        self.borders = []
        self.points = []

    def get_borders(self, k: int) -> List[Coordinate]:
        borders = []
        theta = math.pi / k
        c = self.radius / math.cos(theta)

        for i in range(1, 2 * k, 2):
            deg = theta * i
            x_value = self.center.x + c * math.cos(deg)
            y_value = self.center.y + c * math.sin(deg)
            borders.append(Coordinate(x_value, y_value))

        self.borders = borders
        return borders

    def calc_num_of_points(self, points_per_unit_area: float) -> int:
        return math.ceil(math.pi * (self.radius ** 2) * points_per_unit_area)

    def spray_points(self, points_per_unit_area: float) -> List[Coordinate]:
        points = []

        num_of_points = self.calc_num_of_points(points_per_unit_area)

        for i in range(num_of_points):
            r = random.random() * self.radius
            theta = random.random() * 2 * math.pi
            x = r * math.cos(theta) + self.center.x
            y = r * math.sin(theta) + self.center.y
            points.append((Coordinate(x, y)))

        self.points = points
        return points

    def is_good_angle(self, point1: Coordinate, point2: Coordinate) -> bool:
        angle_p1_to_center = point1.direction_to(self.center)
        angle_p2_to_center = point2.direction_to(self.center)
        angle_p1_to_p2 = point1.direction_to(point2)

        abs_relative_angle_1 = abs(angle_p1_to_p2 - angle_p1_to_center)
        abs_relative_angle_2 = abs(angle_p1_to_p2 - angle_p2_to_center)

        if (abs_relative_angle_1 >= math.pi / 4) and \
                (abs_relative_angle_1 <= 3 * math.pi / 4) and \
                (abs_relative_angle_2 >= math.pi / 4) and \
                (abs_relative_angle_2 <= 3 * math.pi / 4):
            return True

        return False

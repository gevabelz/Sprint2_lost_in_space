from algorithmics.enemy.enemy import Enemy
from algorithmics.utils.coordinate import Coordinate
from shapely.geometry import Point, Polygon
import math
from typing import List


class BlackHole(Enemy):

    def __init__(self, center: Coordinate, radius: float):
        """Initializes a new black hole object anchored at the given point

        :param center: the location of the black hole
        :param radius: radius of the post
        """
        self.center = center
        self.radius = radius

    def get_borders(self, k: int) -> List[Coordinate]:

        borders = []
        theta = math.pi/k
        c = (self.radius/math.cos(theta)) + 0.05

        for i in range(1, 2*k, 2):
            deg = theta*i
            x_value = self.center.x + c*math.cos(deg)
            y_value = self.center.y + c*math.sin(deg)
            borders.append(Coordinate(x_value, y_value))
        return borders


if __name__ == '__main__':
    a = Point(1, 1).buffer(5)
    b = Polygon
    print(a.intersection(b))

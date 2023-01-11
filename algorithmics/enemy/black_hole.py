from Sprint2_lost_in_space.algorithmics.enemy.enemy import Enemy
from Sprint2_lost_in_space.algorithmics.utils.coordinate import Coordinate
import math
from typing import List
from shapely.geometry import Point
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
        c = self.radius/math.cos(theta)

        for i in range(1, 2*k, 2):
            deg = theta*i
            x_value = self.center.x + c*math.cos(deg)
            y_value = self.center.y + c*math.sin(deg)
            borders.append(Coordinate(x_value, y_value))
        return borders

    def point_in_black_hole(self, cord: Coordinate) -> bool:
        circle = Point(self.center.x, self.center.y).buffer(self.radius)
        point = Point(cord.x, cord.y)
        return circle.contains(point)


if __name__ == '__main__':
    bh = BlackHole(Coordinate(10,6), 5)
    c = Coordinate(14.999, 6)
    print(bh.point_in_black_hole(c))


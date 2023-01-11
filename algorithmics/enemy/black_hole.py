from algorithmics.enemy.enemy import Enemy
from algorithmics.utils.coordinate import Coordinate
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
        self.borders = []

    def get_borders(self, k: int) -> List[Coordinate]:

        borders = []
        theta = math.pi/k
        c = self.radius/math.cos(theta)

        for i in range(1, 2*k, 2):
            deg = theta*i
            x_value = self.center.x + c*math.cos(deg)
            y_value = self.center.y + c*math.sin(deg)
            borders.append(Coordinate(x_value, y_value))

        self.borders = borders
        return borders

if __name__ == '__main__':
    bh = BlackHole(Coordinate(10,6), 5)
    print(bh.get_borders(7))

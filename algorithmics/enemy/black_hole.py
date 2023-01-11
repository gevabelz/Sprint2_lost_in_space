from algorithmics.enemy.enemy import Enemy
from algorithmics.utils.coordinate import Coordinate
import math


class BlackHole(Enemy):

    def __init__(self, center: Coordinate, radius: float):
        """Initializes a new black hole object anchored at the given point

        :param center: the location of the black hole
        :param radius: radius of the post
        """
        self.center = center
        self.radius = radius

    def get_borders(self, k: int):
        # if k == 4:
        #     return (Coordinate(self.center.x - self.radius, self.center.y - self.radius),
        #             Coordinate(self.center.x + self.radius, self.center.y - self.radius),
        #             Coordinate(self.center.x - self.radius, self.center.y + self.radius),
        #             Coordinate(self.center.x + self.radius, self.center.y + self.radius))

        # else:
        borders = []
        theta = math.pi/k
        c = self.radius/math.cos(theta)

        for i in range(1, 2*k, 2):
            deg = theta*i
            x_value = round(self.center.x + c*math.cos(deg), 2)
            y_value = round(self.center.y + c*math.sin(deg), 2)
            borders.append(Coordinate(x_value, y_value))
        return borders

if __name__ == '__main__':
    bh = BlackHole(Coordinate(10,6), 5)
    print(bh.get_borders(7))

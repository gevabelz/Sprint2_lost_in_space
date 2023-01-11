from typing import List

from algorithmics.enemy.enemy import Enemy
from algorithmics.utils.coordinate import Coordinate


class AsteroidsZone(Enemy):

    def __init__(self, boundary: List[Coordinate]):
        """Initializes a new asteroids zone area

        :param boundary: list of coordinates representing the boundary of the asteroids zone
        """
        self.boundary = boundary
        self.borders = self.boundary

    def get_borders(self, k=0) -> List[Coordinate]:
        return self.boundary

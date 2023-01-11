import shapely
from shapely import geometry
from shapely.geometry import Polygon, Point, LinearRing, LineString
from algorithmics.enemy.black_hole import BlackHole
from algorithmics.enemy.asteroids_zone import AsteroidsZone
from algorithmics.utils.coordinate import Coordinate


def does_line_slice(coord1: Coordinate, coord2: Coordinate, enemy, num_of_sides: int) -> bool:
    """checks if a line connecting between coord1 and coord2 slices through the shape
    returns True if it slices and False otherwise"""

    shape_coords = enemy.get_borders(num_of_sides)
    shape_coords_list = []
    for coord in shape_coords:
        shape_coords_list.append([coord.x, coord.y])

    shape = Polygon(shape_coords_list)
    ring = shape.exterior

    point1 = coord1.x, coord1.y
    point2 = coord2.x, coord2.y
    path = LineString([point1, point2])  # the line connecting the coords

    intersection = shape.intersection(path)

    if intersection.is_empty:
        return False
    if ring.contains(intersection):
        return False
    return True

import shapely
from shapely import geometry
from shapely.geometry import Polygon, Point, LinearRing, LineString
from algorithmics.enemy.black_hole import BlackHole
EMPTY = "EMPTY"


polygon = Polygon([[0, 0], [1, 0], [1, 1], [0, 1]])

ring = LinearRing([(0, 0), (1, 0), (1, 1), (0, 1)])
line = LineString([(1,1), (2,3)])
a = polygon.intersection(line)



def does_line_slice(coord1, coord2, enemy, num_of_sides):
    # change shape into enemy
    """checks if a line connecting between coord1 and coord2 slices through the shape
    returns True if it slices and False otherwise"""
    shape_coords = enemy.get_borders(num_of_sides)
    shape_coords_list = []
    for coord in shape_coords:
        shape_coords_list.append([coord.x, coord.y])
    shape = Polygon(shape_coords_list)
    ring = shape.exterior
    path = LineString([coord1, coord2])
    intersection = shape.intersection(path)
    if intersection.is_empty:
        return False
    if ring.contains(intersection):
        return False
    return True
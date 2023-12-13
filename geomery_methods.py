import math


def rotate(vec, angle):
    angle = angle * math.pi / 180
    vec = [vec[0] * math.cos(angle) - vec[1] * math.sin(angle), vec[0] * math.sin(angle) + vec[1] * math.cos(angle)]
    return vec


def get_angle(vec):
    if vec[0] ** 2 + vec[1] ** 2 == 0:
        return 0
    return math.degrees(math.atan2(vec[1], vec[0]))


def line_intersection_with_line(car_coords, direction, point1, point2, only_forward=True):

    frac_a1_b1 = - direction[1] / direction[0]
    frac_a2_b2 = - (point1[1] - point2[1]) / (point1[0] - point2[0])
    if abs(frac_a2_b2) == abs(frac_a1_b1):
        return False
    b1 = - 1 / (car_coords[1] + frac_a1_b1 * car_coords[0])
    b2 = - 1 / (point1[1] + frac_a2_b2 * point1[0])
    x = (1 / b2 - 1 / b1) / (frac_a1_b1 - frac_a2_b2)
    y = - abs(x) * frac_a1_b1 - 1 / b1
    if point1[0] <= x <= point2[0] or point1[0] >= x >= point2[0]:
        if only_forward:
            if (x - car_coords[0] > 0 and direction[0] > 0) or (x - car_coords[0] < 0 and direction[0] < 0):
                return x, y
        else:
            return x, y
    return False


def line_intersection_with_poligon(car_coords, direction, polygon):
    min_delta_x = 100000
    intersection = False
    for i in range(len(polygon)):
        intersection_now = line_intersection_with_line(car_coords, direction, polygon[i - 1], polygon[i])
        if intersection_now:
            if abs(intersection_now[0] - car_coords[0]) <= min_delta_x:
                intersection = intersection_now
                min_delta_x = abs(intersection_now[0] - car_coords[0])
    return intersection


def first_intersection(car_coords, direction, polygon1, polygon2):
    point1 = line_intersection_with_poligon(car_coords, direction, polygon1)
    point2 = line_intersection_with_poligon(car_coords, direction, polygon2)
    if not (point1 or point2):
        return False
    if not point1:
        return point2
    if not point2:
        return point1
    if abs(point1[0] - car_coords[0]) <= abs(point2[0] - car_coords[0]):
        return point1
    else:
        return point2




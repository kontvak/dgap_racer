import math


def rotate(vec, angle):
    """
    Поворачивает вектор на угол
    :param vec: вектор в виде массива проекций
    :param angle: угол в градусах
    :return: массив проекций получаемого вектора
    """
    angle = angle * math.pi / 180
    vec = [vec[0] * math.cos(angle) - vec[1] * math.sin(angle), vec[0] * math.sin(angle) + vec[1] * math.cos(angle)]
    return vec


def get_angle(vec):
    if vec[0] ** 2 + vec[1] ** 2 == 0:
        return 0
    return math.degrees(math.atan2(vec[1], vec[0]))


def distanse(point1, point2):
    """
    Расстояние между двумя точками
    :param point1: координаты точки 1
    :param point2: координаты точки 2
    :return:
    """
    if not (point1 and point2):
        return 10000
    return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5


def normalize(vec):
    """
    Нормирует вектор на 1
    :param vec: входной вектор
    :return: выходной вектор
    """
    modul = vec[0] ** 2 + vec[1] ** 2
    if modul == 0:
        return [0, 0]
    return [vec[0] / modul ** 0.5, vec[1] / modul ** 0.5]


def scalar(vec1, vec2):
    """
    Скалярное произведение векторов
    :param vec1: вектор 1
    :param vec2: вектор 2
    :return: скалярное произведение
    """
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]


def line_intersection_with_line(car_coords, direction, point1, point2, only_forward=True):
    """
    Пересечение луча из точки под направлением и отрезка заданного через точки
    :param car_coords: начало луча
    :param direction: направление луча
    :param point1: первая точка отрезка
    :param point2: вторая точка отрезка
    :param only_forward: true - луч(по умолчанию), false - прямая
    :return: координаты точки пересечения или false в случае непересечения
    """

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
    """
    Пересечение луча из точки и многоугольника
    :param car_coords: начало луча
    :param direction: направление луча
    :param polygon: точки многоугольника
    :return: координаты пересечения или false если нет пересечения
    """
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
    """
    Выбор БЛИЖАЙШЕЙ точки пересечения из точек пересечения с двумя многоугольниками
    :param car_coords: начало луча
    :param direction: направление луча
    :param polygon1: точки многоугольника 1
    :param polygon2: точки многоугольника 2
    :return: координаты первого пересечения или false если нет пересечения
    """
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


def normal_point_to_line(point1, point2, point3):
    """
    Находит точку начала нормали от отрезка в точку
    :param point1: первая точка отрезка
    :param point2: вторая точка отрезка
    :param point3: точка, из которой проводится нормаль
    :return: искомая точка или false если ее нет
    """
    napr = (point2[0] - point1[0], point2[1] - point1[1])
    napr = normalize(napr)
    x = point1[0] + napr[0] * (scalar(napr, point3) - scalar(napr, point1))
    y = point1[1] + napr[1] * (scalar(napr, point3) - scalar(napr, point1))
    if point1[0] <= x <= point2[0] or point1[0] >= x >= point2[0]:
        return x, y
    return False


def normal_point_to_polygon(point, polygon):
    """
    находит точку начала нормали от многоугольника к точке
    :param point: точка
    :param polygon: многоугольник
    :return: искомая точка, номер отрезка на котороом находится эта точка
    """
    min_distanse = 100000
    ans_point = False
    number_of_line = 0
    for i in range(len(polygon)):
        now_point = normal_point_to_line(polygon[i - 1], polygon[i], point)
        if now_point:
            if distanse(now_point, point) <= min_distanse:
                min_distanse = distanse(now_point, point)
                ans_point = now_point
                number_of_line = i
    return ans_point, number_of_line


def score_distanse(car_point, polygon):
    """
    расстояние, которое прошла проекция точки на многоугольник
    :param car_point: точка
    :param polygon: многоугольник
    :return: расстояние
    """
    (score_point, number_of_line) = normal_point_to_polygon(car_point, polygon)
    score = 0
    last_point = (number_of_line - 1) % len(polygon)
    if score_point:
        for i in range(0, last_point):
            score += distanse(polygon[i], polygon[i + 1])
        score += distanse(score_point, polygon[last_point])
    return score, number_of_line

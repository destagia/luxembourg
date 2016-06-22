from luxembourg import Line, Point

points = [set([x, y]) for x in range(0, 15) for y in range(0, 15)]

points = [Point(x, y) for x in range(0, 5) for y in range(0, 5) if x >= y]
print(points)
def distinct(acc, x):
    if not x in acc:
        acc.append(x)
    return acc

def validate(acc, points):
    p1, p2 = points
    x_diff = p1.get_x() - p2.get_x()
    y_diff = p1.get_y() - p2.get_y()
    if x_diff == 0 or y_diff == 0 or x_diff == y_diff:
        if p2.get_x() < p1.get_x() or p2.get_y() < p1.get_y():
            points = (p2, p1)
        acc.append(Line(points[0], points[1]))
    return acc
lines = reduce(distinct, [set([x, y]) for x in range(0, 15) for y in range(0, 15)], [])
lines = map(lambda x: list(x) + list(x) if len(x) == 1 else sorted(list(x)), lines)
lines = map(lambda x: (points[x[0]], points[x[1]]), lines)
lines = reduce(validate, lines, [])

import heapq
import time


BOUND_RADIUS = 10.0
EPSILON = 1e-13


def leftNormal(vector):
    x, y = vector
    return -y, x


def add(first, second):
    return first[0] + second[0], first[1] + second[1]


def childSquares(origin, base):
    normal = leftNormal(base)
    topLeft = add(origin, normal)
    leftBase = (
        (16 * base[0] + 12 * normal[0]) / 25,
        (16 * base[1] + 12 * normal[1]) / 25,
    )
    apex = add(topLeft, leftBase)
    rightBase = (
        (9 * base[0] - 12 * normal[0]) / 25,
        (9 * base[1] - 12 * normal[1]) / 25,
    )

    return (topLeft, leftBase), (apex, rightBase)


def dot(first, second):
    return first[0] * second[0] + first[1] * second[1]


def sideLength(base):
    return (base[0] * base[0] + base[1] * base[1]) ** 0.5


def squareSupport(direction, origin, base):
    normal = leftNormal(base)
    vertices = (
        origin,
        add(origin, base),
        add(origin, normal),
        add(add(origin, base), normal),
    )

    return max(dot(direction, vertex) for vertex in vertices)


def treeSupport(direction):
    directionLength = sideLength(direction)
    root = ((0.0, 0.0), (1.0, 0.0))
    best = squareSupport(direction, *root)
    queue = []
    counter = 0

    def upperBound(origin, base):
        return (
            squareSupport(direction, origin, base)
            + directionLength * sideLength(base) * BOUND_RADIUS
        )

    heapq.heappush(queue, (-upperBound(*root), counter, root))
    counter += 1

    while queue:
        negativeBound, _, square = heapq.heappop(queue)

        if -negativeBound <= best + EPSILON:
            break

        origin, base = square
        best = max(best, squareSupport(direction, origin, base))

        if directionLength * sideLength(base) * BOUND_RADIUS <= EPSILON:
            continue

        for child in childSquares(origin, base):
            bound = upperBound(*child)

            if bound > best + EPSILON:
                heapq.heappush(queue, (-bound, counter, child))
                counter += 1

    return best


def boundingArea():
    minimumX = -treeSupport((-1.0, 0.0))
    maximumX = treeSupport((1.0, 0.0))
    minimumY = -treeSupport((0.0, -1.0))
    maximumY = treeSupport((0.0, 1.0))

    return (maximumX - minimumX) * (maximumY - minimumY)


def answer():
    return format(boundingArea(), ".10f")


def runTests():
    assert answer() == "28.2453753155"


if __name__ == "__main__":
    runTests()
    start = time.time()
    result = answer()
    elapsed = time.time() - start

    print("Found " + str(result) + " in " + str(elapsed) + " seconds.")

import itertools
import math
import time


MODULUS = 100000000

A_EDGES = [
    (1, 2),
    (3, 4),
    (1, 4),
    (1, 5),
    (2, 3),
    (2, 7),
    (3, 7),
    (4, 5),
    (5, 6),
    (6, 7),
]
B_EDGES = [
    (1, 2),
    (3, 4),
    (1, 5),
    (2, 3),
    (2, 7),
    (3, 7),
    (4, 5),
    (5, 6),
    (6, 7),
]


def fixedLeftColorings(edges, colors):
    assignments = {1: 0, 2: 1}
    free_vertices = [3, 4, 5, 6, 7]
    count = 0

    for color_tuple in itertools.product(range(colors), repeat=len(free_vertices)):
        for vertex, color in zip(free_vertices, color_tuple):
            assignments[vertex] = color

        if all(assignments[start] != assignments[end] for start, end in edges):
            count += 1

    return count


def forwardDifferences(values):
    differences = [values[0]]
    row = values

    while len(row) > 1:
        row = [row[index + 1] - row[index] for index in range(len(row) - 1)]
        differences.append(row[0])

    return differences


def unitPolynomialValue(edges, colors):
    start = 2
    sample_values = [fixedLeftColorings(edges, value) for value in range(start, start + 6)]
    differences = forwardDifferences(sample_values)
    offset = colors - start

    return sum(math.comb(offset, degree) * difference for degree, difference in enumerate(differences))


def configurationCount(a_units, b_units, colors, modulus=None):
    a_value = unitPolynomialValue(A_EDGES, colors)
    b_value = unitPolynomialValue(B_EDGES, colors)

    if modulus is None:
        return (
            math.comb(a_units + b_units, a_units)
            * colors
            * (colors - 1)
            * (a_value ** a_units)
            * (b_value ** b_units)
        )

    return (
        math.comb(a_units + b_units, a_units)
        * colors
        * (colors - 1)
        * pow(a_value, a_units, modulus)
        * pow(b_value, b_units, modulus)
    ) % modulus


def runTests():
    assert configurationCount(1, 0, 3) == 24
    assert configurationCount(0, 2, 4) == 92928
    assert configurationCount(2, 2, 3) == 20736


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = configurationCount(25, 75, 1984, MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")

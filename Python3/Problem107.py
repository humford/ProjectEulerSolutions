import time
from pathlib import Path


def readNetwork():
    path = Path(__file__).resolve().parents[1] / "Files" / "p107_network.txt"
    return [line.split(",") for line in path.read_text().strip().splitlines()]


def edgesFromMatrix(matrix):
    edges = []
    total = 0

    for row in range(len(matrix)):
        for col in range(row + 1, len(matrix)):
            if matrix[row][col] == "-":
                continue

            weight = int(matrix[row][col])
            total += weight
            edges.append((weight, row, col))

    return total, edges


def minimumSpanningWeight(node_count, edges):
    parent = list(range(node_count))

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    weight = 0
    edge_count = 0

    for edge_weight, first, second in sorted(edges):
        root_first = find(first)
        root_second = find(second)
        if root_first == root_second:
            continue

        parent[root_second] = root_first
        weight += edge_weight
        edge_count += 1
        if edge_count == node_count - 1:
            return weight

    raise ValueError("Network is not connected")


def maximumSaving(matrix):
    total, edges = edgesFromMatrix(matrix)
    return total - minimumSpanningWeight(len(matrix), edges)


def runTests():
    matrix = [
        ["-", "1", "5"],
        ["1", "-", "2"],
        ["5", "2", "-"],
    ]
    assert maximumSaving(matrix) == 5


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = maximumSaving(readNetwork())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")

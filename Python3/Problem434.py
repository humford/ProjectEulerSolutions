import time


MODULUS = 1_000_000_033


def binomialTable(limit):
    table = [[0] * (limit + 1) for _ in range(limit + 1)]

    for row in range(limit + 1):
        table[row][0] = 1
        table[row][row] = 1

        for column in range(1, row):
            table[row][column] = (
                table[row - 1][column - 1] + table[row - 1][column]
            ) % MODULUS

    return table


def powerTable(limit):
    return [
        [pow(2, rows * columns, MODULUS) for columns in range(limit + 1)]
        for rows in range(limit + 1)
    ]


def connectedBipartiteGraphCounts(limit):
    choose = binomialTable(limit)
    graphCounts = powerTable(limit)
    connected = [[0] * (limit + 1) for _ in range(limit + 1)]

    for rows in range(1, limit + 1):
        for columns in range(1, limit + 1):
            disconnected = 0

            for componentRows in range(1, rows + 1):
                chooseRows = choose[rows - 1][componentRows - 1]

                if componentRows == 1:
                    disconnected += chooseRows * graphCounts[rows - componentRows][columns]

                maxComponentColumns = columns
                if componentRows == rows:
                    maxComponentColumns -= 1

                for componentColumns in range(1, maxComponentColumns + 1):
                    disconnected += (
                        chooseRows
                        * choose[columns][componentColumns]
                        % MODULUS
                        * connected[componentRows][componentColumns]
                        % MODULUS
                        * graphCounts[rows - componentRows][columns - componentColumns]
                    )

            connected[rows][columns] = (
                graphCounts[rows][columns] - disconnected
            ) % MODULUS

    return connected


def rigidGridCount(width, height, connected=None):
    if connected is None:
        connected = connectedBipartiteGraphCounts(max(width, height))
    return connected[width][height]


def rigidGridSum(limit):
    connected = connectedBipartiteGraphCounts(limit)
    return sum(
        connected[width][height]
        for width in range(1, limit + 1)
        for height in range(1, limit + 1)
    ) % MODULUS


def runTests():
    connected = connectedBipartiteGraphCounts(5)
    assert rigidGridCount(2, 3, connected) == 19
    assert rigidGridCount(3, 2, connected) == 19
    assert rigidGridCount(5, 5, connected) == 23679901
    assert sum(
        connected[width][height]
        for width in range(1, 6)
        for height in range(1, 6)
    ) % MODULUS == 25021721


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = rigidGridSum(100)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")

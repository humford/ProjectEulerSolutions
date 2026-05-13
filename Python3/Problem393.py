import time
from functools import lru_cache


LIMIT = 10
UP, RIGHT, DOWN, LEFT = range(4)


def migratingAnts(size=LIMIT):
    @lru_cache(maxsize=None)
    def transitions(row, downMask, upMask):
        results = []

        def finishCell(column, move, baseOccupancy, incomingRight, nextDown, nextUp):
            occupancy = baseOccupancy + incomingRight

            if occupancy > 0 or occupancy < -1:
                return None

            if move == DOWN:
                if row + 1 == size or occupancy == -1:
                    return None

                nextDown |= 1 << column

            if occupancy == -1:
                nextUp |= 1 << column

            return nextDown, nextUp

        def searchColumn(column, previousMove, previousBase, nextDown, nextUp):
            if column == size:
                finished = finishCell(
                    size - 1,
                    previousMove,
                    previousBase,
                    0,
                    nextDown,
                    nextUp,
                )

                if finished is not None:
                    results.append(finished)

                return

            bit = 1 << column

            for move in (UP, RIGHT, DOWN, LEFT):
                if column == size - 1 and move == RIGHT:
                    continue
                if previousMove == RIGHT and move == LEFT:
                    continue

                if move == UP:
                    if (downMask & bit) or not (upMask & bit):
                        continue
                elif upMask & bit:
                    continue

                finished = finishCell(
                    column - 1,
                    previousMove,
                    previousBase,
                    1 if move == LEFT else 0,
                    nextDown,
                    nextUp,
                )

                if finished is None:
                    continue

                currentDown, currentUp = finished
                base = (1 if downMask & bit else 0) + (
                    1 if previousMove == RIGHT else 0
                ) - 1
                searchColumn(column + 1, move, base, currentDown, currentUp)

        firstBit = 1

        for move in (UP, RIGHT, DOWN):
            if size == 1 and move == RIGHT:
                continue

            if move == UP:
                if (downMask & firstBit) or not (upMask & firstBit):
                    continue
            elif upMask & firstBit:
                continue

            base = (1 if downMask & firstBit else 0) - 1
            searchColumn(1, move, base, 0, 0)

        return tuple(results)

    @lru_cache(maxsize=None)
    def count(row, downMask, upMask):
        if row == size:
            return 1 if downMask == 0 and upMask == 0 else 0

        return sum(
            count(row + 1, nextDown, nextUp)
            for nextDown, nextUp in transitions(row, downMask, upMask)
        )

    return count(0, 0, 0)


def runTests():
    assert migratingAnts(2) == 2
    assert migratingAnts(4) == 88


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = migratingAnts()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")

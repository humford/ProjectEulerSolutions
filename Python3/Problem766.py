import time
from collections import deque


def encodePositions(positions):
    encoded = 0
    for index, position in enumerate(positions):
        encoded |= position << (5 * index)
    return encoded


def decodePositions(encoded, count):
    return [(encoded >> (5 * index)) & 31 for index in range(count)]


class Puzzle:
    def __init__(self, width, height, pieceTypes, initialPositions):
        self.width = width
        self.height = height
        self.deltas = (-width, width, -1, 1)
        self.types = []

        pieceOffset = 0
        for pieceType in pieceTypes:
            offsets = pieceType["offsets"]
            count = pieceType["count"]
            masks = [0] * (width * height)
            limits = [None] * (width * height)

            for position in range(width * height):
                x = position % width
                y = position // width
                mask = 0
                valid = True
                for dx, dy in offsets:
                    xx = x + dx
                    yy = y + dy
                    if xx < 0 or xx >= width or yy < 0 or yy >= height:
                        valid = False
                        break
                    mask |= 1 << (yy * width + xx)
                if not valid:
                    continue

                masks[position] = mask
                limits[position] = (
                    min(y + dy for _, dy in offsets),
                    min(height - 1 - (y + dy) for _, dy in offsets),
                    min(x + dx for dx, _ in offsets),
                    min(width - 1 - (x + dx) for dx, _ in offsets),
                )

            bitShift = 5 * pieceOffset
            segmentBits = 5 * count
            segmentMask = ((1 << segmentBits) - 1) << bitShift
            self.types.append(
                {
                    "count": count,
                    "masks": masks,
                    "limits": limits,
                    "bitShift": bitShift,
                    "segmentMask": segmentMask,
                }
            )
            pieceOffset += count

        state = 0
        for typeIndex, positions in enumerate(initialPositions):
            typeData = self.types[typeIndex]
            sortedPositions = sorted(positions)
            if len(sortedPositions) != typeData["count"]:
                raise ValueError("wrong piece count")
            for position in sortedPositions:
                if typeData["limits"][position] is None:
                    raise ValueError("invalid initial anchor")
            state |= encodePositions(sortedPositions) << typeData["bitShift"]

        self.initialState = state

    def countReachable(self):
        seen = {self.initialState}
        queue = deque([self.initialState])

        while queue:
            state = queue.popleft()
            occupancy = 0
            decoded = []

            for typeData in self.types:
                segment = (state & typeData["segmentMask"]) >> typeData["bitShift"]
                positions = decodePositions(segment, typeData["count"])
                decoded.append(positions)
                for position in positions:
                    occupancy |= typeData["masks"][position]

            for typeIndex, typeData in enumerate(self.types):
                positions = decoded[typeIndex]
                count = typeData["count"]
                masks = typeData["masks"]
                limits = typeData["limits"]
                segmentMask = typeData["segmentMask"]
                bitShift = typeData["bitShift"]

                for pieceIndex, position in enumerate(positions):
                    occupancyWithoutPiece = occupancy ^ masks[position]

                    for directionIndex, delta in enumerate(self.deltas):
                        maxSteps = limits[position][directionIndex]
                        for steps in range(1, maxSteps + 1):
                            newPosition = position + delta * steps
                            if masks[newPosition] & occupancyWithoutPiece:
                                break

                            newPositions = positions[:]
                            newPositions[pieceIndex] = newPosition
                            index = pieceIndex
                            while index > 0 and newPositions[index] < newPositions[index - 1]:
                                newPositions[index], newPositions[index - 1] = (
                                    newPositions[index - 1],
                                    newPositions[index],
                                )
                                index -= 1
                            while index < count - 1 and newPositions[index] > newPositions[index + 1]:
                                newPositions[index], newPositions[index + 1] = (
                                    newPositions[index + 1],
                                    newPositions[index],
                                )
                                index += 1

                            newSegment = encodePositions(newPositions)
                            newState = (state & ~segmentMask) | (newSegment << bitShift)
                            if newState not in seen:
                                seen.add(newState)
                                queue.append(newState)

        return len(seen)


def examplePuzzle():
    return Puzzle(
        4,
        3,
        [
            {"offsets": [(0, 0), (1, 0), (0, 1)], "count": 1},
            {"offsets": [(0, 0)], "count": 7},
        ],
        [
            [0],
            [2, 5, 6, 8, 9, 10, 11],
        ],
    )


def mainPuzzle():
    return Puzzle(
        6,
        5,
        [
            {"offsets": [(0, 0), (0, 1), (1, 0)], "count": 2},
            {"offsets": [(0, 1), (1, 0), (1, 1)], "count": 2},
            {"offsets": [(0, 0), (0, 1)], "count": 2},
            {"offsets": [(0, 0)], "count": 6},
            {"offsets": [(0, 0), (1, 0), (0, 1), (1, 1)], "count": 1},
            {"offsets": [(0, 0), (1, 0)], "count": 1},
        ],
        [
            [1, 4],
            [2, 22],
            [11, 16],
            [12, 13, 18, 19, 24, 25],
            [14],
            [26],
        ],
    )


def runTests():
    assert examplePuzzle().countReachable() == 208


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = mainPuzzle().countReachable()
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")

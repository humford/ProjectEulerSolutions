import time
from collections import defaultdict


WIDTH = 6
HEIGHT = 10
MODULUS = 10**10


CONNECTIONS = (
    1111,
    1114,
    1133,
    1134,
    1131,
    1211,
    1214,
    1221,
    1222,
    1224,
    1231,
    1232,
    1233,
    1234,
)


def canonicalState(state):
    if state == 0:
        return 0

    mapping = [0] * 20
    next_label = 0
    result = 0
    index = 0

    while state >> (4 * index) != 0:
        label = (state >> (4 * index)) & 15

        if mapping[label] == 0:
            next_label += 1
            mapping[label] = next_label

        result |= (mapping[label] - 1) << (4 * index)
        index += 1

    return result


def mergeLabel(state, source, target, height):
    for index in range(height + 4):
        if ((state >> (4 * index)) & 15) == source:
            state ^= (source ^ target) << (4 * index)

    return state


def labelCount(state, label, height):
    total = 0

    for _ in range(height + 4):
        if state & 15 == label:
            total += 1
        state >>= 4

    return total


def transitions(state, x, y, width, height, final):
    def label(index):
        return (state >> (4 * index)) & 15

    new_label = 0 if x == width or y == height else 15
    colors = [label(y), label(y + 1), label(y + 2), new_label]
    result = []

    for connection in CONNECTIONS:
        indices = (
            connection // 1000 - 1,
            (connection // 100) % 10 - 1,
            (connection // 10) % 10 - 1,
            connection % 10 - 1,
        )

        valid = True
        for i in range(4):
            if colors[i] != 0:
                continue

            for j in range(4):
                if (colors[j] == 0) != (indices[i] == indices[j]):
                    valid = False
                    break

            if not valid:
                break

        if not valid:
            continue

        next_state = (state << 4) | new_label

        for i in range(4):
            if i == indices[i]:
                continue

            source = (
                new_label
                if i == 3
                else (next_state >> (4 * (y + i + 1))) & 15
            )
            target = (next_state >> (4 * (y + indices[i] + 1))) & 15

            if source == 0:
                continue
            if target == 0 or source == target:
                next_state = -1
                break

            next_state = mergeLabel(next_state, source, target, height)

        if next_state == -1:
            continue

        current = next_state & 15
        next_state >>= 4
        old = (next_state >> (4 * (y + 1))) & 15

        if labelCount(next_state, old, height) > 1 or old == current or final:
            next_state ^= (current ^ old) << (4 * (y + 1))

            if y == height:
                next_state <<= 4

            result.append(canonicalState(next_state))

    return result


def eulerianCycleCount(width, height, modulus=MODULUS):
    if width > height:
        width, height = height, width

    counts = {0: 1}
    transition_cache = {}

    for x in range(height + 1):
        for y in range(width + 1):
            final = x == height and y == width
            next_counts = defaultdict(int)

            for state, count in counts.items():
                new_label = 0 if x == height or y == width else 15
                key = (state, y, new_label)

                if final:
                    next_states = transitions(state, x, y, height, width, True)
                else:
                    next_states = transition_cache.get(key)
                    if next_states is None:
                        next_states = transitions(state, x, y, height, width, False)
                        transition_cache[key] = next_states

                for next_state in next_states:
                    next_counts[next_state] = (
                        next_counts[next_state] + count
                    ) % modulus

            counts = next_counts

    return counts.get(0, 0)


def runTests():
    assert eulerianCycleCount(1, 2) == 2
    assert eulerianCycleCount(2, 2) == 37
    assert eulerianCycleCount(3, 3) == 104290


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = eulerianCycleCount(WIDTH, HEIGHT)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")

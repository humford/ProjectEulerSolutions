import time


LENGTH = 15
DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def contactMaps(length):
    pair_index = {}
    index = 0

    for i in range(length):
        for j in range(i + 1, length):
            pair_index[(i, j)] = index
            index += 1

    if length == 1:
        return {0}, pair_index

    maps = set()
    path = [(0, 0), (1, 0)]
    used = {(0, 0), (1, 0)}

    def search():
        if len(path) == length:
            contact_map = 0

            for i in range(length):
                xi, yi = path[i]
                for j in range(i + 1, length):
                    xj, yj = path[j]
                    if abs(xi - xj) + abs(yi - yj) == 1:
                        contact_map |= 1 << pair_index[(i, j)]

            maps.add(contact_map)
            return

        x, y = path[-1]
        for dx, dy in DIRECTIONS:
            next_cell = (x + dx, y + dy)
            if next_cell in used:
                continue

            used.add(next_cell)
            path.append(next_cell)
            search()
            path.pop()
            used.remove(next_cell)

    search()
    return maps, pair_index


def proteinPairMasks(length, pair_index):
    masks = []

    for protein in range(1 << length):
        pair_mask = 0

        for (i, j), index in pair_index.items():
            if protein & (1 << i) and protein & (1 << j):
                pair_mask |= 1 << index

        masks.append(pair_mask)

    return masks


def optimalContactTotal(length):
    maps, pair_index = contactMaps(length)
    pair_masks = proteinPairMasks(length, pair_index)
    best = [0] * (1 << length)

    for contact_map in maps:
        for protein, pair_mask in enumerate(pair_masks):
            score = (contact_map & pair_mask).bit_count()
            if score > best[protein]:
                best[protein] = score

    return sum(best)


def optimalContactAverage(length):
    return optimalContactTotal(length) / (1 << length)


def runTests():
    assert optimalContactTotal(8) == 850


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = optimalContactAverage(LENGTH)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")

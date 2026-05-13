import multiprocessing
import os
import time


ORDER = 18
PARALLEL_MIN_ORDER = 18
PARALLEL_SPLIT_SIZE = 8
POOL_CHUNK_SIZE = 8


_WORKER_ORDER = None
_WORKER_X_COORDS = None
_WORKER_NEIGHBORS = None
_WORKER_QUEUE_CAPACITY = None


def buildGrid(order, half_plane=False):
    max_coordinate = order - 1
    width = 2 * max_coordinate + 1
    shift = max_coordinate
    grid_size = width * order

    x_coords = [0] * grid_size
    neighbors = [None] * grid_size

    for y in range(order):
        row = y * width
        for x_index in range(width):
            cell = row + x_index
            x = x_index - shift
            x_coords[cell] = x

            if half_plane and x < 0:
                neighbors[cell] = ()
                continue

            cell_neighbors = []
            if half_plane:
                if x_index > shift:
                    cell_neighbors.append(cell - 1)
            elif x_index > 0:
                cell_neighbors.append(cell - 1)

            if x_index < width - 1:
                cell_neighbors.append(cell + 1)
            if y > 0:
                cell_neighbors.append(cell - width)
            if y < order - 1:
                cell_neighbors.append(cell + width)

            neighbors[cell] = tuple(cell_neighbors)

    return tuple(x_coords), tuple(neighbors), shift, grid_size


def initialState(order, neighbors, root, grid_size):
    seen = bytearray(grid_size)
    queue = [0] * (8 * order + 50)
    queue_end = 0
    seen[root] = 1

    for neighbor in neighbors[root]:
        if seen[neighbor] == 0:
            seen[neighbor] = 1
            queue[queue_end] = neighbor
            queue_end += 1

    return seen, queue, queue_end


def countTotalFromState(
    order, x_coords, neighbors, queue_begin, queue_end, size, moment, min_x, max_x, seen, queue
):
    total = 0
    x_values = x_coords
    neighbor_values = neighbors
    seen_values = seen
    queue_values = queue

    def search(queue_begin, queue_end, size, moment, min_x, max_x):
        nonlocal total

        if size == order:
            if moment == 0:
                total += 1
            return

        remaining = order - size
        if moment + remaining * (min_x - remaining) > 0:
            return
        if moment + remaining * (max_x + remaining) < 0:
            return

        for index in range(queue_begin, queue_end):
            cell = queue_values[index]
            x = x_values[cell]
            added = 0

            for neighbor in neighbor_values[cell]:
                if seen_values[neighbor] == 0:
                    seen_values[neighbor] = 1
                    queue_values[queue_end + added] = neighbor
                    added += 1

            search(
                index + 1,
                queue_end + added,
                size + 1,
                moment + x,
                x if x < min_x else min_x,
                x if x > max_x else max_x,
            )

            for undo_index in range(queue_end, queue_end + added):
                seen_values[queue_values[undo_index]] = 0

    search(queue_begin, queue_end, size, moment, min_x, max_x)
    return total


def createTotalTasks(order, x_coords, neighbors, root, grid_size, split_size):
    seen, queue, queue_end = initialState(order, neighbors, root, grid_size)
    tasks = []

    def search(queue_begin, queue_end, size, moment, min_x, max_x):
        if size == split_size:
            tasks.append(
                (
                    queue_begin,
                    queue_end,
                    size,
                    moment,
                    min_x,
                    max_x,
                    bytes(seen),
                    tuple(queue[:queue_end]),
                )
            )
            return

        remaining = order - size
        if moment + remaining * (min_x - remaining) > 0:
            return
        if moment + remaining * (max_x + remaining) < 0:
            return

        for index in range(queue_begin, queue_end):
            cell = queue[index]
            x = x_coords[cell]
            added = 0

            for neighbor in neighbors[cell]:
                if seen[neighbor] == 0:
                    seen[neighbor] = 1
                    queue[queue_end + added] = neighbor
                    added += 1

            search(
                index + 1,
                queue_end + added,
                size + 1,
                moment + x,
                x if x < min_x else min_x,
                x if x > max_x else max_x,
            )

            for undo_index in range(queue_end, queue_end + added):
                seen[queue[undo_index]] = 0

    search(0, queue_end, 1, 0, 0, 0)
    return tasks


def initializeTotalWorker(order, x_coords, neighbors):
    global _WORKER_ORDER
    global _WORKER_X_COORDS
    global _WORKER_NEIGHBORS
    global _WORKER_QUEUE_CAPACITY

    _WORKER_ORDER = order
    _WORKER_X_COORDS = x_coords
    _WORKER_NEIGHBORS = neighbors
    _WORKER_QUEUE_CAPACITY = 8 * order + 50


def countTotalWorker(task):
    queue_begin, queue_end, size, moment, min_x, max_x, seen_bytes, queue_prefix = task
    seen = bytearray(seen_bytes)
    queue = list(queue_prefix) + [0] * (_WORKER_QUEUE_CAPACITY - len(queue_prefix))

    return countTotalFromState(
        _WORKER_ORDER,
        _WORKER_X_COORDS,
        _WORKER_NEIGHBORS,
        queue_begin,
        queue_end,
        size,
        moment,
        min_x,
        max_x,
        seen,
        queue,
    )


def countTotalBalanced(order):
    x_coords, neighbors, root, grid_size = buildGrid(order)

    if order >= PARALLEL_MIN_ORDER and (os.cpu_count() or 1) > 1:
        tasks = createTotalTasks(
            order, x_coords, neighbors, root, grid_size, PARALLEL_SPLIT_SIZE
        )
        worker_count = min(os.cpu_count() or 1, len(tasks))

        try:
            context = multiprocessing.get_context("fork")
        except ValueError:
            context = None

        if context is not None:
            with context.Pool(
                processes=worker_count,
                initializer=initializeTotalWorker,
                initargs=(order, x_coords, neighbors),
            ) as pool:
                return sum(
                    pool.imap_unordered(
                        countTotalWorker, tasks, chunksize=POOL_CHUNK_SIZE
                    )
                )

    seen, queue, queue_end = initialState(order, neighbors, root, grid_size)
    return countTotalFromState(
        order, x_coords, neighbors, 0, queue_end, 1, 0, 0, 0, seen, queue
    )


def countSymmetricBalanced(order):
    x_coords, neighbors, root, grid_size = buildGrid(order, half_plane=True)
    seen, queue, queue_end = initialState(order, neighbors, root, grid_size)
    total = 0

    def search(queue_begin, queue_end, full_size):
        nonlocal total

        if full_size == order:
            total += 1
            return

        for index in range(queue_begin, queue_end):
            cell = queue[index]
            x = x_coords[cell]
            next_size = full_size + (1 if x == 0 else 2)

            if next_size > order:
                continue

            added = 0
            for neighbor in neighbors[cell]:
                if seen[neighbor] == 0:
                    seen[neighbor] = 1
                    queue[queue_end + added] = neighbor
                    added += 1

            search(index + 1, queue_end + added, next_size)

            for undo_index in range(queue_end, queue_end + added):
                seen[queue[undo_index]] = 0

    search(0, queue_end, 1)
    return total


def balancedSculptureCount(order):
    total = countTotalBalanced(order)
    symmetric = countSymmetricBalanced(order)
    return (total + symmetric) // 2


def runTests():
    assert balancedSculptureCount(6) == 18
    assert balancedSculptureCount(10) == 964
    assert balancedSculptureCount(15) == 360505


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = balancedSculptureCount(ORDER)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")

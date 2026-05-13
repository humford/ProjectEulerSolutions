import time
from array import array


MODULUS = 1_000_000_000


def reversalChecksum(size, operations, modulus=None):
    useModulus = modulus is not None

    leftChild = array("I", [0])
    rightChild = array("I", [0])
    priority = array("I", [0])
    segmentLength = array("Q", [0])
    segmentStart = array("Q", [0])
    segmentDirection = array("b", [0])
    reverseFlag = array("b", [0])
    totalLength = array("Q", [0])

    if useModulus:
        segmentSum = array("I", [0])
        segmentPositionSum = array("I", [0])
        subtreeSum = array("I", [0])
        subtreePositionSum = array("I", [0])
    else:
        segmentSum = array("q", [0])
        segmentPositionSum = array("q", [0])
        subtreeSum = array("q", [0])
        subtreePositionSum = array("q", [0])

    randomState = 2_463_534_242

    def random32():
        nonlocal randomState
        randomState ^= (randomState << 13) & 0xFFFFFFFF
        randomState ^= (randomState >> 17) & 0xFFFFFFFF
        randomState ^= (randomState << 5) & 0xFFFFFFFF
        return randomState & 0xFFFFFFFF

    if useModulus:

        def triangle(length):
            a = length
            b = length - 1
            if a % 2 == 0:
                a //= 2
            else:
                b //= 2
            return (a % modulus) * (b % modulus) % modulus

        def squarePrefix(length):
            a = length - 1
            b = length
            c = 2 * length - 1

            if a % 2 == 0:
                a //= 2
            else:
                b //= 2

            if a % 3 == 0:
                a //= 3
            elif b % 3 == 0:
                b //= 3
            else:
                c //= 3

            return (a % modulus) * (b % modulus) % modulus * (c % modulus) % modulus

        def segmentSums(length, start, direction):
            startMod = start % modulus
            lengthMod = length % modulus
            triangular = triangle(length)
            squareSum = squarePrefix(length)
            if direction == 1:
                valueSum = (startMod * lengthMod + triangular) % modulus
                positionSum = (startMod * triangular + squareSum) % modulus
            else:
                valueSum = (startMod * lengthMod - triangular) % modulus
                positionSum = (startMod * triangular - squareSum) % modulus
            return valueSum, positionSum

    else:

        def segmentSums(length, start, direction):
            triangular = length * (length - 1) // 2
            squareSum = (length - 1) * length * (2 * length - 1) // 6
            if direction == 1:
                valueSum = start * length + triangular
                positionSum = start * triangular + squareSum
            else:
                valueSum = start * length - triangular
                positionSum = start * triangular - squareSum
            return valueSum, positionSum

    def newNode(length, start, direction):
        index = len(leftChild)
        leftChild.append(0)
        rightChild.append(0)
        priority.append(random32())
        segmentLength.append(length)
        segmentStart.append(start)
        segmentDirection.append(direction)
        reverseFlag.append(0)
        totalLength.append(length)

        valueSum, positionSum = segmentSums(length, start, direction)
        segmentSum.append(valueSum)
        segmentPositionSum.append(positionSum)
        subtreeSum.append(valueSum)
        subtreePositionSum.append(positionSum)
        return index

    def applyReverse(node):
        if node == 0:
            return

        leftChild[node], rightChild[node] = rightChild[node], leftChild[node]
        reverseFlag[node] ^= 1

        length = segmentLength[node]
        direction = segmentDirection[node]
        if length > 1:
            segmentStart[node] = segmentStart[node] + direction * (length - 1)
        segmentDirection[node] = -direction

        if useModulus:
            segmentPositionSum[node] = (
                ((length - 1) % modulus) * segmentSum[node]
                - segmentPositionSum[node]
            ) % modulus
            subtreePositionSum[node] = (
                ((totalLength[node] - 1) % modulus) * subtreeSum[node]
                - subtreePositionSum[node]
            ) % modulus
        else:
            segmentPositionSum[node] = (
                (length - 1) * segmentSum[node]
                - segmentPositionSum[node]
            )
            subtreePositionSum[node] = (
                (totalLength[node] - 1) * subtreeSum[node]
                - subtreePositionSum[node]
            )

    def push(node):
        if node and reverseFlag[node]:
            if leftChild[node]:
                applyReverse(leftChild[node])
            if rightChild[node]:
                applyReverse(rightChild[node])
            reverseFlag[node] = 0

    def update(node):
        if node == 0:
            return

        left = leftChild[node]
        right = rightChild[node]
        leftLength = totalLength[left] if left else 0
        rightLength = totalLength[right] if right else 0
        totalLength[node] = leftLength + segmentLength[node] + rightLength

        leftSum = subtreeSum[left] if left else 0
        rightSum = subtreeSum[right] if right else 0
        leftPositionSum = subtreePositionSum[left] if left else 0
        rightPositionSum = subtreePositionSum[right] if right else 0

        if useModulus:
            subtreeSum[node] = (leftSum + segmentSum[node] + rightSum) % modulus
            subtreePositionSum[node] = (
                leftPositionSum
                + (leftLength % modulus) * segmentSum[node]
                + segmentPositionSum[node]
                + rightPositionSum
                + ((leftLength + segmentLength[node]) % modulus) * rightSum
            ) % modulus
        else:
            subtreeSum[node] = leftSum + segmentSum[node] + rightSum
            subtreePositionSum[node] = (
                leftPositionSum
                + leftLength * segmentSum[node]
                + segmentPositionSum[node]
                + rightPositionSum
                + (leftLength + segmentLength[node]) * rightSum
            )

    def merge(left, right):
        if left == 0:
            return right
        if right == 0:
            return left

        stack = []
        while left and right:
            if priority[left] < priority[right]:
                push(left)
                stack.append((left, 1))
                left = rightChild[left]
            else:
                push(right)
                stack.append((right, 0))
                right = leftChild[right]

        root = left or right
        while stack:
            node, usedRight = stack.pop()
            if usedRight:
                rightChild[node] = root
            else:
                leftChild[node] = root
            update(node)
            root = node

        return root

    def split(root, count):
        if root == 0:
            return 0, 0

        leftStack = []
        rightStack = []

        while root:
            push(root)
            left = leftChild[root]
            leftLength = totalLength[left] if left else 0
            ownLength = segmentLength[root]

            if count < leftLength:
                rightStack.append(root)
                root = left
            elif count > leftLength + ownLength:
                count -= leftLength + ownLength
                leftStack.append(root)
                root = rightChild[root]
            else:
                if count == leftLength:
                    leftResult = left
                    leftChild[root] = 0
                    update(root)
                    rightResult = root
                elif count == leftLength + ownLength:
                    rightResult = rightChild[root]
                    rightChild[root] = 0
                    update(root)
                    leftResult = root
                else:
                    leftPartLength = count - leftLength
                    oldRight = rightChild[root]
                    oldLength = ownLength
                    oldStart = segmentStart[root]
                    oldDirection = segmentDirection[root]

                    segmentLength[root] = leftPartLength
                    valueSum, positionSum = segmentSums(
                        leftPartLength,
                        oldStart,
                        oldDirection,
                    )
                    segmentSum[root] = valueSum
                    segmentPositionSum[root] = positionSum

                    rightPartStart = oldStart + oldDirection * leftPartLength
                    rightPartLength = oldLength - leftPartLength
                    rightPart = newNode(rightPartLength, rightPartStart, oldDirection)
                    rightResult = merge(rightPart, oldRight)

                    rightChild[root] = 0
                    update(root)
                    leftResult = root
                break
        else:
            leftResult = 0
            rightResult = 0

        while leftStack:
            node = leftStack.pop()
            rightChild[node] = leftResult
            update(node)
            leftResult = node

        while rightStack:
            node = rightStack.pop()
            leftChild[node] = rightResult
            update(node)
            rightResult = node

        return leftResult, rightResult

    def reverseRange(root, first, last):
        left, middleRight = split(root, first)
        middle, right = split(middleRight, last - first + 1)
        applyReverse(middle)
        return merge(merge(left, middle), right)

    root = newNode(size, 0, 1)
    first = 1 % size
    second = 1 % size

    for _ in range(operations):
        if first < second:
            root = reverseRange(root, first, second)
        else:
            root = reverseRange(root, second, first)

        third = first + second
        if third >= size:
            third -= size
        first, second = second, third

        third = first + second
        if third >= size:
            third -= size
        first, second = second, third

    return int(subtreePositionSum[root] % modulus) if useModulus else int(subtreePositionSum[root])


def runTests():
    assert reversalChecksum(5, 4) == 27
    assert reversalChecksum(10 ** 2, 10 ** 2) == 246_597
    assert reversalChecksum(10 ** 4, 10 ** 4) == 249_275_481_640


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = reversalChecksum(10 ** 18, 10 ** 6, MODULUS)
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")

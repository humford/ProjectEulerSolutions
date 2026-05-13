import math
import time


HEIGHT = 100.0
VELOCITY = 20.0
GRAVITY = 9.81


def firecrackerVolume(height=HEIGHT, velocity=VELOCITY, gravity=GRAVITY):
    envelopeHeight = height + velocity * velocity / (2.0 * gravity)
    return math.pi * velocity * velocity * envelopeHeight * envelopeHeight / gravity


def runTests():
    assert round(firecrackerVolume(0.0, 1.0, 1.0), 4) == round(math.pi / 4.0, 4)


if __name__ == "__main__":
    runTests()
    start = time.time()
    answer = "{:.4f}".format(firecrackerVolume())
    elapsed = time.time() - start

    print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")

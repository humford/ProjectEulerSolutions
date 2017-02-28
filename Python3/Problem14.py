import time


def collatzsequence(n):
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n /= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence


def findlongest(max):
    l = 0
    start = 0
    for x in range(max, 1, -1):
        seqlen = len(collatzsequence(x))
        if seqlen > l:
            l = seqlen
            start = x
            print(start, l)
    return start


start = time.time()
startingnumber = findlongest(int(input("Under: ")))
elapsed = (time.time() - start)

print("found %s in %s seconds" % (startingnumber, elapsed))

import time

# fast, pythonic method
def arePermutations(a, b):
    return sorted([d for d in str(a)]) == sorted([d for d in str(b)])

# other method, from StackExchange
# def arePermutations (num1, num2):
#     create array count, ten elements, all zero.
#     for each digit in num1:
#         increment count[digit]
#     for each digit in num2:
#         decrement count[digit]
#     for each item in count:
#         if item is non-zero:
#             return false
#     return true
# def arePermutations(a, b):
#     count = [0 for i in range(10)]
#     for digit in str(a):
#         count[int(digit)] += 1
#     for digit in str(b):
#         count[int(digit)] -= 1
#     for item in count:
#         if item != 0:
#             return False
#     return True

def smallestPermutedMultiple(n=2):
    for x in range(2, 999999999):
        permultiple = True
        for m in range(2, n+1):
            if not arePermutations(x, x * m):
                permultiple = False
        if permultiple:
            return x

start = time.time()
answer = smallestPermutedMultiple(6)
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
import time
from itertools import permutations

# private bool isPandigital(long n) {
#     int digits = 0;
#     int count = 0;
#     int tmp;
 
#     while (n > 0) {
#         tmp = digits;
#         digits = digits | 1 << (int)((n % 10) - 1);
#         if (tmp == digits) {
#             return false;
#         }
 
#         count++;
#         n /= 10;
#     }
#     return digits == (1 << count) - 1;
# }

# private long concat(long a, long b) {
#     long c = b;
#     while (c > 0) {
#         a *= 10;
#         c /= 10;
#     }
#     return a + b;
# }

def concat(a, b):
	return int(str(a) + str(b))

def isPandigital(nr, n):
    digits = ''.join(map(str, range(1, n + 1)))
    nr = str(nr)
    for i in digits:
        if str(i) not in nr[0:n]:
            return False
        if str(i) not in nr[-n:]:
            return False

    return True

# long result = 0;
# for (long i = 9387; i >= 9234; i--) {
#     result = concat(i, 2*i);
#     if(isPandigital(result)){
#         break;
#     }
# }

def largestPandigitalMultiple():
	result = 0
	for i in range(9387, 9234-1, -1):
		result = concat(i, 2 * i)
		if isPandigital(result, 9):
			break
	return result

start = time.time()
answer = largestPandigitalMultiple()
elapsed = (time.time() - start)

print("Found " + str(answer) + " in " + str(elapsed) + " seconds.")
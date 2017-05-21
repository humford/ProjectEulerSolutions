#cheap method
from itertools import permutations
print(int("".join([x for x in permutations("0123456789")][999999])))
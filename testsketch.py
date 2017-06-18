import random
import string
N = 10

print ''.join(random.choice('0' + '1') for _ in range(N))

import math
for i in range(12):
    n = int(20 + 18*math.sin(i/2))
    print(" "*(40-n//2) + "~"*n)

import math, time
for t in range(24):
    print("".join(" .:~"[int((math.sin(x/4+t/3)+1)*1.99)] for x in range(60)))

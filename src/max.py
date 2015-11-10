poss = [[False for i in range(14)] for j in range(14)]
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

for r in range(100):
	for t in range(100):
		if(r**t * factorial(t)) < 10**10:
			poss[r][t] = True
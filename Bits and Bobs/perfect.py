"""
    The perfect numbers up to x

    I'm fanscinated in the idea of an odd perfect number possibly existing.
"""


def perfect(x):
    for i in range(1, x):
        sum = 0
        divisors = []
        for p in range(1, i):
            if i % p == 0:
                divisors.append(p)
        for d in divisors:
            sum += d
        if i == sum:
            print(i)



"""
    Build the fibonacci sequence, find those that are modulable with their
    1-order index.
"""


def fibint(n):
    fibs = [1, 1]
    for i in range(2, n):
        fibs.append(fibs[i-1]+fibs[i-2])

    for i, f in enumerate(fibs):
        if(f % (i+1) == 0):
            print(i+1)

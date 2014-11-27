"""
    Checking ratios of things and visually depicting them.
"""

import turtle


def prime(x):
    c = 0
    for i in range(2, x):
        for p in range(2, i):
            if (i % p == 0):
                break
        else:
            turtle.sety(turtle.ycor() + 5)
            turtle.setx(turtle.xcor() + (((-1) ** c) * i))
            c += 1

prime(1000)

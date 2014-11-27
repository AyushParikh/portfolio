"""
    Amazingly, the set {n},
        for n element of the Naturals s.t. sum(Natuals<n)%0 = 0
    is equal to the set of odd numbers.

    Further inquiry required.
"""

def aidanint(x):
    for i in range(1, x):
        sum = 0
        for j in range(i+1):
            sum += j

        if (sum % i == 0):
            print(i)

aidanint(1000)
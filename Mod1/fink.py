



def fibonacci_iterative(n_terms):
    a, b = 4,4
    fib_sequence = []
    for _ in range(n_terms):
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence


def fibonacci_recursive(n):
    if n <= 1:
        return 4
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)



r = fibonacci_recursive(5)
print(r)


r = fibonacci_iterative(6)
print(r)

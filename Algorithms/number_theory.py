"""Number theory utilities.

Functions for primes, GCD/LCM, modular arithmetic, and factorisation.
"""

from __future__ import annotations


def sieve_of_eratosthenes(n: int) -> list[int]:
    """Return all primes less than or equal to ``n``.

    Args:
        n: Upper bound (inclusive). Negative input returns empty list.

    Returns:
        Sorted list of primes in [2, n].

    Complexity:
        Time: O(n log log n). Space: O(n).
    """
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            for multiple in range(p * p, n + 1, p):
                sieve[multiple] = False
    return [i for i, is_p in enumerate(sieve) if is_p]


def is_prime(n: int) -> bool:
    """Probabilistic-free primality test by trial division.

    Args:
        n: Integer to test.

    Returns:
        True if ``n`` is prime, False otherwise. ``n <= 1`` returns False;
        ``n == 2`` returns True.

    Complexity:
        Time: O(sqrt(n)). Space: O(1).
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def gcd(a: int, b: int) -> int:
    """Greatest common divisor via the Euclidean algorithm.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Non-negative gcd. ``gcd(0, 0)`` returns 0.

    Complexity:
        Time: O(log(min(a, b))). Space: O(log(min(a, b))) recursion.
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Least common multiple.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Non-negative lcm. ``lcm(0, 0)`` returns 0.

    Complexity:
        Time: O(log(min(a, b))). Space: O(1).
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def modular_exponentiation(base: int, exp: int, mod: int) -> int:
    """Compute ``base ** exp mod mod`` via repeated squaring.

    Args:
        base: Base integer (may be negative; reduced modulo ``mod``).
        exp: Non-negative exponent.
        mod: Positive modulus.

    Returns:
        ``(base ** exp) % mod``.

    Raises:
        ValueError: If mod <= 0 or exp < 0.

    Complexity:
        Time: O(log exp). Space: O(1).
    """
    if mod <= 0:
        raise ValueError("mod must be positive")
    if exp < 0:
        raise ValueError("exp must be non-negative")
    result = 1
    b = base % mod
    e = exp
    while e > 0:
        if e & 1:
            result = (result * b) % mod
        b = (b * b) % mod
        e >>= 1
    return result


def factorial(n: int) -> int:
    """Iterative factorial.

    Args:
        n: Non-negative integer.

    Returns:
        ``n!``.

    Raises:
        ValueError: If n is negative.

    Complexity:
        Time: O(n). Space: O(1).
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci(n: int) -> int:
    """Naive recursive Fibonacci (provided for complexity comparison).

    Args:
        n: Non-negative integer.

    Returns:
        F(n).

    Raises:
        ValueError: If n is negative.

    Complexity:
        Time: O(2^n) — exponential. Prefer :func:`dp.fibonacci_memo`.
        Space: O(n) recursion.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def prime_factorization(n: int) -> dict[int, int]:
    """Prime factorization by trial division.

    Args:
        n: Integer > 1.

    Returns:
        Mapping ``{prime: exponent}``. For n=1 returns ``{}``.

    Raises:
        ValueError: If n <= 0.

    Complexity:
        Time: O(sqrt(n)). Space: O(log n) for output.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    factors: dict[int, int] = {}
    x = n
    d = 2
    while d * d <= x:
        while x % d == 0:
            factors[d] = factors.get(d, 0) + 1
            x //= d
        d += 1
    if x > 1:
        factors[x] = factors.get(x, 0) + 1
    return factors


def euler_totient(n: int) -> int:
    """Euler's totient: count of integers in [1, n] coprime to n.

    Args:
        n: Positive integer.

    Returns:
        phi(n).

    Raises:
        ValueError: If n <= 0.

    Complexity:
        Time: O(sqrt(n)). Space: O(1).
    """
    if n <= 0:
        raise ValueError("n must be positive")
    result = n
    p = 2
    x = n
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            result -= result // p
        p += 1
    if x > 1:
        result -= result // x
    return result


__all__ = [
    "sieve_of_eratosthenes",
    "is_prime",
    "gcd",
    "lcm",
    "modular_exponentiation",
    "factorial",
    "fibonacci",
    "prime_factorization",
    "euler_totient",
]
""" ---------------- PROBLEM 1 ----------------"""


def equiv_to(a, m, low, high):
    # return the list of integers x in [low, high] for which x ≡ a (mod m)
    # If m == 0, congruence modulo 0 means equality (x == a).
    x_vals = []
    if m == 0:
        # only include a if it's in the range
        if low <= a <= high:
            return [a]
        return []

    mod = abs(m)
    # Python's % gives a non-negative representative for negative a as well
    target = a % mod
    for x in range(low, high + 1):
        if x % mod == target:
            x_vals.append(x)
    return x_vals


""" ---------------- PROBLEM 2 ----------------"""


def b_rep(n, b):
    # simple base-b representation for non-negative integers (supports hex digits)
    if n == 0:
        return '0'
    digits = []  # stores the digits of the b-representation of n
    q = n
    while q != 0:
        digit = q % b
        if b == 16 and digit > 9:
            hex_dict = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
            digit = hex_dict[digit]
        digits.append(str(digit))
        q = q // b
    return ''.join(reversed(digits))


""" ---------------- PROBLEM 3 ----------------"""


def binary_add(a, b):
    # removing all whitespace from the strings
    a = a.replace(' ', '')
    b = b.replace(' ', '')

    # padding the strings with 0's so they are the same length
    if len(a) < len(b):
        diff = len(b) - len(a)
        a = "0" * diff + a
    elif len(a) > len(b):
        diff = len(a) - len(b)
        b = "0" * diff + b

    # addition algorithm
    result = ""
    carry = 0
    for i in reversed(range(len(a))):
        a_i = int(a[i])
        b_i = int(b[i])

        total = a_i + b_i + carry
        digit = total % 2
        carry = total // 2
        result = str(digit) + result
    if carry == 1:
        result = '1' + result
    return result


""" ---------------- PROBLEM 4 ----------------"""


def binary_mul(a, b):
    # removing all whitespace from the strings
    a = a.replace(' ', '')
    b = b.replace(' ', '')

    # multiplication algorithm
    partial_products = []
    i = 0  # index of the current bit of string 'a' beginning at 0, right-to-left
    for bit in reversed(a):
        if bit == '1':
            # partial product is b shifted left by i (append i zeros)
            partial_products.append(b + ('0' * i))
        i += 1

    result = '0'
    while len(partial_products) > 0:
        result = binary_add(result, partial_products[0])
        del partial_products[0]

    # normalize result (remove leading zeros, but keep at least one zero)
    result = result.lstrip('0')
    if result == '':
        result = '0'
    return result
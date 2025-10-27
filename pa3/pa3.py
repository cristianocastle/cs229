import util

""" ----------------- PROBLEM 1 ----------------- """


def affine_encrypt(text, a, b):
    # Check if gcd(a, 26) == 1
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    if gcd(a, 26) != 1:
        raise ValueError("The given key is invalid.")
    cipher = ""
    for letter in text:
        if letter.isalpha():
            letter = letter.upper()
            num = ord(letter) - 65
            cipher_num = (a * num + b) % 26
            cipher_digits = str(cipher_num)
            if len(cipher_digits) == 1:
                cipher_digits = "0" + cipher_digits
            cipher += util.digits2letters(cipher_digits)
    return cipher


""" ----------------- PROBLEM 2 ----------------- """


def affine_decrypt(ciphertext, a, b):
    # Check if gcd(a, 26) == 1
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    if gcd(a, 26) != 1:
        raise ValueError("The given key is invalid.")
    # Compute modular inverse of a mod 26
    def mod_inv(a, m):
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError("No modular inverse")
    a_inv = mod_inv(a, 26)
    text = ""
    for letter in ciphertext:
        if letter.isalpha():
            letter = letter.upper()
            num = ord(letter) - 65
            plain_num = (a_inv * (num - b)) % 26
            letter_digits = str(plain_num)
            if len(letter_digits) == 1:
                letter_digits = "0" + letter_digits
            text += util.digits2letters(letter_digits)
    return text


""" ----------------- PROBLEM 3 ----------------- """


def rsa_encrypt(plaintext, n, e):
    text = plaintext.replace(' ', '')
    digits = util.letters2digits(text)
    l = util.blocksize(n)
    while len(digits) % l != 0:
        digits += "23"
    blocks = [digits[i:i + l] for i in range(0, len(digits), l)]
    cipher = ""
    for b in blocks:
        block_int = int(b)
        encrypted_int = pow(block_int, e, n)
        encrypted_block = str(encrypted_int)
        if len(encrypted_block) < l:
            encrypted_block = encrypted_block.zfill(l)
        cipher += encrypted_block
    return cipher


""" ----------------- PROBLEM 4 ----------------- """


def rsa_decrypt(cipher, p, q, e):
    n = p * q
    ciphertext = cipher.replace(' ', '')
    l = util.blocksize(n)
    blocks = [ciphertext[i:i + l] for i in range(0, len(ciphertext), l)]
    text = ""
    # Compute modular inverse of e mod (p-1)*(q-1)
    phi_n = (p - 1) * (q - 1)
    def mod_inv(a, m):
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError("No modular inverse")
    e_inv = mod_inv(e, phi_n)
    for b in blocks:
        block_int = int(b)
        decrypted_int = pow(block_int, e_inv, n)
        decrypted_block = str(decrypted_int)
        if len(decrypted_block) < l:
            decrypted_block = decrypted_block.zfill(l)
        text += util.digits2letters(decrypted_block)
    return text

"""Caesar Encrypter/Decrypter"""


def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ptbl = list(plaintext)
    ciphertext = ""
    for i in ptbl:
        if "A" <= i <= "Z":
            ciphertext += chr(ord("A") + (ord(i) - ord("A") + 3) % 26)
        elif "a" <= i <= "z":
            ciphertext += chr(ord("a") + (ord(i) - ord("a") + 3) % 26)
        else:
            ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    ctbl = list(ciphertext)
    plaintext = ""
    for i in ctbl:
        if "A" <= i <= "Z":
            plaintext += chr(ord("A") + (26 + ord(i) - ord("A") - 3) % 26)
        elif "a" <= i <= "z":
            plaintext += chr(ord("a") + (26 + ord(i) - ord("a") - 3) % 26)
        else:
            plaintext += i
    return plaintext

""""Vigener Encrypter/Decrypter"""


def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ptbl = list(plaintext)
    kwbl = list(keyword)
    ptl = len(plaintext)
    kwl = len(keyword)
    ciphertext = ""
    for i in range(ptl):
        change = 0
        if "A" <= kwbl[i % kwl] <= "Z":
            change = ord(kwbl[i % kwl]) - ord("A")
        elif "a" <= ptbl[i] <= "z":
            change = ord(kwbl[i % kwl]) - ord("a")
        if "A" <= ptbl[i] <= "Z":
            ciphertext += chr(ord("A") + (ord(ptbl[i]) - ord("A") + change) % 26)
        elif "a" <= ptbl[i] <= "z":
            ciphertext += chr(ord("a") + (ord(ptbl[i]) - ord("a") + change) % 26)
        else:
            ciphertext += ptbl[i]
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    ctbl = list(ciphertext)
    kwbl = list(keyword)
    ctl = len(ciphertext)
    kwl = len(keyword)
    plaintext = ""
    for i in range(ctl):
        change = 0
        if "A" <= kwbl[i % kwl] <= "Z":
            change = ord(kwbl[i % kwl]) - ord("A")
        elif "a" <= ctbl[i] <= "z":
            change = ord(kwbl[i % kwl]) - ord("a")
        if "A" <= ctbl[i] <= "Z":
            plaintext += chr(ord("A") + (26 + ord(ctbl[i]) - ord("A") - change) % 26)
        elif "a" <= ctbl[i] <= "z":
            plaintext += chr(ord("a") + (26 + ord(ctbl[i]) - ord("a") - change) % 26)
        else:
            plaintext += ctbl[i]
    return plaintext

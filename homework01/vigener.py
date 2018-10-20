def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    def pt_letter(letter,kletter):

        change=0
        if ("A" <= kletter <= "Z"):
            change=ord(kletter) - ord("A")
        elif ("a" <= letter <= "z"):
            change=ord(kletter) - ord("a")

        if ("A" <= letter <= "Z"):
            return chr(ord("A") + (ord(letter) - ord("A") + change) % 26)
        elif ("a" <= letter <= "z"):
            return chr(ord("a") + (ord(letter) - ord("a") + change) % 26)
        else:
            return letter

    ptbl=list(plaintext)
    kwbl=list(keyword)
    ptl=len(plaintext)
    kwl=len(keyword)
    ciphertext=""
    for i in range(ptl):
        ciphertext += pt_letter(ptbl[i],kwbl[i%kwl])
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
    def ct_letter(letter,kletter):

        change=0
        if ("A" <= kletter <= "Z"):
            change=ord(kletter) - ord("A")
        elif ("a" <= letter <= "z"):
            change=ord(kletter) - ord("a")

        if ("A" <= letter <= "Z"):
            return chr(ord("A") + (26 + ord(letter) - ord("A") - change) % 26)
        elif ("a" <= letter <= "z"):
            return chr(ord("a") + (26 + ord(letter) - ord("a") - change) % 26)
        else:
            return letter
        
    ctbl=list(ciphertext)
    kwbl=list(keyword)
    ctl=len(ciphertext)
    kwl=len(keyword)
    plaintext=""
    for i in range(ctl):
        plaintext += ct_letter(ctbl[i],kwbl[i%kwl])
    return plaintext

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

    def pt_letter(letter):

        if ("A" <= letter <= "Z"):
            return chr(ord("A") + (ord(letter) - ord("A") + 3) % 26)
        elif ("a" <= letter <= "z"):
            return chr(ord("a") + (ord(letter) - ord("a") + 3) % 26)
        else:
            return letter


    ptbl=list(plaintext)
    ciphertext=""
    for i in ptbl:
        ciphertext += pt_letter(i)
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
    def ct_letter(letter):

        if ("A" <= letter <= "Z"):
            return chr(ord("A") + (26 + ord(letter) - ord("A") - 3) % 26)
        elif ("a" <= letter <= "z"):
            return chr(ord("a") + (26 + ord(letter) - ord("a") - 3) % 26)
        else:
            return letter

    ctbl=list(ciphertext)
    plaintext=""
    for i in ctbl:
        plaintext += ct_letter(i)
    return plaintext

ALPHABET_LENGTH: int = 128

def encrypt(plaintext: str, key: int) -> str:
    ciphertext: str = ""
    for letter in plaintext:
        ciphertext += chr((ord(letter) + key) % ALPHABET_LENGTH)
    
    return ciphertext

def decrypt(ciphertext: str, key: int) -> str:
    plaintext: str = ""
    for letter in ciphertext:
        plaintext += chr((ord(letter) - key) % ALPHABET_LENGTH)

    return plaintext

def main() -> int:
    key: int = 3
    plaintext: str = "Adirtka"
    encrypted_text: str = encrypt(plaintext, key)
    decrypted_text: str = decrypt(encrypted_text, key)
    print(f"{plaintext=}")
    print(f"{encrypted_text=}")
    print(f"{decrypted_text=}")
    return 0


if __name__ == "__main__":
    main()
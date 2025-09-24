from LFSR import LFSR


def encrypt(plaintext: str, lfsr: LFSR) -> bytes:
    """Шифрует строку с помощью LFSR и XOR."""
    string_bytes = plaintext.encode("utf-8")          # исходный текст в байтах
    keystream = lfsr.bytes(len(string_bytes))         # столько же байтов ключевого потока
    encrypted = bytes(a ^ b for a, b in zip(string_bytes, keystream))
    return encrypted


def decrypt(ciphertext: bytes, lfsr: LFSR) -> str:
    """Расшифровка: повторяем XOR с тем же LFSR."""
    keystream = lfsr.bytes(len(ciphertext))
    decrypted = bytes(a ^ b for a, b in zip(ciphertext, keystream))
    return decrypted.decode("utf-8")


def main() -> None:
    seed = 0b1011
    taps = [0, 1]
    lfsr_enc = LFSR(seed, taps)
    plaintext = "Даня"
    ciphertext = encrypt(plaintext, lfsr_enc)
    print("Cipher (hex):", ciphertext.hex())

    # для расшифровки нужен новый LFSR с тем же seed и taps
    lfsr_dec = LFSR(seed, taps)
    decrypted = decrypt(ciphertext, lfsr_dec)
    print("Decrypted:", decrypted)


if __name__ == "__main__":
    main()

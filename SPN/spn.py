BLOCK_SIZE = 16
SBOX_SIZE = 4
ROUNDS = 4


def s_box_permutation(bits: int, invert=False) -> int:
    nibble_size: int = 4
    s_box: dict[int, int] = {
        0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
        0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
        0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
        0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7,
    }
    if invert:
        s_box = {v: k for k, v in s_box.items()}

    out: int = 0
    for i in range(BLOCK_SIZE // SBOX_SIZE):
        nibble = (bits >> (SBOX_SIZE * i)) & 0xF
        new_int = s_box[nibble]
        out |= new_int << (SBOX_SIZE * i)
    return out


def p_box_permutation(bits: int, invert=False) -> int:
    p_block = [1, 5, 9, 13,
               2, 6, 10, 14,
               3, 7, 11, 15,
               4, 8, 12, 16]
    p_block = [x - 1 for x in p_block]  # сделаем 0-базовым

    if invert:
        inv_p = [0] * len(p_block)
        for i, p in enumerate(p_block):
            inv_p[p] = i
        p_block = inv_p

    out = 0
    for i, pos in enumerate(p_block):
        bit = (bits >> pos) & 1
        out |= bit << i
    return out


def get_round_keys(master_key: int) -> list[int]:
    round_keys = []
    for r in range(ROUNDS + 1):
        shift = 16 - 4 * r
        shifted = (master_key >> shift) & 0xFFFF
        round_keys.append(shifted)
    return round_keys


def encrypt(message: int, key: int, inverted=False) -> int:
    round_keys = get_round_keys(key)
    w = message
    for i in range(ROUNDS - 1):
        round_key = round_keys[i]
        u = w ^ round_key
        v = s_box_permutation(u, inverted)
        w = p_box_permutation(v, inverted)
        # print(f"{bin(round_key)=}\n{bin(u)=}\n{bin(v)=}\n{bin(w)=}\n")

    final_state = w ^ round_keys[ROUNDS - 1]
    final_state = s_box_permutation(final_state, inverted)
    final_state = final_state ^ round_keys[ROUNDS]
    return final_state


def decrypt(ciphertext: int, key: int) -> int:
    round_keys = get_round_keys(key)
    w = ciphertext ^ round_keys[-1]
    w = s_box_permutation(w, invert=True)
    w ^= round_keys[-2]

    for i in range(ROUNDS-2, -1, -1):
        w = p_box_permutation(w, invert=True)
        w = s_box_permutation(w, invert=True)
        w ^= round_keys[i]
    return w


def main() -> None:
    """Entry point."""
    key = 0b00111010100101001101011000111111
    x = 0b0010011010110111
    ciphertext = encrypt(x, key)
    print(ciphertext)
    decrypted = decrypt(ciphertext, key)
    print(decrypted)
    print(x)


if __name__ == '__main__':
    main()

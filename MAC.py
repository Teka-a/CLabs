import format as f
import Magma as m
import Kuznechik as h

#  ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff  Magma
#  8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef  Kuznechik
def set_params():
    while True:
        key = input("Введите ключ в 16-ом формате, длиной 64: ")
        key = key.lower()
        if f.is_hex_alphabet(key):
            if len(key) == 64:
                break
            else:
                print("Ключ должен быть длины 64!")
        else:
            print("Ключ содержит недопустимые символы!")
    while True:
        try:
            print("Доступные алгоритмы шифрования: \n\t1. Магма. "
                  "\n\t2. Кузнечик.")

            algo = int(input("Выберите алгоритм шифрования: "))
            break
        except ValueError:
            print("Введите число!")
    return [key, algo]


def get_add_keys(key: str, block: int) -> list:
    if block == 64:
        R = m.encrypt("0" * 64, key)
        B = "0"*59 + "11011"
    else:
        R = h.encrypt("0" * 128, key)
        B = "0" * 120 + "10000111"
    R = bin(int(R, 16))[2:].zfill(block)

    if f.MSB(R, 1) == "0":
        K1 = bin(int(R, 2) << 1)[2:][:block].zfill(block)

    else:
        K1 = bin(int(f.XOR(hex((int(R, 2) << 1))[3:], hex(int(B, 2))[2:].zfill(block//4), block//4), 16))[2:].zfill(block)

    if f.MSB(K1, 1) == "0":
        K2 = bin(int(K1, 2) << 1)[2:][:block].zfill(block)
    else:
        K2 = bin(int(f.XOR(hex((int(K1, 2) << 1))[2:], B, block // 4), 16))[2:].zfill(block)

    return [hex(int(K1, 2))[2:], hex(int(K2, 2))[2:]]


def blocks_64(text: str, key: str, do: str):
    output = ""
    s = 32
    for start in range(0, len(text) - 16, 16):
        if do == "encrypt":
            P = text[start:start + 16]
            # "Зацепление"
            if start == 0:
                P_xor_C = P
            else:
                P_xor_C = f.XOR(P, output[start-16:start], 16)
            # Шифрование
            C = m.encrypt(P_xor_C, key)
            output += C
        elif do == "decrypt":
            C = text[start:start + 16]
            # Расшифрование
            P = m.decrypt(C, key)
            # Убрать "зацепление"
            if start == 0:
                C_xor_P = P
            else:
                C_xor_P = f.XOR(P, text[start - 16:start], 16)
            output += C_xor_P
    add_keys = get_add_keys(key, 64)
    K = ""
    # Выбор дополнительного ключа
    if len(text[start + 16:]) == 16:
        K = add_keys[0]
    else:
        K = add_keys[1]
    # Обработка последнего блока
    if do == "encrypt":
        block = f.XOR(text[start + 16:start + 32], output[start:start+16], 16)
        block = f.XOR(block, K, 16)
        C = m.encrypt(block, key)
        output += C
        # Выработка МАС
        MAC = f.MSB(C, s//4)
        print("MAC: ", MAC)
    elif do == "decrypt":
        C = text[start+16:start + 32]
        # Расшифрование
        P = m.decrypt(C, key)
        C_xor_P = f.XOR(P, text[start:start+16], 16)
        C_xor_P = f.XOR(C_xor_P, K, 16)
        output += C_xor_P
    return output

def blocks_128(text: str, key: str, do: str):
    output = ""
    s = 64
    for start in range(0, len(text) - 32, 32):
        if do == "encrypt":
            P = text[start:start + 32]
            # "Зацепление"
            if start == 0:
                P_xor_C = P
            else:
                P_xor_C = f.XOR(P, output[start - 32:start], 32)
            # Шифрование
            C = h.encrypt(P_xor_C, key)
            output += C
        elif do == "decrypt":
            C = text[start:start + 32]
            # Расшифрование
            P = h.decrypt(C, key)
            # Убрать "зацепление"
            if start == 0:
                C_xor_P = P
            else:
                C_xor_P = f.XOR(P, text[start - 32:start], 32)
            output += C_xor_P
    add_keys = get_add_keys(key, 128)
    K = ""
    # Выбор дополнительного ключа
    if len(text[start + 32:]) == 32:
        K = add_keys[0]
    elif len(text[start:]) < 32:
        K = add_keys[1]
    # Обработка последнего блока
    if do == "encrypt":
        block = f.XOR(text[start + 32:start + 64], output[start:start+32], 32)
        block = f.XOR(block, K, 32)
        C = h.encrypt(block, key)
        output += C
        # Выработка МАС
        MAC = f.MSB(C, s//4)
        print("MAC: ", MAC)
    elif do == "decrypt":
        C = text[start+32:start + 64]
        P = h.decrypt(C, key)
        C_xor_P = f.XOR(P, text[start:start+32], 32)
        C_xor_P = f.XOR(C_xor_P, K, 32)
        output += C_xor_P
    return output

def main():
    print("Выбран Режим выработки имитовставки")
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Зашифровать (из to-encrypt.txt в to-decrypt.txt). "
              "\n\t2. Расшифровать (из to-decrypt.txt в result.txt).")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            [key, algo] = set_params()

            text = f.read_from_file("to-encrypt.txt")
            #  Подготовка строки для шифрования
            prepared = f.replace_empty_symbols(text, 1)
            if not f.is_hex_alphabet(prepared):
                #  Преобразовать в 16 формат
                prepared = f.prepare_in(text, 1, 16)
            if algo == 1:
                key = bin(int(key, 16))[2:]
                encrypted = f.prepare_out(blocks_64(prepared, key, "encrypt"), 1)
            else:
                encrypted = f.prepare_out(blocks_128(prepared, key, "encrypt"), 1)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            [key, algo] = set_params()
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            if algo == 1:
                key = bin(int(key, 16))[2:]
                decrypted = blocks_64(prepared, key, "decrypt")
            else:
                decrypted = blocks_128(prepared, key, "decrypt")

            print("Нужно ли преобразовать в буквы русского алфавита?"
                  "\n\t0. Нет. "
                  "\n\t1. Да. ")
            need = int(input("Выберите опцию: "))

            if need == 1:
                #  Преобразовать из 16 формата в буквы русского алфавита
                decrypted = f.prepare_out(decrypted, 2, 16)

            f.write_to_file("result.txt", decrypted, 2)

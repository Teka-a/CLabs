import format as f


K = [
    ["c", "4", "6", "2", "a", "5", "b", "9", "e", "8", "d", "7", "0", "3", "f", "1"],
    ["6", "8", "2", "3", "9", "a", "5", "c", "1", "e", "4", "7", "b", "d", "0", "f"],
    ["b", "3", "5", "8", "2", "f", "a", "d", "e", "1", "7", "4", "c", "9", "6", "0"],
    ["c", "8", "2", "1", "d", "4", "f", "6", "7", "0", "a", "5", "3", "e", "9", "b"],
    ["7", "f", "5", "a", "8", "1", "6", "d", "0", "9", "3", "e", "b", "4", "2", "c"],
    ["5", "d", "f", "6", "9", "2", "c", "a", "b", "7", "8", "1", "4", "3", "e", "0"],
    ["8", "e", "2", "5", "6", "9", "1", "c", "f", "4", "b", "0", "d", "a", "3", "7"],
    ["1", "7", "e", "d", "0", "5", "8", "3", "4", "f", "a", "6", "9", "c", "b", "2"]
]


#  Ключ в 16-ом формате должен быть длины 64 ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff
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
    return key


def cipher_cycle(j: int, N1: str, N2: str, X: dict) -> list:
    CM1 = str(bin((int(N1, 2) + int(X.get(f'X{j}'), 2)) % (2 ** 32))[2:]).zfill(32)
    CM = CM1.zfill(32)
    CM1 = {}
    R = {}
    for i in range(8):
        CM1[8 - i] = CM[i * 4:i * 4 + 4]

    for j in range(8, 1, -1):
        R[j] = "0000"
    m = 1
    while m <= 8:
        L = int(CM1.get(m), 2)
        R[m] = bin(int(K[m - 1][L], 16))[2:].zfill(4)
        m += 1
    R_str = ""
    for r in R:
        R_str += R.get(r)
    R_str = R_str[11:] + R_str[:11]
    CM2 = str(bin((int(R_str, 2) ^ int(N2, 2)))[2:]).zfill(32)
    N1 = N1.zfill(32)
    return [N1, CM2]


def get_keys(key: str) -> dict:
    #расширение ключа
    keys = {"X0": key[0:32],
            "X1": key[32:64],
            "X2": key[64:96],
            "X3": key[96:128],
            "X4": key[128:160],
            "X5": key[160:192],
            "X6": key[192:224],
            "X7": key[224:256]}
    return keys


def encrypt(text: str, X: str) -> str:
    #  Расширяем ключ
    X = get_keys(X)
    #  Разбиваем на 2 "ветви"
    N2 = bin(int(text[:8], 16))[2:].zfill(32)
    N1 = bin(int(text[8:], 16))[2:].zfill(32)
    j2 = 1
    #  3*8 (24) цикла с ключом в исходной последовательности
    while j2 <= 3:
        j1 = 0
        while j1 <= 7:
            [N1, CM2] = cipher_cycle(j1, N1, N2, X)
            N2 = N1.zfill(32)
            N1 = CM2.zfill(32)
            j1 += 1
        j2 += 1
    j1 = 7
    #  Последние 8 циклов с ключом в обратной последовательности
    while j1 != 0:
        [N1, CM2] = cipher_cycle(j1, N1, N2, X)
        N2 = N1.zfill(32)
        N1 = CM2.zfill(32)
        j1 -= 1
    [N1, CM2] = cipher_cycle(j1, N1, N2, X)
    N2 = N1.zfill(32)
    N1 = CM2.zfill(32)
    encrypted = hex(int(N1, 2))[2:].zfill(8) + hex(int(N2, 2))[2:].zfill(8)
    return encrypted


def decrypt(text: str, X: str) -> str:
    #  Расширяем ключ
    X = get_keys(X)
    #  Разбиваем на 2 "ветви"
    N2 = bin(int(text[:8], 16))[2:].zfill(32)
    N1 = bin(int(text[8:], 16))[2:].zfill(32)
    j1 = 0
    #  8 циклов с ключом в обратной последовательности
    while j1 <= 7:
        [N1, CM2] = cipher_cycle(j1, N1, N2, X)
        N2 = N1.zfill(32)
        N1 = CM2.zfill(32)
        j1 += 1
    j2 = 1
    while j2 <= 2:
        j1 = 7
        while j1 >= 0:
            [N1, CM2] = cipher_cycle(j1, N1, N2, X)
            N2 = N1.zfill(32)
            N1 = CM2.zfill(32)
            j1 -= 1
        j2 += 1
    j1 = 7
    while j1 != 0:
        [N1, CM2] = cipher_cycle(j1, N1, N2, X)
        N2 = N1.zfill(32)
        N1 = CM2.zfill(32)
        j1 -= 1
    [N1, CM2] = cipher_cycle(j1, N1, N2, X)
    N2 = N1.zfill(32)
    N1 = CM2.zfill(32)
    decrypted = hex(int(N1, 2))[2:].zfill(8) + hex(int(N2, 2))[2:].zfill(8)
    return decrypted


def blocks_64(text: str, key: str, do: str):
    output = ""
    if do == "encrypt":
        text = f.procedure2(text, 64)
    for start in range(0, len(text), 16):
        if do == "encrypt":
            output += encrypt(text[start:start + 16], key).zfill(16)
        elif do == "decrypt":
            output += decrypt(text[start:start + 16], key).ljust(16, "0")
    if do == "decrypt":
        output = f.unprocedure2(output)
    return output

def main():
    print("Выбран шифр 28147-89.")
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Зашифровать (из to-encrypt.txt в to-decrypt.txt). "
              "\n\t2. Расшифровать (из to-decrypt.txt в result.txt).")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            key = set_params()
            key = bin(int(key, 16))[2:]
            text = f.read_from_file("to-encrypt.txt")
            #  Подготовка строки для шифрования
            prepared = f.replace_empty_symbols(text, 1)
            if not f.is_hex_alphabet(prepared):
                #  Преобразовать в 16 формат
                prepared = f.prepare_in(text, 1, 16)
            encrypted = f.prepare_out(blocks_64(prepared, key, "encrypt"), 1)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            key = set_params()
            key = bin(int(key, 16))[2:]
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = blocks_64(prepared, key, "decrypt")
            print("Нужно ли преобразовать в буквы русского алфавита?"
                  "\n\t0. Нет. "
                  "\n\t1. Да. ")
            need = int(input("Выберите опцию: "))

            if need == 1:
                #  Преобразовать из 16 формата в буквы русского алфавита
                decrypted = f.prepare_out(decrypted, 2, 16)

            f.write_to_file("result.txt", decrypted, 2)

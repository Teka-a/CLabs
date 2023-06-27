import format as f

#  Маски для регистров длиной 19, 22, 23
R1MASK = 0x07FFFF
R2MASK = 0x3FFFFF
R3MASK = 0x7FFFFF

#  8 бит
R1MID = 0x000100
#  10 бит
R2MID = 0x000400
#  10 бит
R3MID = 0x000400

#  биты 18, 17, 16, 13
R1TAPS = 0x072000
#  биты 21, 20
R2TAPS = 0x300000
#  биты 22, 21, 20, 7
R3TAPS = 0x700080

#  Старшие биты регистров
R1OUT = 0x040000
R2OUT = 0x200000
R3OUT = 0x400000

R1, R2, R3 = 0, 0, 0


#  1110111011101110111011101110111111001111110011101110111011101110
def set_params():
    while True:
        key = input("Введите ключ в 2-ом формате, длиной 64: ")
        if f.is_bin(key):
            if len(key) == 64:
                key_mas = []
                for i in range(8):
                    key_mas.append(int(key[i*8:i*8 + 8], 2))
                break
            else:
                print("Ключ должен быть длины 64!")
        else:
            print("Ключ содержит недопустимые символы!")
    while True:
        try:
            frame = int(input("Введите номер кадра: "))
            frame = bin(frame)[2:].zfill(22)
            frame = int(frame, 2)
            break
        except ValueError:
            print("Введите число!")
    return [key_mas, frame]


def xor(text: str, gamma: str) -> str:
    print(f"Текст: {text}")
    print(f"Гамма: {gamma}")
    res_xor = ""
    for i in range(114):
        res_xor += str(int(text[i], 2) ^ int(gamma[i], 2))
    return res_xor


def parity(x):
    x ^= x >> 16
    x ^= x >> 8
    x ^= x >> 4
    x ^= x >> 2
    x ^= x >> 1
    return x & 1


def clockone(reg, mask, taps):
    t = reg & taps
    reg = (reg << 1) & mask
    reg |= parity(t)
    return reg


def majority():
    sum = parity(R1 & R1MID) + parity(R2 & R2MID) + parity(R3 & R3MID)
    if sum >= 2:
        return 1
    else:
        return 0


def clock():
    global R1, R2, R3
    maj = majority()
    print(f"F = {maj}")
    print(f"8 бит R1 {bin(R1)[2:].zfill(19)[-9]}")
    print(f"10 бит R2 {bin(R2)[2:].zfill(22)[-11]}")
    print(f"10 бит R2 {bin(R3)[2:].zfill(23)[-11]}")
    if ((R1 & R1MID) != 0) == maj:
        print(f"Нужно сдвинуть R1: {bin(R1)[2:].zfill(19)}")
        R1 = clockone(R1, R1MASK, R1TAPS)
        print(f"R1 {bin(R1)[2:].zfill(19)}")
    if ((R2 & R2MID) != 0) == maj:
        print(f"Нужно сдвинуть R2: {bin(R2)[2:].zfill(22)}")
        R2 = clockone(R2, R2MASK, R2TAPS)
        print(f"R2 {bin(R1)[2:].zfill(22)}")
    if ((R3 & R3MID) != 0) == maj:
        print(f"Нужно сдвинуть R3: {bin(R3)[2:].zfill(23)}")
        R3 = clockone(R3, R3MASK, R3TAPS)
        print(f"R3 {bin(R1)[2:].zfill(23)}")


def clockallthree():
    global R1, R2, R3
    R1 = clockone(R1, R1MASK, R1TAPS)
    R2 = clockone(R2, R2MASK, R2TAPS)
    R3 = clockone(R3, R3MASK, R3TAPS)


def keysetup(key, frame):
    global R1, R2, R3
    R1, R2, R3 = 0, 0, 0
    print("Загрузка ключа, 64 такта: ")
    print("Изначально")
    print(f"R1 {bin(R1)[2:].zfill(19)}")
    print(f"R2 {bin(R2)[2:].zfill(22)}")
    print(f"R3 {bin(R3)[2:].zfill(23)}")
    for i in range(64):
        print(f"Такт {i}")
        clockallthree()
        keybit = (key[i // 8] >> (i & 7)) & 1
        R1 ^= keybit
        R2 ^= keybit
        R3 ^= keybit
        print("Бит ключа", keybit)
        print("После загрузки бита ключа: ")
        print(f"R1 {bin(R1)[2:].zfill(19)}")
        print(f"R2 {bin(R2)[2:].zfill(22)}")
        print(f"R3 {bin(R3)[2:].zfill(23)}")
    print("Загрузка кадра, 22 такта: ")
    print("Изначально")
    print(f"R1 {bin(R1)[2:].zfill(19)}")
    print(f"R2 {bin(R2)[2:].zfill(22)}")
    print(f"R3 {bin(R3)[2:].zfill(23)}")
    for i in range(22):
        print(f"Такт {i}")
        clockallthree()
        framebit = (frame >> i) & 1
        R1 ^= framebit
        R2 ^= framebit
        R3 ^= framebit
        print("Бит кадра", framebit)
        print("После загрузки бита кадра: ")
        print(f"R1 {bin(R1)[2:].zfill(19)}")
        print(f"R2 {bin(R2)[2:].zfill(22)}")
        print(f"R3 {bin(R3)[2:].zfill(23)}")
    print("100 тактов без генерации последовательности: ")
    print("Изначально")
    print(f"R1 {bin(R1)[2:].zfill(19)}")
    print(f"R2 {bin(R2)[2:].zfill(22)}")
    print(f"R3 {bin(R3)[2:].zfill(23)}")
    print(f"R1: {parity(R1 & R1OUT)}, R2: {parity(R2 & R2OUT)}, R3: {parity(R3 & R3OUT)}")
    for i in range(100):
        print(f"Такт {i}")
        clock()
        print("После сдвига: ")
        print(f"R1 {bin(R1)[2:].zfill(19)}")
        print(f"R2 {bin(R2)[2:].zfill(22)}")
        print(f"R3 {bin(R3)[2:].zfill(23)}")


def get_gamma():
    gamma = ""
    print("Изначально")
    print(f"R1 {bin(R1)[2:].zfill(19)}")
    print(f"R2 {bin(R2)[2:].zfill(22)}")
    print(f"R3 {bin(R3)[2:].zfill(23)}")
    for i in range(114):
        print(f"Такт {i}")
        clock()
        print(f"R1 {parity(R1 & R1OUT)}")
        print(f"R2 {parity(R2 & R2OUT)}")
        print(f"R3 {parity(R3 & R3OUT)}")
        gamma += str(parity(R1 & R1OUT) ^ parity(R2 & R2OUT) ^ parity(R3 & R3OUT))
        print(f"Гамма: {gamma}")

    return gamma


def blocks_114(text: str, key: list, frame, do: str):
    output = ""

    if do == "encrypt":
        text = bin(int(text, 16))[2:]
        text = text.zfill(len(text) + (114 - len(text) % 114))
    print(text)
    for start in range(0, len(text), 114):
        if do == "encrypt":
            plaintext = text[start:start + 114]
            keysetup(key, frame)
            print("Генерация гаммы")
            gamma = get_gamma()
            output += xor(plaintext, gamma)
            frame += 1
        elif do == "decrypt":
            ciphertext = text[start:start + 114]
            keysetup(key, frame)
            gamma = get_gamma()
            output += xor(ciphertext, gamma)
            frame += 1
    if do == "decrypt":
        output = hex(int(output, 2))[2:]
    return output


def main():
    print("Выбран шифр a5/1.")
    [key, frame] = set_params()
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Зашифровать (из to-encrypt.txt в to-decrypt.txt). "
              "\n\t2. Расшифровать (из to-decrypt.txt в result.txt).")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            text = f.read_from_file("to-encrypt.txt")
            #  Подготовка строки для шифрования
            prepared = f.replace_empty_symbols(text, 1)
            if not f.is_hex_alphabet(prepared):
                #  Преобразовать в 16 формат
                prepared = f.prepare_in(text, 1, 16)
            encrypted = f.prepare_out(blocks_114(prepared, key, frame, "encrypt"), 1)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = blocks_114(prepared, key, frame, "decrypt")
            print("Нужно ли преобразовать в буквы русского алфавита?"
                  "\n\t0. Нет. "
                  "\n\t1. Да. ")
            need = int(input("Выберите опцию: "))

            if need == 1:
                #  Преобразовать из 16 формата в буквы русского алфавита
                decrypted = f.prepare_out(decrypted, 2, 16)

            f.write_to_file("result.txt", decrypted, 2)


import format as f

R1MASK = 0x07FFFF
R2MASK = 0x3FFFFF
R3MASK = 0x7FFFFF
R4MASK = 0x01FFFF

R4TAP1 = 0x000400
R4TAP2 = 0x000008
R4TAP3 = 0x000080

R1TAPS = 0x072000
R2TAPS = 0x300000
R3TAPS = 0x700080
R4TAPS = 0x010800

R1, R2, R3, R4 = 0, 0, 0, 0


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
    res_xor = ""
    print(f"Текст: {text}")
    print(f"Гамма: {gamma}")
    for i in range(114):
        res_xor += str(int(text[i], 2) ^ int(gamma[i], 2))
    return res_xor


#  Сумма битов по модулю 2
def parity(x):
    x ^= x >> 16
    x ^= x >> 8
    x ^= x >> 4
    x ^= x >> 2
    x ^= x >> 1
    return x & 1


def clockone(reg, mask, taps, loaded_bit):
    t = reg & taps
    reg = (reg << 1) & mask
    reg |= parity(t)
    reg |= loaded_bit
    return reg


def majority(w1, w2, w3):
    sum = (w1 != 0) + (w2 != 0) + (w3 != 0)
    if sum >= 2:
        return 1
    else:
        return 0


def clock(allP, loaded):
    global R1, R2, R3, R4
    print(f"Биты синхронизации R4: {bin(R4)[2:].zfill(17)[-4]}(3), {bin(R4)[2:].zfill(17)[-8]}(7), {bin(R4)[2:].zfill(17)[-11]}(10)")
    maj = majority(R4&R4TAP1, R4&R4TAP2, R4&R4TAP3)
    print(f"F = {maj}")
    if allP or (((R4&R4TAP1)!=0) == maj):
        print(f"Нужно сдвинуть R1: {bin(R1)[2:].zfill(19)}")
        R1 = clockone(R1, R1MASK, R1TAPS, loaded << 15)
        print(f"R1 {bin(R1)[2:].zfill(19)}")
    if allP or (((R4&R4TAP2)!=0) == maj):
        print(f"Нужно сдвинуть R2: {bin(R2)[2:].zfill(22)}")
        R2 = clockone(R2, R2MASK, R2TAPS, loaded << 16)
        print(f"R2 {bin(R1)[2:].zfill(22)}")
    if allP or (((R4&R4TAP3)!=0) == maj):
        print(f"Нужно сдвинуть R3: {bin(R3)[2:].zfill(23)}")
        R3 = clockone(R3, R3MASK, R3TAPS, loaded << 18)
        print(f"R3 {bin(R1)[2:].zfill(23)}")
    print(f"Нужно сдвинуть R4: {bin(R4)[2:].zfill(17)}")
    R4 = clockone(R4, R4MASK, R4TAPS, loaded << 10)
    print(f"R4 {bin(R4)[2:].zfill(17)}")

delaybit = 0

def getbit():
    global delaybit
    topbits = (((R1 >> 18) ^ (R2 >> 21) ^ (R3 >> 22)) & 0x01)
    print("Выходной бит системы: ", delaybit)
    nowbit = delaybit
    print("Рассчет следующего: ")
    print(R1 >> 18, R2 >> 21, R3 >> 22)
    print((((R1 >> 18) ^ (R2 >> 21) ^ (R3 >> 22)) & 0x01))
    print(majority(R1 & 0x8000, (~R1) & 0x4000, R1 & 0x1000), majority((~R2) & 0x10000, R2 & 0x2000, R2 & 0x200), majority(R3 & 0x40000, R3 & 0x10000, (~R3) & 0x2000))

    delaybit = (
            topbits
            ^ majority(R1 & 0x8000, (~R1) & 0x4000, R1 & 0x1000)
            ^ majority((~R2) & 0x10000, R2 & 0x2000, R2 & 0x200)
            ^ majority(R3 & 0x40000, R3 & 0x10000, (~R3) & 0x2000)
    )
    print(delaybit)
    return nowbit

def keysetup(key, frame):
    global R1, R2, R3, R4
    R1, R2, R3, R4 = 0, 0, 0, 0
    print("Загрузка ключа, 64 такта: ")
    print("Изначально")
    print(f"R1 {bin(R1)[2:].zfill(19)}")
    print(f"R2 {bin(R2)[2:].zfill(22)}")
    print(f"R3 {bin(R3)[2:].zfill(23)}")
    print(f"R4 {bin(R4)[2:].zfill(17)}")
    for i in range(64):
        print(f"Такт {i}")
        clock(1, 0)
        keybit = (key[i // 8] >> (i & 7)) & 1
        R1 ^= keybit
        R2 ^= keybit
        R3 ^= keybit
        R4 ^= keybit
        print("Бит ключа", keybit)
        print("После загрузки бита ключа: ")
        print(f"R1 {bin(R1)[2:].zfill(19)}")
        print(f"R2 {bin(R2)[2:].zfill(22)}")
        print(f"R3 {bin(R3)[2:].zfill(23)}")
        print(f"R4 {bin(R4)[2:].zfill(17)}")
    print("Загрузка кадра, 22 такта: ")
    print("Изначально")
    print(f"R1 {bin(R1)[2:].zfill(19)}")
    print(f"R2 {bin(R2)[2:].zfill(22)}")
    print(f"R3 {bin(R3)[2:].zfill(23)}")
    print(f"R4 {bin(R4)[2:].zfill(17)}")
    for i in range(22):
        clock(1, i == 21)
        print(f"Такт {i}")
        framebit = (frame >> i) & 1
        R1 ^= framebit
        R2 ^= framebit
        R3 ^= framebit
        R4 ^= framebit
        print("Бит кадра", framebit)
        print("После загрузки бита кадра: ")
        print(f"R1 {bin(R1)[2:].zfill(19)}")
        print(f"R2 {bin(R2)[2:].zfill(22)}")
        print(f"R3 {bin(R3)[2:].zfill(23)}")
        print(f"R4 {bin(R4)[2:].zfill(17)}")

    R4 |= R4TAP1 | R4TAP2 | R4TAP3
    print("Такт, биты 3, 7, 10 4-го регистра нужно заполнить 1")
    print("После: ")
    print(f"R4 {bin(R4)[2:].zfill(17)}")
    print("99 тактов без генерации последовательности: ")
    print("Изначально")
    print(f"R1 {bin(R1)[2:].zfill(19)}")
    print(f"R2 {bin(R2)[2:].zfill(22)}")
    print(f"R3 {bin(R3)[2:].zfill(23)}")
    print(f"R4 {bin(R4)[2:].zfill(17)}")
    for i in range(99):
        print(f"Такт {i}")
        clock(0, 0)
        print("После сдвига: ")
        print(f"R1 {bin(R1)[2:].zfill(19)}")
        print(f"R2 {bin(R2)[2:].zfill(22)}")
        print(f"R3 {bin(R3)[2:].zfill(23)}")
        print(f"R4 {bin(R4)[2:].zfill(17)}")


def get_gamma():
    gamma = ""
    print("Изначально")
    print(f"R1 {bin(R1)[2:].zfill(19)}")
    print(f"R2 {bin(R2)[2:].zfill(22)}")
    print(f"R3 {bin(R3)[2:].zfill(23)}")
    print(f"R4 {bin(R4)[2:].zfill(17)}")
    for i in range(114):
        print(f"Такт {i}")
        clock(0, 0)
        gamma += str(getbit())
        print(f"Гамма: {gamma}")

    return gamma


def blocks_114(text: str, key: list, frame, do: str):
    output = ""
    if do == "encrypt":
        text = bin(int(text, 16))[2:]
        text = text.zfill(len(text) + (114 - len(text) % 114))

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
    print("Выбран шифр a5/2.")
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



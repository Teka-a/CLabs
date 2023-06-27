import format as f

#  000102030405060708090a0b0c0d0e0f
def set_params():
    while True:
        key = input("Введите ключ в 16-ом формате, длиной 32: ")
        key = key.lower()
        if f.is_hex_alphabet(key):
            if len(key) == 32:
                break
            else:
                print("Ключ должен быть длины 32!")
        else:
            print("Ключ содержит недопустимые символы!")
    return key


Rcon = [["01", "00", "00", "00"], ["02", "00", "00", "00"],
        ["04", "00", "00", "00"], ["08", "00", "00", "00"],
        ["10", "00", "00", "00"], ["20", "00", "00", "00"],
        ["40", "00", "00", "00"], ["80", "00", "00", "00"],
        ["1b", "00", "00", "00"], ["36", "00", "00", "00"]]


rijndaelMatrix = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
reversedRijndaelMatrix = [[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]]

sBox = [["63", "7c", "77", "7b", "f2", "6b", "6f", "c5", "30", "01", "67", "2b", "fe", "d7", "ab", "76"],
        ["ca", "82", "c9", "7d", "fa", "59", "47", "f0", "ad", "d4", "a2", "af", "9c", "a4", "72", "c0"],
        ["b7", "fd", "93", "26", "36", "3f", "f7", "cc", "34", "a5", "e5", "f1", "71", "d8", "31", "15"],
        ["04", "c7", "23", "c3", "18", "96", "05", "9a", "07", "12", "80", "e2", "eb", "27", "b2", "75"],
        ["09", "83", "2c", "1a", "1b", "6e", "5a", "a0", "52", "3b", "d6", "b3", "29", "e3", "2f", "84"],
        ["53", "d1", "00", "ed", "20", "fc", "b1", "5b", "6a", "cb", "be", "39", "4a", "4c", "58", "cf"],
        ["d0", "ef", "aa", "fb", "43", "4d", "33", "85", "45", "f9", "02", "7f", "50", "3c", "9f", "a8"],
        ["51", "a3", "40", "8f", "92", "9d", "38", "f5", "bc", "b6", "da", "21", "10", "ff", "f3", "d2"],
        ["cd", "0c", "13", "ec", "5f", "97", "44", "17", "c4", "a7", "7e", "3d", "64", "5d", "19", "73"],
        ["60", "81", "4f", "dc", "22", "2a", "90", "88", "46", "ee", "b8", "14", "de", "5e", "0b", "db"],
        ["e0", "32", "3a", "0a", "49", "06", "24", "5c", "c2", "d3", "ac", "62", "91", "95", "e4", "79"],
        ["e7", "c8", "37", "6d", "8d", "d5", "4e", "a9", "6c", "56", "f4", "ea", "65", "7a", "ae", "08"],
        ["ba", "78", "25", "2e", "1c", "a6", "b4", "c6", "e8", "dd", "74", "1f", "4b", "bd", "8b", "8a"],
        ["70", "3e", "b5", "66", "48", "03", "f6", "0e", "61", "35", "57", "b9", "86", "c1", "1d", "9e"],
        ["e1", "f8", "98", "11", "69", "d9", "8e", "94", "9b", "1e", "87", "e9", "ce", "55", "28", "df"],
        ["8c", "a1", "89", "0d", "bf", "e6", "42", "68", "41", "99", "2d", "0f", "b0", "54", "bb", "16"]]

inverseSBox = [["52", "09", "6a", "d5", "30", "36", "a5", "38", "bf", "40", "a3", "9e", "81", "f3", "d7", "fb"],
               ["7c", "e3", "39", "82", "9b", "2f", "ff", "87", "34", "8e", "43", "44", "c4", "de", "e9", "cb"],
               ["54", "7b", "94", "32", "a6", "c2", "23", "3d", "ee", "4c", "95", "0b", "42", "fa", "c3", "4e"],
               ["08", "2e", "a1", "66", "28", "d9", "24", "b2", "76", "5b", "a2", "49", "6d", "8b", "d1", "25"],
               ["72", "f8", "f6", "64", "86", "68", "98", "16", "d4", "a4", "5c", "cc", "5d", "65", "b6", "92"],
               ["6c", "70", "48", "50", "fd", "ed", "b9", "da", "5e", "15", "46", "57", "a7", "8d", "9d", "84"],
               ["90", "d8", "ab", "00", "8c", "bc", "d3", "0a", "f7", "e4", "58", "05", "b8", "b3", "45", "06"],
               ["d0", "2c", "1e", "8f", "ca", "3f", "0f", "02", "c1", "af", "bd", "03", "01", "13", "8a", "6b"],
               ["3a", "91", "11", "41", "4f", "67", "dc", "ea", "97", "f2", "cf", "ce", "f0", "b4", "e6", "73"],
               ["96", "ac", "74", "22", "e7", "ad", "35", "85", "e2", "f9", "37", "e8", "1c", "75", "df", "6e"],
               ["47", "f1", "1a", "71", "1d", "29", "c5", "89", "6f", "b7", "62", "0e", "aa", "18", "be", "1b"],
               ["fc", "56", "3e", "4b", "c6", "d2", "79", "20", "9a", "db", "c0", "fe", "78", "cd", "5a", "f4"],
               ["1f", "dd", "a8", "33", "88", "07", "c7", "31", "b1", "12", "10", "59", "27", "80", "ec", "5f"],
               ["60", "51", "7f", "a9", "19", "b5", "4a", "0d", "2d", "e5", "7a", "9f", "93", "c9", "9c", "ef"],
               ["a0", "e0", "3b", "4d", "ae", "2a", "f5", "b0", "c8", "eb", "bb", "3c", "83", "53", "99", "61"],
               ["17", "2b", "04", "7e", "ba", "77", "d6", "26", "e1", "69", "14", "63", "55", "21", "0c", "7d"]]



def round_XOR(col1, col2):
    result = []
    for i in range(len(col1)):
        result.append((hex(int(col1[i], 16)^int(col2[i], 16)))[2:].zfill(2))
    return result

# Функция для изменения раудового ключа в конце каждой итерации
def roundKeyIteration(key, iter, encryption):
    newKey = []
    if encryption:
        # берем последнюю колонку ключа
        column = key[12:]
        # переставляем первый HEX элемент на последнее место
        column = column[1:] + column[:1]
        # производим операцию subBytes
        column = subBytes(column, encryption)
        # производим XOR между полученной колонкой, первой колонкой ключа и колонкой Rcon, зависящей от номера раунда, получаем первую колонку нового ключа
        newKey += round_XOR(round_XOR(column, key[:4]), Rcon[iter])
        # производим XOR между соответствующей (1-3) полученной колонкой нового ключа и соответствующей + 1 (2-4) колонкой переданного ключа
        for i in range(3):
            newKey += round_XOR(newKey[i * 4: i * 4 + 4], key[(i+1) * 4: (i+1) * 4 + 4])
    else:
        i = 3
        tmp = []
        # производим XOR между соответствующей (3-1) колонкой ключа и колонкой -1 (2-0)
        while i >= 1:
            tmp += round_XOR(key[i * 4: i * 4 + 4], key[(i-1) * 4: (i-1) * 4 + 4])
            i -= 1
        # производим XOR между первой колонкой ключа и колонкой Rcon, зависящей от номера раунда,
        column = round_XOR(key[:4], Rcon[iter])
        # берем первую колонку tmp
        some_p = tmp[:4]
        # переставляем первый HEX элемент на последнее место
        some_p = some_p[1:] + some_p[:1]
        # производим операцию subBytes
        some_p = subBytes(some_p, encryption=True)
        # производим XOR между column и some_p
        newKey = round_XOR(some_p, column)
        # меняем местами: 3 и 4 колонки, потом 2, потом 1
        newKey += tmp[8:] + tmp[4:8] + tmp[:4]
    return newKey

# Функция для XOR-сложения полученного раудового ключа и блока в обработке
def addRKey(text, rKey):
    result = []
    for i in range(len(text)):
        result.append((hex(int(text[i], 16)^int(rKey[i], 16)))[2:].zfill(2))
    return result

# Функция, выполняющая операции SubBytes и InvSubBytes, замена производится по Sbox (S-блок AES)
def subBytes(text, encryption):
    result = []
    for i in text:
        if encryption:
            result.append(sBox[int(i[0], 16)][int(i[1], 16)])
        else:
            result.append(inverseSBox[int(i[0], 16)][int(i[1], 16)])
    return result

# Функция для конвертации одномерного массива в двумерную матрицу
def arrayToMatrix(arr):
    result = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(len(arr)):
        result[i%4][i//4] = arr[i]
    return result

# Функция для конвертации двумерной матрицы в одномерный массив
def matrixToList(matrix):
    result = []
    for i in range(4):
        for j in range(4):
            result.append(matrix[j][i])
    return result

# Функция, выполняющая операции ShiftRows и InvShiftRows
def shiftRows(text, encryption):
    text = arrayToMatrix(text)
    for i in range(1,4):
        if encryption:
            text[i] = text[i][i:] + text[i][:i]
        else:
            text[i] = text[i][-i:] + text[i][:-i]
    text = matrixToList(text)
    return text

# Функция, выполняющая умножение числа из колонки на 2
def doubleNum(num: str):
    if int(num, 2) >= 128:
        num = num[1:] + '0'
        num = bin(int(num, 2) ^ int("1b", 16))[2:].zfill(8)
    else:
        num = num[1:] + '0'
    return num

# Функция, выполняющая операцию MixColumns и InvMixColumns
def mixColumns(column, row, encryption):
    result = 0
    if encryption:
        for i in range(4):
            bin_num = bin(int(column[i], 16))[2:].zfill(8)
            if rijndaelMatrix[row][i] == 2:
                bin_num = doubleNum(bin_num)
            elif rijndaelMatrix[row][i] == 3:
                init_bin_num = int(bin_num, 2)
                bin_num = bin(int(doubleNum(bin_num), 2) ^ init_bin_num)[2:].zfill(8)
            if i == 0:
                result = int(bin_num, 2)
            else:
                result ^= int(bin_num, 2)
    else:
        for i in range(4):
            bin_num = bin(int(column[i], 16))[2:].zfill(8)
            init_bin_num = int(bin_num, 2)
            if reversedRijndaelMatrix[row][i] == 9:
                # 09=(((x·2)·2)·2)+x
                bin_num = int(doubleNum(doubleNum(doubleNum(bin_num))), 2) ^ init_bin_num
            elif reversedRijndaelMatrix[row][i] == 11:
                # 11=((((x·2)s·2)+x)·2)+x
                bin_num = int(doubleNum(bin(int(doubleNum(doubleNum(bin_num)), 2) ^ init_bin_num)[2:].zfill(8)), 2) ^ init_bin_num
            elif reversedRijndaelMatrix[row][i] == 13:
                # 13=((((x·2)+x)·2)·2)+x
                bin_num = int(doubleNum(doubleNum(bin(int(doubleNum(bin_num), 2) ^ init_bin_num)[2:].zfill(8))), 2) ^ init_bin_num
            elif reversedRijndaelMatrix[row][i] == 14:
                bin_num = int(doubleNum(bin(int(doubleNum(bin(int(doubleNum(bin_num), 2) ^ init_bin_num)[2:].zfill(8)), 2) ^ init_bin_num)[2:].zfill(8)), 2)
                # print("check", bin_num)
            if i == 0:
                result = bin_num
            else:
                result ^= bin_num
    return hex(result)[2:].zfill(2)

# Функция шифрования
def encrypt(text: str, key: str):
    text = f.bigramm_list(text)
    key = f.bigramm_list(key)
    res = []
    init_key = key
    for i in range(len(text) // 16):
        encryption = True
        tmp = addRKey(text[i * 16 : i * 16 + 16], key)
        for j in range(9):
            result = []
            tmp = subBytes(tmp, encryption)
            tmp = shiftRows(tmp, encryption)
            for l in range(4):
                column = tmp[l * 4: l * 4 + 4]
                for k in range(4):
                    result.append(mixColumns(column, k, encryption))
            key = roundKeyIteration(key, j, encryption)
            tmp = addRKey(result, key)
        tmp = subBytes(tmp, encryption)
        tmp = shiftRows(tmp, encryption)
        key = roundKeyIteration(key, 9, encryption)
        res.extend(addRKey(tmp, key))
        key = init_key
    return "".join(res)

def decrypt(text: str, key: str):
    text = f.bigramm_list(text)
    key = f.bigramm_list(key)
    res = []
    i = 0
    while i <= 9:
        key = roundKeyIteration(key, i, True)
        i += 1
    init_key = key
    encryption = False
    for l in range(len(text) // 16):
        tmp = addRKey(text[l * 16 : l * 16 + 16], key)
        tmp = shiftRows(tmp, encryption)
        tmp = subBytes(tmp, encryption)
        key = roundKeyIteration(key, 9, encryption)
        i = 8
        while i >= 0:
            result = []
            tmp = addRKey(tmp, key)
            key = roundKeyIteration(key, i, encryption)
            for j in range(4):
                column = tmp[j * 4: j * 4 + 4]
                for k in range(4):
                    result.append(mixColumns(column, k, encryption))
            tmp = result
            tmp = shiftRows(tmp, encryption)
            tmp = subBytes(tmp, encryption)
            i -= 1
        res.extend(addRKey(tmp, key))
        key = init_key
    return "".join(res)


def blocks_128(text: str, key: str, do: str):
    output = ""
    if do == "encrypt":
        text = f.procedure2(text, 128)
    for start in range(0, len(text), 32):
        if do == "encrypt":
            output += encrypt(text[start:start + 32], key)
        elif do == "decrypt":
            output += decrypt(text[start:start + 32], key)
    if do == "decrypt":
        output = f.unprocedure2(output)
    return output


def main():
    print("Выбран шифр AES.")
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Зашифровать (из to-encrypt.txt в to-decrypt.txt). "
              "\n\t2. Расшифровать (из to-decrypt.txt в result.txt).")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            key = set_params()
            text = f.read_from_file("to-encrypt.txt")
            #  Подготовка строки для шифрования
            prepared = f.replace_empty_symbols(text, 1)
            if not f.is_hex_alphabet(prepared):
                #  Преобразовать в 16 формат
                prepared = f.prepare_in(text, 1, 16)
            encrypted = f.prepare_out(blocks_128(prepared, key, "encrypt"), 1)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            key = set_params()
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = blocks_128(prepared, key, "decrypt")
            print("Нужно ли преобразовать в буквы русского алфавита?"
                  "\n\t0. Нет. "
                  "\n\t1. Да. ")
            need = int(input("Выберите опцию: "))

            if need == 1:
                #  Преобразовать из 16 формата в буквы русского алфавита
                decrypted = f.prepare_out(decrypted, 2, 16)

            f.write_to_file("result.txt", decrypted, 2)

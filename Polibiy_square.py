import format as f


#  Функция получения индексов буквы
def get_nums(char: str) -> str:
    for i in f.arr_ru_6:
        stri = f.arr_ru_6.index(i)
        if char in i:
            col = i.index(char)
            return(f"{stri + 1}{col + 1}")
        #  Если в данной строке нет буквы, необходимо проверить следующую
        continue
    return ""


#  Функция получения буквы по указанным индексам
def get_letter(row: int, col: int) -> str:
    letter = "Ошибка"
    try:
        letter = f.arr_ru_6[row - 1][col - 1]
    except IndexError:
        print("Произошла ошибка!")
    return letter


#  Функция зашифрования
def encrypt(text: str) -> str:
    encrypted = ""
    for i in text:
        #  Преобразуем букву в 2 числовых значения: строка и столбец
        #  Определяются местонахождением буквы в алфавите 6*6
        c = get_nums(i)
        encrypted += c
    return f.prepare_out(encrypted, 1)


#  Функция расшифрования
def decrypt(text: str) -> str:
    decrypted = ""
    counter = 0
    pairs = len(text) - 2
    while counter <= pairs:
        #  Берем по 2 цифры, первая - строка, вторая - столбец
        row = int(text[counter])
        column = int(text[counter + 1])

        p = get_letter(row, column)

        decrypted += p
        counter += 2
    return f.prepare_out(decrypted, 2)


def main():
    print("Выбран шифр квадрат Полибия.")
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
            prepared = f.prepare_in(text, 1)
            encrypted = encrypt(prepared)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:

            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = decrypt(prepared)

            f.write_to_file("result.txt", decrypted, 2)

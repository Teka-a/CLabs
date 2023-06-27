import format as f
import numpy.linalg as linalg


def set_params():
    while True:
        print("Заполните значения матрицы 3*3: ")
        matr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                while True:
                    try:
                        #  Введенное значение должно является числом
                        matr[i][j] = int(input(f"Ввведите значение [{i}][{j}]: "))
                        break
                    except ValueError:
                        print("Введите число!")
        if linalg.det(matr) == 0:
            print("Определитель матрицы равен 0, такая матрица не подходит для шифра.")
        else:
            break
    return matr


#  Функция зашифрования
def encrypt(text: str, key: list) -> str:
    encrypted = ""
    positions = []
    for char in text:
        positions.append(f.arr_ru.index(char)+1)
    for i in range(0, len(positions), len(key[0])):
        mult1, mult2, mult3 = 0, 0, 0
        for k in range(3):
            #  Перемножение матриц: ключа и 3 букв
            mult1 += positions[i+k] * key[0][k]
            mult2 += positions[i + k] * key[1][k]
            mult3 += positions[i + k] * key[2][k]
        mas_mult = [mult1, mult2, mult3]
        for mult in range(3):
            m = str(mas_mult[mult])
            if len(m) < 3:
                while len(m) < 3:
                    m = "0" + m
            mas_mult[mult] = m
        encrypted += mas_mult[0] + mas_mult[1] + mas_mult[2]
    return f.prepare_out(encrypted, 1)


#  Функция расшифрования
def decrypt(text: str, key: list) -> str:
    decrypted = ""
    positions = []
    for i in range(0, len(text), 3):
        positions.append(int(text[i:i+3]))
    #  Для расшифрования используется обратная матрица
    key = linalg.inv(key)
    for i in range(0, len(positions), len(key[0])):
        mult1, mult2, mult3 = 0, 0, 0
        for k in range(3):
            #  Перемножение матриц: ключа и 3 букв
            mult1 += positions[i+k] * key[0][k]
            mult2 += positions[i + k] * key[1][k]
            mult3 += positions[i + k] * key[2][k]
        decrypted += f.arr_ru[int(mult1) - 1] + f.arr_ru[int(mult2) - 1] + f.arr_ru[int(mult3) - 1]
    return f.prepare_out(decrypted, 2)



def main():
    print("Выбран матричный шифр.")
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Зашифровать (из to-encrypt.txt в to-decrypt.txt). "
              "\n\t2. Расшифровать (из to-decrypt.txt в result.txt).")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            matr = set_params()
            text = f.read_from_file("to-encrypt.txt")
            #  Подготовка строки для шифрования
            prepared = f.prepare_in(text, 1)
            #  Количество букв должно быть кратно 3
            if len(prepared) % 3 != 0:
                prepared += "п" * (3 - (len(prepared) % 3))
            encrypted = encrypt(prepared, matr)

            f.write_to_file("to-decrypt.txt", encrypted, 1)

        elif do == 2:
            matr = set_params()
            text = f.read_from_file("to-decrypt.txt")
            #  Подготовка строки для расшифрования
            prepared = f.prepare_in(text, 2)
            decrypted = decrypt(prepared, matr)

            f.write_to_file("result.txt", decrypted, 2)


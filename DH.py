import format as f


def set_params():
    while True:
        try:
            n = int(input("Введите простое число n: "))
            if f.is_prime(n):
                break
            else:
                print("Ожидается простое число!")
        except ValueError:
            print("Введите число!")
    while True:
        try:
            a = int(input(f"Введите число а (меньше {n - 1}): "))
            if a < n:
                break
            else:
                print("Необходимо выбрать а меньше n!")
        except ValueError:
            print("Введите число!")
    while True:
        try:
            Ka = int(input(f"Введите число Ka от 2 до {n}: "))
            if Ka >= 2 and Ka < n:
                break
            else:
                print("Число вне указанного диапазона!")
        except ValueError:
            print("Введите число!")
    while True:
        try:
            Kb = int(input(f"Введите число Kb от 2 до {n}: "))
            if Kb >= 2 and Kb < n:
                break
            else:
                print("Число вне указанного диапазона!")
        except ValueError:
            print("Введите число!")
    Ya = pow(a, Ka, n)
    Yb = pow(a, Kb, n)
    return [Ka, Kb, n, Ya, Yb]


def main():
    print("Выбран обмен ключами по Диффи-Хеллману.")
    while True:
        print("Что вы хотите сделать? \n\t0. Вернуться в главное меню. "
              "\n\t1. Вычислить общий секретный ключ. ")

        do = int(input("Выберите опцию: "))

        if do == 0:
            break

        elif do == 1:
            [Ka, Kb, n, Ya, Yb] = set_params()
            secret_A = pow(Yb, Ka, n)
            secret_B = pow(Ya, Kb, n)
            print("secret_A: ", secret_A)
            print("secret_B: ", secret_B)
            if secret_A == 1:
                print("Общий секрет равен 1, попробуйте изменить a.")
                break
            if secret_A == secret_B:
                print("Общий секрет =", secret_A)
            else:
                print("Произошла ошибка!")


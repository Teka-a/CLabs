import Atbash, Ceasar, Polibiy_square, Thritemiy, Belazo, Vigener, s_block, Matrix, Playfer, Vertical,\
    Cardano, Feistel, One_time_Pad, gost_34_13_2015, a_5_1, a_5_2, Magma, gost_28147_89, AES, Kuznechik, RSA, \
    Elgamal, ECC, RSA_sign, Elgamal_sign, gost_34_10_94, gost_34_10_2012, DH


def print_options():
    print("0. Exit.")
    print("Блок А: Шифры однозначной замены")
    print("    1. Шифр Атбаш")
    print("    2. Шифр Цезаря")
    print("    3. Квадрат Полибия")
    print("Блок B: Шифры многозначной замены")
    print("    4. Шифр Тритемия")
    print("    5. Шифр Белазо")
    print("    6. Шифр Виженера")
    print("    7. S-блок замены ГОСТ Р 34.12-2015")
    print("Блок C: Шифры блочной замены")
    print("    8. Матричный шифр")
    print("    9. Шифр Плэйфера - шифр биграммной замены")
    print("Блок D: Шифры перестановки")
    print("    10. Вертикальная перестановка")
    print("    11. Решетка Кардано")
    print("    12. Перестановка в комбинационных шифрах - сеть Фейстеля")
    print("Блок E: Шифры гаммирования")
    print("    13. Одноразовый блокнот К. Шеннона")
    print("    14. ГОСТ Р 34.13-2015")
    print("Блок F: Поточные ширфы")
    print("    15. А5/1")
    print("    16. А5/2")
    print("Блок G: Комбинационные ширфы")
    print("    17. МАГМА")
    print("    18. ГОСТ 28147-89")
    print("    19. AES")
    print("    20. КУЗНЕЧИК")
    print("Блок H: Асимметричные ширфы")
    print("    21. RSA")
    print("    22. Elgamal")
    print("    23. ECC с использованием абсциссы точки")
    print("Блок I: Алгоритмы цифровых подписей")
    print("    24. RSA")
    print("    25. Elgamal")
    print("Блок J: Стандарты цифровых подписей")
    print("    26. ГОСТ Р 34.10-94")
    print("    27. ГОСТ Р 34.10-2012")
    print("Блок K: Обмен ключами")
    print("    28. Обмен ключами по Диффи-Хеллману")


print_options()
ciphers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]

while True:
    cipher = int(input("Введите номер выбранного шифра: "))
    if cipher not in ciphers:
        print("Шифр под таким номером не предусмотрен.")
    if cipher == 0:
        raise SystemExit
    elif cipher == 1:
        Atbash.main()
    elif cipher == 2:
        Ceasar.main()
    elif cipher == 3:
        Polibiy_square.main()
    elif cipher == 4:
        Thritemiy.main()
    elif cipher == 5:
        Belazo.main()
    elif cipher == 6:
        Vigener.main()
    elif cipher == 7:
        s_block.main()
    elif cipher == 8:
        Matrix.main()
    elif cipher == 9:
        Playfer.main()
    elif cipher == 10:
        Vertical.main()
    elif cipher == 11:
        Cardano.main()
    elif cipher == 12:
        Feistel.main()
    elif cipher == 13:
        One_time_Pad.main()
    elif cipher == 14:
        gost_34_13_2015.main()
    elif cipher == 15:
        a_5_1.main()
    elif cipher == 16:
        a_5_2.main()
    elif cipher == 17:
        Magma.main()
    elif cipher == 18:
        gost_28147_89.main()
    elif cipher == 19:
        AES.main()
    elif cipher == 20:
        Kuznechik.main()
    elif cipher == 21:
        RSA.main()
    elif cipher == 22:
        Elgamal.main()
    elif cipher == 23:
        ECC.main()
    elif cipher == 24:
        RSA_sign.main()
    elif cipher == 25:
        Elgamal_sign.main()
    elif cipher == 26:
        gost_34_10_94.main()
    elif cipher == 27:
        gost_34_10_2012.main()
    elif cipher == 28:
        DH.main()
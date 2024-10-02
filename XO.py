playing_field = [['-', '-', '-'],
                ['-', '-', '-'],
                ['-', '-', '-']]

def field() -> None:
    """"Функция выводит игровое поле в консоль"""
    print(" ",0,1,2)
    for i in range(len(playing_field)):
        for j in range(len(playing_field[i])):
            if j == 0:
                print(i, end=" ")
            print(playing_field[i][j], end=" ")
        print()

def result(sign: str, player: int, counter: int) -> bool:
    """Функция выводит результаты игры на основе расположения знаков на поле:
    победа первого или второго игрока
    и ничью
    """
    if any([
        all(playing_field[i][j] == sign for i in range(3)) for j in range(3) #проверяет строки
    ]) or any([
        all(playing_field[j][i] == sign for i in range(3)) for j in range(3) #проверяет столбцы
    ]) or (playing_field[0][0] == playing_field[1][1] == playing_field[2][2] == sign) or \
    (playing_field[0][2] == playing_field[1][1] == playing_field[2][0] == sign): #проверяет диагонали
        print(f"Player {player} has won") #вывод победы
        return True
    elif counter == 9:
        print("Tie") #вывод ничьей
        return True

def check_moves() -> tuple[bool, int, int] | tuple[bool, int, None]:
    """Функция просит input для индекса строки и колонны.
    Проверяет, входят ли значения в назначенный диапазон.
    Далее сверяется с клеткой, которая находится в данных индексах
    и не занята ли она X/O"""
    row = int(input("Enter the number of the row: ")) #запрос на ввод индекса строки
    if row in range(3): # проверка диапазона строки
        col = int(input("Enter the number of the column: ")) #запрос на ввод индекса столбца
        if col in range(3): # проверка диапазона столбца
            if playing_field[row][col] not in ("X","O"): #проверка на наличие X/O в данной клетке
                return True, row, col
            else:
                print("This space is already spotted") #вывод при условии, что данная точка занята
                return False, row, col
        else:
            print("The column number have to be in range from 0 to 2") # вывод, если индекс столбца вне диапазона
            return False, row, col
    else:
        print("The row number have to be in range from 0 to 2") # вывод, если индекс строки вне диапазона
        return False, row, None

def move() -> None:
    """Функция осуществляет ход после проверки check_move"""
    counter = 0
    while True:
        player = 1 if counter % 2 == 0 else 2 #выражение, вычисляющее номер игрока
        sign = "X" if player == 1 else "O" #привязка знака к игроку
        reply, row, col = check_moves()
        if reply:
            playing_field[row][col] = sign #вставка знака при условии, что клетка не занята
            counter += 1 #добавление единицы к счетчику для чередования игроков
            if result(sign, player, counter): #условие, останавливающее функцию, если при result -> True
                field()
                break
            else:
                field() #в противном случае, продолжает игру
field()
move()
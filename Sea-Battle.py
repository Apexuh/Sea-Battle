from random import randint


class Ship:
    def __init__(self, length,  tp=1, x=None, y=None):
        self._x = x #start coord
        self._y = y #start coord
        self._length = length # length of ship (1,2,3 or 4)
        self._tp = tp    #ship orientation(1 - horizontal, 2- vertical)
        self._is_move = True #True if ship can move
        self._cells = [1] * self._length #1 if part of ship is unbroken, 2 -this part is broken

    def set_start_coords(self, x, y):  # - установка начальных координат (запись значений в локальные атрибуты _x, _y);
        self._x = x
        self._y = y

    def get_start_coords(self): # - получение начальных координат корабля в виде кортежа x, y;
        return self._x, self._y

    def move(self, go):  #- перемещение корабля в направлении его ориентации на go клеток (go = 1 - движение в одну сторону на клетку; go = -1 - движение в другую сторону на одну клетку); движение возможно только если флаг _is_move = True;
        if self._is_move:
            if self._tp == 1:
                self._x += go
            else:
                self._y += go

    def is_collide(self, ship): # - проверка на столкновение с другим кораблем ship (столкновением считается, если другой корабль или пересекается с текущим или просто соприкасается, в том числе и по диагонали); метод возвращает True, если столкновение есть и False - в противном случае;
        if self._x is not None and self._y is not None and ship._x is not None and ship._y is not None:
            return len(set(self.is_collide_location()) & set(ship.ship_position())) != 0
        return False

    def is_collide_location(self):
        '''определение "ореола" корабля для определения столкновения с другим кораблем'''
        s01 = []
        for i in self.ship_position():
            for x in range(i[0] - 1, i[0] + 2):
                for y in range(i[1] - 1, i[1] + 2):
                    if (x, y) not in s01 and 0 <= x and 0 <= y:
                        s01.append((x, y))
        return s01

    def is_out_pole(self, size):
        '''проверка на выход корабля за пределы игрового поля (size - размер игрового поля, обычно, size = 10);
        возвращается булево значение True, если корабль вышел из игрового поля и False - в противном случае;'''
        hor, vert = 0, 0    #дополнительные параметры (в зависимости от направления судна).
        if self._tp == 1: # если горизонтально расположено судно, то х максимальная меняется
            hor = self._length
        else:
            vert = self._length
        if self._x < 0 or self._y < 0 or self._x + hor >= size or self._y + vert >= size:
            return True
        return False

    def ship_position(self):
        '''возвращает список координат расположения корабля'''
        start_x, start_y = self._x, self._y
        if self._tp == 1:
            end_x, end_y = start_x + self._length, start_y + 1
        else:
            end_x, end_y = start_x + 1, start_y + self._length
        s = [(i, j) for i in range(start_x, end_x) for j in range(start_y, end_y)]
        return s

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value


class GamePole:
    def __init__(self, size=10, name=None):
        self._size = size
        self._ships = []
        self._name = name
        self._shots = [[0] * self._size for _ in range(self._size)]



    def init(self):
        type_of_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self._count_of_ships = len(type_of_ships)
        self._ships = [Ship(i, tp=randint(1, 2)) for i in type_of_ships]
        self.installation_ships()


    def installation_ships(self):
        '''установка кораблей на поле(рандомно), данные о кораблях берутся из списка self._ships'''
        counter = 0
        i = 0
        while i < 10:
            counter += 1
            if counter > 100:
                self.installation_ships()
            ship = self._ships[i]
            x = randint(0, self._size)
            y = randint(0, self._size)
            ship.set_start_coords(x, y)
            if ship.is_out_pole(self._size): # проверка выхода за поле
                continue

            s = []
            for boat in self._ships:   # проход по списку из судов, если есть пересечение с каким-то судном, то запуск генерации заново
                if ship == boat:
                    continue
                else:
                    s.append(ship.is_collide(boat))
            if any(s):
                continue
            i += 1



    def get_ships(self):
        '''возвращает коллекцию _ships;'''
        return self._ships

    def move_ships(self):
        '''- перемещает каждый корабль из коллекции _ships на одну клетку (случайным образом вперед или назад) в
        направлении ориентации корабля; если перемещение в выбранную сторону невозможно (другой корабль или пределы игрового поля),
         то попытается переместиться в противоположную сторону, иначе (если перемещения невозможны), остается на месте;'''
        for ship in self._ships:
            temp_coords = ship.get_start_coords()
            if ship._is_move:
                ship.move(1)
                any_list_collide = [ship.is_collide(boat) for boat in self._ships if ship != boat]
                if any(any_list_collide) or ship.is_out_pole(self._size):
                    ship.move(-2)
                    any_list_collide = [ship.is_collide(boat) for boat in self._ships if ship != boat]
                    if any(any_list_collide) or ship.is_out_pole(self._size):
                        ship.set_start_coords(*temp_coords)
                        ship._is_move = False



    def show(self):
        '''- отображение игрового поля в консоли (корабли отображаются значениями из коллекции _cells каждого корабля,
         вода - значением 0);'''
        s = '\n'.join(tuple(map(lambda x: ' '.join(tuple(map(str, x))), self.get_pole())))
        print(s)
        print('=' * 19)



    def get_pole(self):
        '''- получение текущего игрового поля в виде двумерного (вложенного) кортежа размерами size x size элементов.'''
        self._pole = [[0] * self._size for _ in range(self._size)]
        for ship in self._ships:
            for i, coords in enumerate(ship.ship_position()):
                x, y = coords
                value = ship._cells[i]
                self._pole[y][x] = value
        self._pole = tuple(map(lambda x: tuple(x), self._pole))
        return self._pole

    def make_shot(self, x, y):
        '''стрельба по кораблю. Если введены неактуальные данные, то ошибка. Если корабль уничтожен, то удаляется из списка кораблей'''
        for boat in self._ships:
            if (x, y) in boat.ship_position():
                boat._cells[boat.ship_position().index((x, y))] = 2
                ship_is_broken = all(list(map(lambda x: x == 2, boat._cells)))
                self._shots[x][y] = 'X'
                if boat._is_move:
                    boat._is_move = False
                if ship_is_broken:
                    print(f"{self._name}'s ship with {boat._length} deck(s) was destroyed")
                    self._count_of_ships -= 1
                    for coords in boat.is_collide_location():
                        i, j = coords
                        self._shots[i][j] = '*'
                    for coords in boat.ship_position():
                        i, j = coords
                        self._shots[i][j] = 'X'
                else:

                    print(f'There was a hit on the {self._name} ship in coords: {(x + 1, y + 1)}')
                break

    def take_shot(self, x, y):
        raise ValueError


    def __len__(self):
        return self._count_of_ships

class Player(GamePole):
    def take_shot(self):
        x, y = randint(0, self._size - 1), randint(0, self._size - 1)
        self.make_shot(x, y)



class Enemy(GamePole):
    def take_shot(self):
        x = input(f'Please input vertical coord in interval (1, {self._size}):   ')
        y = input(f'Please input horizontal coord in interval (1, {self._size}):   ')
        print('=' * 19)
        try:
            x, y = int(x), int(y)
            if x <= 0 or y <= 0 or x > self._size or x > self._size:
                raise ValueError
        except:
            print('Error in coords, try again...')
            self.take_shot()
        self._shots[x - 1][y - 1] = '*'
        self.make_shot(x - 1, y - 1)

    def show(self):
        '''- отображение игрового поля в консоли (корабли отображаются значениями из коллекции _cells каждого корабля,
         вода - значением 0);'''
        s = '\n'.join(tuple(map(lambda x: ' '.join(tuple(map(str, x))), self._shots)))
        print(s)
        print('=' * 19)








# RUN
if __name__ == '__main__':
    print('Hello! This is a sea battle game. Differs from the original in that ships can move in it.\n'
        'If you get on a ship, it will go to the bottom and clear the place for other ships.\n'
        'if you get in a ship, it will no longer be able to sail away.\n'
         'Good luck!')
    SIZE_GAME_POLE = 10
    enemy = Enemy(SIZE_GAME_POLE, 'Enemy')
    player = Player(SIZE_GAME_POLE, input('Input your name please:   '))
    player.init()
    player.show()
    enemy.init()
    r = 0
    while len(player) > 0 or len(enemy) > 0:
        r += 1
        print(f'Round {r}!')
        enemy.take_shot()
        player.take_shot()
        print(f'You have {len(player)} ships afloat')
        print(f'Your enemy has {len(enemy)} ships afloat')
        print('=' * 19)
        player.move_ships()
        enemy.move_ships()
        print('Your shots')
        enemy.show()
    winner = player._name if len(player) > len(enemy) else enemy._name if len(enemy) > len(player) else None
    if not winner:
        print('Nobody wins!')
    else:
        print(f'The winner is: {winner}')



# ============================================================================================================




# MY TESTS
# s1 = Ship(3) #horizontal
# assert s1._cells == [1, 1, 1]
# s1.set_start_coords(9, 5)
# assert s1.ship_position() == [(9, 5), (10, 5), (11, 5)]
# assert s1.is_out_pole(10) == True

# s = Ship(4, 2) #vertical
# s.set_start_coords(3, 7)
# assert s.ship_position() == [(3, 7), (3, 8), (3, 9), (3, 10)]
# assert s.is_out_pole(10) == True
#
# s2 = Ship(4)
# s3 = Ship(4)
# s4 = Ship(4)
# assert s2._cells == [1, 1, 1, 1]
# s2.set_start_coords(3, 3)
# s3.set_start_coords(3, 4)
# s4.set_start_coords(3, 5)
#
# # print(s4.ship_position())
# print(s2.is_collide(s3))
# print(s2.is_collide(s4))


# s5 = Ship(3)
# s5.set_start_coords(1, 1)
# print(s5.ship_position())
# print(s5.is_collide_location())
#
# s6 = Ship(3,2)
# s6.set_start_coords(1, 1)
# print(s6.ship_position())
# print(sorted(s6.is_collide_location(),key=lambda x: x[0]))
''''''

# TESTS
# ship = Ship(2)
# ship = Ship(2, 1)
# ship = Ship(3, 2, 0, 0)
#
# assert ship._length == 3 and ship._tp == 2 and ship._x == 0 and ship._y == 0, "неверные значения атрибутов объекта класса Ship"
# assert ship._cells == [1, 1, 1], "неверный список _cells"
# assert ship._is_move, "неверное значение атрибута _is_move"
# #
# ship.set_start_coords(1, 2)
# assert ship._x == 1 and ship._y == 2, "неверно отработал метод set_start_coords()"
# assert ship.get_start_coords() == (1, 2), "неверно отработал метод get_start_coords()"
# #
# ship.move(1)
# s1 = Ship(4, 1, 0, 0)
# s2 = Ship(3, 2, 0, 0)
# s3 = Ship(3, 2, 0, 2)
# # print(s1.ship_position())
# # print(s1.is_collide_location())
# # print(s3.ship_position())
# # print(s3.is_collide_location())
# # print(s1.is_collide(s3))
#
# assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 0)"
# assert s1.is_collide(
#     s3) == False, "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 2)"
#
# s2 = Ship(3, 2, 1, 1)
# assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 1, 1)"
#
# s2 = Ship(3, 1, 8, 1)
# assert s2.is_out_pole(10), "неверно работает метод is_out_pole() для корабля Ship(3, 1, 8, 1)"
#
# s2 = Ship(3, 2, 1, 5)
# assert s2.is_out_pole(10) == False, "неверно работает метод is_out_pole(10) для корабля Ship(3, 2, 1, 5)"
#
# s2[0] = 2
# # print(s2[0])
# assert s2[0] == 2, "неверно работает обращение ship[indx]"
#
#
#
# p = GamePole(10)
# p.init()
# # print(*p._pole, sep='\n')
# #
# #
# # print(p.get_ships())
# # print(p.get_ships()[0].is_collide(s2))
#
# for nn in range(5):
#     for s in p._ships:
#         assert s.is_out_pole(10) == False, "корабли выходят за пределы игрового поля"
# #
#         for ship in p.get_ships():
#             if s != ship:
#                 assert s.is_collide(ship) == False, "корабли на игровом поле соприкасаются"
#     p.move_ships()
#     # print(*p._pole, sep='\n')
#
# # print('============================================')
# gp = p.get_pole()
# # print(gp)
# # print(p.show())
# assert type(gp) == tuple and type(gp[0]) == tuple, "метод get_pole должен возвращать двумерный кортеж"
# assert len(gp) == 10 and len(gp[0]) == 10, "неверные размеры игрового поля, которое вернул метод get_pole"
#
# pole_size_8 = GamePole(8)
# pole_size_8.init()


from sea_battle import *


def test_create_ships():
    ship = Ship(3, 2, 0, 0)

    assert ship._length == 3 and ship._tp == 2 and ship._x == 0 and ship._y == 0, "неверные значения атрибутов объекта класса Ship"
    assert ship._cells == [1, 1, 1], "неверный список _cells"
    assert ship._is_move, "неверное значение атрибута _is_move"
    #
    ship.set_start_coords(1, 2)
    assert ship._x == 1 and ship._y == 2, "неверно отработал метод set_start_coords()"
    assert ship.get_start_coords() == (1, 2), "неверно отработал метод get_start_coords()"


def test_ship_move():
    ship = Ship(3, 2, 0, 0)
    pos = ship.ship_position()
    ship.move(1)
    assert pos != ship.ship_position()


def test_create_horizontal_ship():
    s = Ship(3)  # horizontal
    assert s._cells == [1, 1, 1]
    s.set_start_coords(9, 5)
    assert s.ship_position() == [(9, 5), (10, 5), (11, 5)]
    assert s.is_out_pole(10) == True


def test_create_vertical_ship():
    s = Ship(4, 2)  # vertical
    s.set_start_coords(3, 7)
    assert s.ship_position() == [(3, 7), (3, 8), (3, 9), (3, 10)]
    assert s.is_out_pole(10) == True


def tests_ships_is_collide():
    s2 = Ship(4)
    s3 = Ship(4)
    s4 = Ship(4)
    assert s2._cells == [1, 1, 1, 1]
    s2.set_start_coords(3, 3)
    s3.set_start_coords(3, 4)
    s4.set_start_coords(3, 5)
    assert s2.is_collide(s3) == True
    assert s2.is_collide(s4) == False


def tests_ships_is_colide_2():
    s1 = Ship(4, 1, 0, 0)
    s2 = Ship(3, 2, 0, 0)
    s3 = Ship(3, 2, 0, 2)

    assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 0)"
    assert s1.is_collide(
        s3) == False, "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 2)"

    s2 = Ship(3, 2, 1, 1)
    assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 1, 1)"

    s2 = Ship(3, 1, 8, 1)
    assert s2.is_out_pole(10), "неверно работает метод is_out_pole() для корабля Ship(3, 1, 8, 1)"

    s2 = Ship(3, 2, 1, 5)
    assert s2.is_out_pole(10) == False, "неверно работает метод is_out_pole(10) для корабля Ship(3, 2, 1, 5)"

    s2[0] = 2
    # print(s2[0])
    assert s2[0] == 2, "неверно работает обращение ship[indx]"


def test_game_pole():
    p = GamePole(10)
    p.init()

    for nn in range(5):
        for s in p._ships:
            assert s.is_out_pole(10) == False, "корабли выходят за пределы игрового поля"

            for ship in p.get_ships():
                if s != ship:
                    assert s.is_collide(ship) == False, "корабли на игровом поле соприкасаются"
        p.move_ships()


def test_len_type():
    p = GamePole(10)
    p.init()
    gp = p.get_pole()
    assert type(gp) == tuple and type(gp[0]) == tuple, "метод get_pole должен возвращать двумерный кортеж"
    assert len(gp) == 10 and len(gp[0]) == 10, "неверные размеры игрового поля, которое вернул метод get_pole"

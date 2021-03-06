from typing import Optional

from unit import Unit

class UnitNotFound(Exception):
    pass

class Hex:

    # Just a singleton, but we like to write unreadable code

    def __init__(self, x: int, y: int, country = 0):
        """ Are you surprised? """
        self.x = x
        self.y = y
        self.country = country
        self.unit: Optional[Unit] = None

    @property
    def pos(self):
        return self.x, self.y


    def __add__(self, other):
        return Hex(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Hex(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f'<Hex({self.x}, {self.y})>'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.x) * 10 + hash(self.y)



class Direction:
    SOUTHEAST = 0
    NORTHEAST = 1
    NORTH = 2
    NORTHWEST = 3
    SOUTHWEST = 4
    SOUTH = 5


class HexMap:
    neighbors = [Hex(+1, 0),
                 Hex(+1, -1),
                 Hex(0, -1),
                 Hex(-1, 0),
                 Hex(-1, +1),
                 Hex(0, +1)]

    def __init__(self, sizex: int, sizey: int = None, preinit = False):
        if not sizey:
            sizey = sizex
        if preinit:
            self.map = {(x, y): Hex(x, y) for x in range(sizex) for y in range(sizey)}
        else:
            self.map = {}
        self.sizex = sizex
        self.sizey = sizey

    def move_unit(self, unit: Unit, direction: Direction):
        unit.hex = self.get_neighbor(unit.hex, direction)

    def reload_all_units(self):
        for unit in self.get_all_units():
            unit.reload()

    def set_unit(self, hex: Hex, unit: Unit):
        hex.unit = unit

    def get_all_units(self):
        for hex in self:
            if hex.unit:
                yield hex.unit

    def get_neighbor(self, hex: Hex, direction):
        return hex + self.neighbors[direction]

    def is_adjacent(self, one: Hex, other: Hex):
        return self.distance(one, other) == 1

    @staticmethod
    def get_hexes_in_range(hex: Hex, n: int):
        for x in range(-n, n+1):
            for y in range(max(-n, -x - n), min(n, -x + n) + 1):
                yield hex + Hex(x, y)

    @staticmethod
    def distance(hex: Hex, other: Hex):
        return (abs(hex.x - other.x) + + abs(hex.x + hex.y - other.x - other.y) + abs(hex.y - other.y)) / 2

    def __repr__(self):
        return f'<HexMap({self.sizex}, {self.sizey})>'

    def __iter__(self):
        for hex in self.map.values():
            yield hex

    def set_hex(self, position: tuple, hex: Hex):
        self.map[position] = hex

    def get_hex(self, position: tuple):
        return self.map[position]

# -*- coding: utf-8 -*-
__author__ = "Step"
import msvcrt
import collections
import os
import sys
from time import sleep

class Ring(object):
    def __init__(self, size):
        self.__size__ = size

    def __str__(self):
        return "<{0}>".format("=" * (2 * self.__size__ - 1))

    def __gt__(self, other):
        assert isinstance(other, Ring)

        return self.__size__ > other.__size__

    def __lt__(self, other):
        assert isinstance(other, Ring)

        return self.__size__ < other.__size__

class InvisibleRing(Ring):
    def __init__(self):
        super(InvisibleRing, self).__init__(0)

    def __str__(self):
        return "|"

    def __gt__(self, other):
        return True

class Pole(object):
    def __init__(self, height, width):
        self.__height__ = height
        self.__width__ = width
        self.__rings__ = collections.deque()

    def pullRing(self):
        if self.__rings__:
            return self.__rings__.pop()
        else:
            raise BaseException("Pole has no rings")

    def placeRing(self, ring):
        if self.__rings__:
            if self.__rings__[-1] > ring:
                self.__rings__.append(ring)
            else:
                raise ValueError("You cannot put bigger ring on the smaller")
        else:
            self.__rings__.append(ring)

    def __str__(self):
        lines = []
        ringsCount = len(self.__rings__)
        for section in xrange(self.__height__ - ringsCount):
            lines.append("|".center(self.__width__))
        for ring in reversed(self.__rings__):
            lines.append(str(ring).center(self.__width__))

        return "\n".join(lines)

class Hanoi(object):
    def __init__(self, numOfRings, numOfPoles=3):
        heightOfPole = numOfRings + 2
        widthOfPole = numOfRings * 2 + 1
        self.__frames__ = []
        self.__numOfRings__ = numOfRings
        #noinspection PyUnusedLocal
        self.__poles__ = [Pole(heightOfPole, widthOfPole) for i in xrange(numOfPoles)]
        for i in reversed(xrange(numOfRings)):
            self.__poles__[0].placeRing(Ring(i + 1))

    def __str__(self):
        poles = [str(pole).splitlines() for pole in self.__poles__]
        poles = zip(*poles)
        poles = [reduce(lambda x, y: "{0} {1}".format(x, y), pole) for pole in poles]
        return "\n".join(poles)

    def move(self, source, destination):
        ring = self.__poles__[source].pullRing()
        self.__poles__[destination].placeRing(ring)

        return "{0}\n\nRing moved from pole {1} to pole {2}".format(str(self), str(source + 1), str(destination + 1))

    def genSolveAnimation(self, n, source, destination, buf):
        if n:
            self.genSolveAnimation(n - 1, source, buf, destination)
            self.__frames__.append(self.move(source, destination))
            self.genSolveAnimation(n - 1, buf, destination, source)

    def playSolveAnimation(self, auto=None):
        if auto is None:
            auto = False
        if self.__frames__:
            frame = 0
            if auto:
                for frame in self.__frames__:
                    print frame
                    sleep(0.3)
                    os.system("cls")
            else:
                while -1 < frame < 2 ** self.__numOfRings__:
                    os.system("cls")
                    print self.__frames__[frame]
                    code = msvcrt.getch()
                    while code not in ("a", "d"):
                        code = msvcrt.getch()   
                    if code == "a":
                        frame -= 1
                    else:
                        frame += 1
        else:
            self.__frames__.append("{0}\n\nStarting move".format(str(self)))
            self.genSolveAnimation(self.__numOfRings__, 0, 2, 1)
            self.playSolveAnimation(auto)

towers = Hanoi(5)
# print towers.move(0, 1)
towers.playSolveAnimation()
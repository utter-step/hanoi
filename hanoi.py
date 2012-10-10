# -*- coding: utf-8 -*-
__author__ = "Step"
import msvcrt
import os
from time import sleep

class Animation(object):
    def __init__(self, from_, to, delay=0.02, multiframe=True):
        self.__delay__ = delay if multiframe else delay * 15
        self.__from__ = str(from_ + 1)
        self.__to__ = str(to + 1)
        if not multiframe and from_ == to:
            self.__start__ = True
        self.__multiframe__ = multiframe
        self._framebuffer__ = [] if multiframe else ""

    def addFrame(self, frame):
        if self.__multiframe__:
            self._framebuffer__.append(frame)
        else:
            self._framebuffer__ = frame

    def play(self):
        if self.__multiframe__:
            for frame in self._framebuffer__:
                os.system("cls")
                print frame
                print "\n\nMoving ring from {0} to {1}.".format(self.__from__, self.__to__)
                sleep(self.__delay__)
        else:
            os.system("cls")
            print self._framebuffer__
            if self.__start__:
                print "\n\nInitial position."
            else:
                print "\n\nMoving ring from {0} to {1}.".format(self.__from__, self.__to__)
            sleep(self.__delay__)

    def rewind(self):
        if self.__multiframe__:
            for frame in reversed(self._framebuffer__):
                os.system("cls")
                print frame
                print "\n\nReturning ring back from {1} to {0}.".format(self.__from__, self.__to__)
                sleep(self.__delay__)
        else:
            os.system("cls")
            print self._framebuffer__
            if self.__start__:
                print "\n\nReturned to the initial position."
            else:
                print "\n\nReturning ring back from {1} to {0}.".format(self.__from__, self.__to__)
            sleep(self.__delay__)


    def isEmpty(self):
        return bool(self._framebuffer__)


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
        self._rings__ = []

    def pullRing(self):
        if self._rings__:
            return self._rings__.pop()
        else:
            raise BaseException("Pole has no rings")

    def placeRing(self, ring):
        if self._rings__:
            if self._rings__[-1] > ring:
                self._rings__.append(ring)
            else:
                raise ValueError("You cannot put bigger ring on the smaller")
        else:
            self._rings__.append(ring)

    def freeSpace(self):
        return self.__height__ - len(self._rings__)

    def removeAllInvisible(self):
        while self.removeLastInvisible():
            pass

    def removeLastInvisible(self):
        for i in reversed(xrange(len(self._rings__))):
            if isinstance(self._rings__[i], InvisibleRing):
                del self._rings__[i]
                break
        else:
            return False
        return True

    def __str__(self):
        lines = []
        ringsCount = len(self._rings__)
        for section in xrange(self.__height__ - ringsCount):
            lines.append("|".center(self.__width__))
        for ring in reversed(self._rings__):
            lines.append(str(ring).center(self.__width__))

        return "\n".join(lines)


class Hanoi(object):
    def __init__(self, numOfRings, numOfPoles=3, multiframe=True):
        heightOfPole = numOfRings + 2
        widthOfPole = numOfRings * 2 + 1
        self.__animationHolder__ = [Animation(from_=0, to=0, multiframe=False)]
        self.__numOfRings__ = numOfRings
        #noinspection PyUnusedLocal
        self._poles__ = [Pole(heightOfPole, widthOfPole) for i in xrange(numOfPoles)]
        for i in reversed(xrange(numOfRings)):
            self._poles__[0].placeRing(Ring(i + 1))
        self.__animationHolder__[0].addFrame(str(self))
        self.genSolveAnimation(self.__numOfRings__, 0, 2, 1)

    def __str__(self):
        poles = [str(pole).splitlines() for pole in self._poles__]
        poles = zip(*poles)
        poles = [reduce(lambda x, y: "{0} {1}".format(x, y), pole) for pole in poles]
        return "\n".join(poles)

    def move(self, source, destination):
        ring = self._poles__[source].pullRing()
        self._poles__[destination].placeRing(ring)

        return "{0}\n\nRing moved from pole {1} to pole {2}".format(str(self), str(source + 1), str(destination + 1))

    def animatedMove(self, source, destination):
        holder = Animation(from_=source, to=destination)
        holder.addFrame(str(self))
        ring = self._poles__[source].pullRing()

        while self._poles__[source].freeSpace() > 1:
            self._poles__[source].placeRing(InvisibleRing())
            self._poles__[source].placeRing(ring)
            holder.addFrame(str(self))
            self._poles__[source].pullRing()
        self._poles__[source].removeAllInvisible()

        if abs(source - destination) > 1:
            while self._poles__[1].freeSpace() > 1:
                self._poles__[1].placeRing(InvisibleRing())
            self._poles__[1].placeRing(ring)
            holder.addFrame(str(self))
            self._poles__[1].pullRing()
            self._poles__[1].removeAllInvisible()

        while self._poles__[destination].freeSpace() > 0:
            self._poles__[destination].placeRing(InvisibleRing())
        self._poles__[destination].placeRing(ring)
        while self._poles__[destination].removeLastInvisible():
            holder.addFrame(str(self))

        return holder


    def genSolveAnimation(self, n, source, destination, buf):
        if n:
            self.genSolveAnimation(n - 1, source, buf, destination)
            self.__animationHolder__.append(self.animatedMove(source, destination))
            self.genSolveAnimation(n - 1, buf, destination, source)

    def playSolveAnimation(self, auto=None):
        if auto is None:
            auto = True
        if auto:
            for animation in self.__animationHolder__:
                animation.play()
        else:
            index = 0
            direction = 1
            while -1 < (index % 2 ** self.__numOfRings__) < 2 ** self.__numOfRings__:
                if direction == 1:
                    self.__animationHolder__[index].play()
                    print "Press 'a' and 'd' to move, 'q' to stop."
                    index += 1
                    index %= 2 ** self.__numOfRings__ - 1
                elif direction == -1:
                    index -= 1
                    index %= 2 ** self.__numOfRings__ - 1
                    self.__animationHolder__[index].rewind()
                    print "Press 'a' and 'd' to move, 'q' to stop."
                code = msvcrt.getch()
                while code not in ("a", "d", "q"):
                    code = msvcrt.getch()
                if code == "a":
                    direction = -1
                elif code == "d":
                    direction = 1
                elif code == "q":
                    break


def main():
    ringsCount = 0
    try:
        ringsCount = int(raw_input("\nRings count: "))
    except ValueError:
        print "Don't try to fool me."
        exit()
    print "\nPress any key to control movements.\nIf you press Enter it will be done automatically."
    key = msvcrt.getch()
    auto = (ord(key) == 13)
    towers = Hanoi(ringsCount)
    towers.playSolveAnimation(auto)
    if raw_input("Do you want to exit? (y/[n]): ") == "y":
        return False
    return True

if __name__ == "__main__":
    reRun = main()
    if reRun:
        main()

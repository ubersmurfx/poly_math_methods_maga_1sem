import matplotlib.pyplot as plt
import random
import math
import keyboard
from time import sleep
import threading

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Triangle:
    def __init__(self, a=Point(), b=Point(), c=Point()):
        self.ds = [a, b, c]

    def plot(self, color='b'):
        x = [p.x for p in self.ds] + [self.ds[0].x]
        y = [p.y for p in self.ds] + [self.ds[0].y]
        plt.plot(x, y, color + '-')
        plt.fill(x,y, color='gray', alpha=0.2)


def is_point_to_triangle(p, t):
    for i in range(3):
        j = (i + 1) % 3
        k = (p.x - t.ds[i].x) * (t.ds[i].y - t.ds[j].y) - (p.y - t.ds[i].y) * (t.ds[i].x - t.ds[j].x)
        if k < 0:
            return False
    return True

def is_intersect_line(a1, a2, b1, b2):
    b = Point(a2.x - a1.x, a2.y - a1.y)
    d = Point(b2.x - b1.x, b2.y - b1.y)

    dot = b.x * d.y - b.y * d.x
    if dot == 0:
        return False

    c = Point(b1.x - a1.x, b1.y - a1.y)
    t = (c.x * d.y - c.y * d.x) / dot
    if t < 0.0 or t > 1.0:
        return False

    t = (c.x * b.y - c.y * b.x) / dot
    return not (t < 0.0 or t > 1.0)

def is_intersect_triangle(a, b):
    for p in range(3):
        if is_point_to_triangle(a.ds[p], b) or is_point_to_triangle(b.ds[p], a):
            return True

    for i in range(3):
        for j in range(3):
            if is_intersect_line(a.ds[i], a.ds[(i + 1) % 3], b.ds[j], b.ds[(j + 1) % 3]):
                return True
    return False


def main():
    a = Triangle(
            Point(round(random.uniform(0, 300), 1), 50), 
            Point(150, round(random.uniform(0, 300), 1)), 
            Point(round(random.uniform(0, 300), 1), 100)
        )
    b= Triangle(
            Point(round(random.uniform(0, 300), 1), 50), 
            Point(150, round(random.uniform(0, 300), 1)), 
            Point(round(random.uniform(0, 300), 1), 100)
        )
    
    if is_intersect_triangle(a, b):
        print("Yes.")
    else:
        print("No!")
    a.plot('r')
    b.plot('g')

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Triangles intersect is {is_intersect_triangle(a, b)}")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(0, 300)
    plt.ylim(0, 300)
    plt.grid(True)
    plt.show(block=False)
    plt.pause(1)
    plt.close('all')
    plt.clf()

if __name__=="__main__":
    i = 0
    while i < 10:
        i =+ 1
        main()
        continue

    

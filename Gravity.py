#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Gravity'''

import os, sys
from tkinter import *
import math
import time
import json


root = Tk()

# Initiate the window and the canvas that will hold the planets
planets = []
entries = []
mempty = []
canvas = Canvas(root, bg='black', width=1000, height=500)
canvas.pack()
frame = Frame(root, bg='white', width=700, height=500)
frame.pack()


class Planet():
    '''
    Planet class

    Object keeping track of the speed vector and mass
    '''

    def __init__(self, x, y, sx, sy, m, color):
        self.sx = sx
        self.sy = sy
        self.m = m
        self.planet = canvas.create_oval(x-m/2, y-m/2, x+m/2, y+m/2, fill=color, state="hidden")
        self.color = color

    def move(self,planets):
        '''
        Move planet method
        '''
        canvas.move(self.planet, self.sx, self.sy)
        for p in planets:
            p.force(self)


    def coord(self):
        '''
        Get coordinates method
        '''
        dim = canvas.coords(self.planet)
        coord = [dim[2]-self.m/2, dim[3]-self.m/2]
        return coord

    def force(self, other_planet):
        '''
        Force method
        
        Using the law of attraction of the universe
        '''
        global planets
        if self is other_planet:
            return 0

        # Ensures that the gravity and speed vectors are in the right direction
        if self.m < other_planet.m:
            other_planet.force(self)
            return 0

        # Get the distance and calculate the mid gravity using m1*m2/d^2
        self_location = self.coord()
        other_location = other_planet.coord()
        difference = list(map(lambda x1,x2: x1-x2, self_location, other_location))
        d = 1.0 * difference[0] ** 2 + difference[1] ** 2
        adjacent = math.sqrt(d)
        min_distance = 20
        if d <= min_distance:
            return 1
        gravity = (self.m * other_planet.m) / d

        # Obtain the acceleration vectors
        ax = difference[0] / adjacent * gravity
        ay = difference[1] / adjacent * gravity

        # Ensures that the acceleration does not get too big
        other_planet.sx += ax
        other_planet.sy += ay

        return 0

    @staticmethod
    def object_decoder(obj):
        '''
        Object decoder class function
        '''
        saved_planet = Planet(int(obj['x']), int(obj['y']), int(obj["sx"]),
                              int(obj["sy"]), int(obj["m"]), obj["color"])
        return saved_planet

    def object_encoder(self):
        '''
        Object encoder method
        '''
        planet_json = json.dumps(self, default=lambda o: o.__dict__,
                                 sort_keys=False, indent=-1)
        coord = self.coord()
        coord = ' "x": %d, "y": %d, ' % (coord[0],coord[1])
        coord = str(coord)[1:-1]
        planet_json = planet_json[:1] + coord + planet_json[1:]
        return planet_json


def fuse(planet1, planet2):
    '''
    Fuse two planets function
    '''
    if planet2.m > planet1.m:
        planet1, planet2 = planet2, planet1
    planet1.m = planet1.m + planet2.m
    global canvas
    canvas.delete(planet2.planet)
    global planets
    planets = [planet1]

def simulation():
    '''
    World simulation function
    '''
    global planets
    global canvas
    for p in planets:
        canvas.itemconfig(p.planet, state="normal")
    while True:
        try:
            for p in planets:
                p.move(planets)
            root.update()
            time.sleep(1/slide_speed.get())
        except:
            exit(0)

def clear():
    '''
    Clear function
    '''
    for entry in entries:
        entry.delete(0, END)

def save():
    '''
    Save planets function
    '''
    global mempty
    try:
        nplanet = Planet(int(x.get()), int(y.get()), int(sx.get()), int(sy.get()),
                         int(m.get()), color.get())
        mempty.append(nplanet)
    except:
        pass


def addplanet():
    '''
    Add a planet function
    '''
    global canvas
    global mempty
    global planets
    try:
        nplanet = Planet(int(x.get()), int(y.get()), int(sx.get()), int(sy.get()),
                         int(m.get()), color.get())
        planets.append(nplanet)
        canvas.itemconfig(nplanet.planet, state="normal")
        for p in mempty:
            if p.coord() == [int(x.get()), int(y.get())]:
                canvas.delete(p.planet)
                continue
            canvas.itemconfig(p.planet, state="normal")
            planets.append(p)

        mempty = []
    except:
        for p in mempty:
            canvas.itemconfig(p.planet, state="normal")
            planets.append(p)
        mempty = []

def save_planets():
    '''
    Save planet objects to JSON file function
    '''
    file = open("data.json", "r")
    str = file.read()
    file.close()
    file = open("data.json", "w")
    str = str[:-1]
    file.write(str)
    for p in mempty:
        file.write(",\n")
        file.write(p.object_encoder())
    file.write("]")
    file.close()

def recover_from_file():
    '''
    Load data from JSON file function
    '''
    global canvas
    global planets
    file = open("data.json", "r")
    str = file.read()
    data = json.loads(str, object_hook=Planet.object_decoder)
    file.close()
    for p in data:
        canvas.itemconfig(p.planet, state="normal")
        planets.append(p)

def reset():
    '''
    Reset planets function
    '''
    for p in planets:
        canvas.delete(p.planet)


def main():
    '''
    Main function
    '''
    # Initialize the sun
    sun = Planet(500, 250, 0, 0, 100, "yellow")
    global planets
    reset()
    planets = []
    planets = [sun]
    root.after(0, simulation)
    root.mainloop()
    # earth = planet(250, 250, 1, 2, 49, "blue")
    # mars = planet(1000, 1000, -3, -5, 20, "red")
    return 0


# Buttons
restart = Button(frame, text="Restart simulation", command=main)
addp = Button(frame, text="Add planet", command=addplanet)
saveb = Button(frame, text="Save planet", command=save)
savfil = Button(frame, text="Store saved data", command=save_planets)
clear = Button(frame, text="Clear fields", command=clear)
slide_speed = Scale(frame, from_=1, to=100, orient=HORIZONTAL, length=200)
recfil = Button(frame, text="Load data", command=recover_from_file)

restart.grid(column=1, row=0)
addp.grid(column=4, row=0)
saveb.grid(column=5, row=1)
savfil.grid(column=5, row=3)
clear.grid(column=1, row=4)
slide_speed.set(1000)
slide_speed.grid(column=2, row=4)
recfil.grid(column=4, row=4)

# Fields
x = Entry(frame)
y = Entry(frame)
sx = Entry(frame)
sy = Entry(frame)
m = Entry(frame)
color = Entry(frame)

x.grid(column=1, row=1)
y.grid(column=4, row=1)
sx.grid(column=1, row=2)
sy.grid(column=4, row=2)
m.grid(column=1, row=3)
color.grid(column=4, row=3)

# Default values
x.insert(0, "200")
y.insert(0, "100")
sx.insert(0, "1")
sy.insert(0, "2")
m.insert(0, "30")
color.insert(0, "red")

# Labels
Label(frame, text="x").grid(column=0, row=1)
Label(frame, text="y").grid(column=3, row=1)
Label(frame, text="sx").grid(column=0, row=2)
Label(frame, text="sy").grid(column=3, row=2)
Label(frame, text="mass").grid(column=0, row=3)
Label(frame, text="color").grid(column=3, row=3)

entries = [x, y, sx, sy, m, color]


if __name__ == "__main__":
    sys.exit(main())

from tkinter import *
import math
import time
import json
import threading as th
root = Tk()
# Initiate the window and the canvas that will hold the planets
planets=[]
entries=[]
mempty=[]
canvas = Canvas(root,bg='black', width=1000, height=500)
canvas.pack()
frame = Frame(root, bg='white', width=700, height=500)
frame.pack()

# Object keeping track of the speed vector and mass
class planet():
    def __init__(self,x,y,sx,sy,m,color):
        self.sx = sx
        self.sy = sy
        self.m = m
        self.planet = canvas.create_oval(x-m/2,y-m/2,x+m/2,y+m/2,fill=color,state="hidden")
        self.color=color

    def move(self,planets):
        canvas.move(self.planet,self.sx,self.sy)
        for i in planets:
            i.force(self)


    def cord(self):
        dim = canvas.coords(self.planet)
        coord = [dim[2]-self.m/2,dim[3]-self.m/2]
        return coord
# Using the law of attraction of the universer
    def force(self,other_planet):


        if self is other_planet:
            return 0

# Ensures that the gravite and speed vectors are in the right direction
        if self.m < other_planet.m:
            other_planet.force(self)
            return 0

# Get the distance and calculate the mid gravity usin m1*m2/d^2
        self_location = self.cord()
        other_location = other_planet.cord()
        difference = list(map(lambda x1,x2: x1-x2,self_location,other_location))
        d = 1.0*difference[0]**2+difference[1]**2
        adjacent = math.sqrt(d)
        gravity = (self.m*other_planet.m)/d

# Obtain the acceleration vectores
        ax = difference[0] / adjacent * gravity
        ay = difference[1] / adjacent * gravity

# Ensures that the acceleration does not get too big
        other_planet.sx += ax
        other_planet.sy += ay


        return 0




# ToDO
def fuse(planet1,planet2):
    if planet2.m > planet1.m:
        planet1, planet2 = planet2, planet1
    planet1.m = planet1.m + planet2.m
    global canvas
    canvas.delete(planet2.planet)
    global planets
    planets=[planet1]

# Stimulates the word
def stimulation():
    global planets
    global canvas
    for p in planets:
        canvas.itemconfig(p.planet,state="normal")
    while True:
        try:
            for p in planets:
                p.move(planets)
            root.update()
            time.sleep(0.001)
        except:
            return 0




def clear():
    for entry in entries:
        entry.delete(0,END)

def save():
    global mempty
    try:
        nplanet = planet(int(x.get()), int(y.get()), int(sx.get()), int(sy.get()), int(m.get()), color.get())
        mempty.append(nplanet)
    except:
        pass


def addplanet():
    global canvas
    global mempty
    global planets
    try:
        nplanet=planet(int(x.get()),int(y.get()),int(sx.get()),int(sy.get()),int(m.get()),color.get())
        planets.append(nplanet)
        canvas.itemconfig(nplanet.planet, state="normal")
        for p in mempty:
            if p.cord() == [int(x.get()), int(y.get())]:
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





def reset():
    for i in planets:
        canvas.delete(i.planet)
# Initialize the sun
def main():
    sun = planet(500, 250, 0, 0, 100, "yellow")
    global planets
    reset()
    planets=[]
    planets=[sun]
    stimulation()
    # earth = planet(250, 250, 1, 2, 49, "blue")
    # earth1 = planet(1000, 1000, -3, -5, 20, "red")


restart = Button(frame, text="Restart", command=main)
restart.grid()

addp = Button(frame, text="Add Planet", command=addplanet)
addp.grid(column=1,row=0)

x=Entry(frame)
x.insert(0,"200")
x.grid(column=0,row=1)
y=Entry(frame)
y.insert(0,"100")
y.grid(column=1,row=1)

sx=Entry(frame)
sx.insert(0,"1")
sx.grid(column=0,row=2)

sy=Entry(frame)
sy.grid(column=1,row=2)
sy.insert(0,"2")

m=Entry(frame)
m.grid(column=0,row=3)
m.insert(0,"30")

color=Entry(frame)
color.insert(0,"red")
color.grid(column=1,row=3)

entries=[x,y,sx,sy,m,color]

clear = Button(frame, text="clear", command=clear)
clear.grid()

saveb= Button(frame, text="save", command=save)
saveb.grid(column=3,row=2)






if __name__== "__main__": main()

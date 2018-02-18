from tkinter import *
import math
import time
import threading as th
root = Tk()
# Initiate the window and the canvas that will hold the planets
planets=[]
canvas = Canvas(root,bg='black', width=1000, height=500)
canvas.pack()


# Object keeping track of the speed vector and mass
class planet():
    def __init__(self,x,y,sx,sy,m,color):
        self.sx = sx
        self.sy = sy
        self.m = m
        self.planet = canvas.create_oval(x-m/2,y-m/2,x+m/2,y+m/2,fill=color)
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
    while True:
        try:
            global planets
            for p in planets:
                p.move(planets)
            root.update()
            time.sleep(0.001)
        except:
            return 0





def addplanet():
    nplanet=planet(int(x.get()),int(y.get()),int(sx.get()),int(sy.get()),int(m.get()),color.get())
    global planets
    planets.append(nplanet)

def reset():
    for i in planets:
        canvas.delete(i.planet)
# Initialize the sun
def main():
    global planets
    reset()
    planets=[]
    sun = planet(500, 250, 0, 0, 100, "yellow")
    planets=[sun]
    stimulation()
    # earth = planet(250, 250, 1, 2, 49, "blue")
    # earth1 = planet(1000, 1000, -3, -5, 20, "red")

canvas1 = Canvas(root,bg='white', width=700, height=500)
canvas1.pack()

restart = Button(canvas1,text="Restart",command=main)
restart.grid()

addp = Button(canvas1,text="Add Planet", command=addplanet)
addp.grid(column=1,row=0)

x=Entry(canvas1)
x.insert(0,"200")
x.grid(column=0,row=1)

y=Entry(canvas1)
y.insert(0,"100")
y.grid(column=1,row=1)

sx=Entry(canvas1)
sx.insert(0,"1")
sx.grid(column=0,row=2)

sy=Entry(canvas1)
sy.grid(column=1,row=2)
sy.insert(0,"2")

m=Entry(canvas1)
m.grid(column=0,row=3)
m.insert(0,"30")

color=Entry(canvas1)
color.insert(0,"red")
color.grid(column=1,row=3)





if __name__== "__main__": main()

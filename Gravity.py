from tkinter import *
import time

class planet():
    def __init__(self,x,y,sx,sy,m,color):
        self.sx = sx
        self.sy = sy
        self.m = m
        self.planet = canvas.create_oval(x-m/2,y-m/2,x+m/2,x+m/2,fill=color)
        self.color=color

    def move(self):
        canvas.move(self.planet,self.sx,self.sy)

    def cord(self):
        dim = canvas.coords(self.planet)
        coord = [dim[2]-self.m/2,dim[3]-self.m/2]
        return coord

    def collide(self,earth):
        us = self.cord()
        them = earth.cord()
        return us[0]==them[0] and them[1]==us[1]


def fuse(planet1,planet2):
    m = planet1.m+planet2.m
    if planet2.m > planet1.m:
        planet1, planet2 = planet2, planet1
    coord=planet1.cord()
    newplanet = planet(coord[0],coord[1],planet1.sx,planet1.sy,m,planet1.color)
    canvas.delete(planet1)
    canvas.delete(planet2)
    planets.remove(planet1)
    planets.remove(planet2)
    return newplanet




root = Tk()
canvas = Canvas(root,bg='black', width=500, height=512)
canvas.pack()
sun = planet(250,250,-1,-1,100,"yellow")
sun1 = planet(0,0,1,1,50,"yellow")
sun2 = canvas.create_oval(10,10,50,50,fill="brown")
planets= [sun,sun2,sun1]
while True:
    sun.move()
    sun1.move()
    if sun.collide(sun1):
        fuse(sun,sun1)
    root.update()
    time.sleep(0.1)
    canvas.delete(sun2)

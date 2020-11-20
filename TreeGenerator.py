# L-system implementation

import pymel.core as pm
from pymel.all import *
import pymel.core.datatypes as dt
import maya.cmds as cmds
import math

directions = []
points = []
HEIGHT = 1
count = 0

currentPos = dt.Vector(0, 0, 0)
currentDir = dt.Vector(0, 1, 0)


# Rewrite rules
def applyRules(lhch):
    rhch = ""
    if(lhch == "F"):
        rhch = "F - F"  # Rule 1
    if(lhch == "-"):
        rhch = " - "      # Rule 2
    if(lhch == "+"):
        rhch = " + "      # Rule 3

    return rhch

# How the 'turtle' should interpretend the characters


def turtleInterpretation(ch):
    global currentPos, currentDir
    if(ch == "F"):
        points.append(currentPos)
        directions.append(currentDir)
        forwardStep()
    if(ch == "-"):
        rotAxis = currentDir.cross(dt.Vector(1.0, 1.0, 0.0))
        currentDir = currentDir.rotateBy(rotAxis, pi/6.0)
        currentDir = currentDir.normal()
    if(ch == "+"):
        rotAxis = currentDir.cross(dt.Vector(1.0, 0.0, 1.0))
        currentDir = currentDir.rotateBy(rotAxis, pi/4.0)
        currentDir = currentDir.normal()

# Process string so the rules can be applied for each character


def processString(oldStr):
    newstr = ""
    for ch in oldStr:
        newstr = newstr + applyRules(ch)

    return newstr


def createLSystem(numIters, axiom, lSystem_):
    startString = axiom
    endString = ""
    lSystem = lSystem_
    for i in range(numIters):
        endString = processString(startString)
        lSystem.append(endString)
        startString = endString

    return endString

# Calculate new position


def forwardStep():
    global currentPos
    currentPos = currentPos.__add__(currentDir)

# Create the mesh, loops through all the characters


def createMesh(arr):
    global currentDir, currentPos, count
    for i in range(len(arr)):
        for ch in arr[i]:
            turtleInterpretation(ch)


lSystem = []
createLSystem(2, "F + F", lSystem)
createMesh(lSystem)
# for i in range(len(points)):
#    pm.sphere(name="sphere{}".format(i))
#    pm.scale("sphere{}".format(i), [0.05, 0.05, 0.05])
#    pm.move("sphere{}".format(i), points[i])
pm.curve(name="curve", p=points)

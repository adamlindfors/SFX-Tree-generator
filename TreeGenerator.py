# L-system implementation

import pymel.core as pm
from pymel.all import *
import pymel.core.datatypes as dt
import maya.cmds as cmds
import math

curves = []
curvesStack = []
directionStack = []
positionStack = []
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
        rhch = "  F + [ F + F ] - F"  # Rule 1
    if(lhch == "-"):
        rhch = " - "      # Rule 2
    if(lhch == "+"):
        rhch = " + "      # Rule 3
    if(lhch == "["):
        rhch = " [ "      # Rule 4
    if(lhch == "]"):
        rhch = " ] "      # Rule 5
    if(lhch == "s"):
        rhch = "s"

    return rhch

# How the 'turtle' should interpretend the characters


def turtleInterpretation(ch):
    global currentPos, currentDir, points
    if(ch == "F"):
        points.append(currentPos)
        directions.append(currentDir)
        forwardStep()
    if(ch == "-"):
        rotAxis = currentDir.cross(dt.Vector(1.0, 1.0, 0.0))
        currentDir = currentDir.rotateBy(rotAxis, pi/6.0)
        currentDir = currentDir.normal()
    if(ch == "+"):
        rotAxis = currentDir.cross(dt.Vector(1.0, 1.0, 1.0))
        currentDir = currentDir.rotateBy(rotAxis, -1*pi/4.0)
        currentDir = currentDir.normal()
    if(ch == "["):
        copyPoints = copyList(points)
        curvesStack.append(copyPoints)
        positionStack.append(currentPos)
        directionStack.append(currentDir)
    if(ch == "]"):
        copyPoints = copyList(points)
        curves.append(copyPoints)
        points = curvesStack.pop()
        currentPos = positionStack.pop()
        currentDir = directionStack.pop()
    if(ch == "s"):
        curves.append(points)

    # Process string so the rules can be applied for each character


def copyList(lst):
    tmpLst = list(lst)
    return tmpLst


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


def createMesh(arr, numIters):
    global currentDir, currentPos, count
    for ch in arr[numIters-1]:
        turtleInterpretation(ch)


n = 2
lSystem = []
createLSystem(n, "F + F - [F] + s", lSystem)
createMesh(lSystem, n)
print(curves[6])
for i in range(len(curves)):
    if(len(curves[i]) >= 4):
        pm.curve(name="curve{}".format(i), p=curves[i])
        pm.circle(name="surface{}".format(i), nr=(
            0, 1, 0), c=curves[i][0], r=0.1)
        pm.extrude("surface{}".format(i), "curve{}".format(
            i), et=2, scale=0.5, pivot=(0, 0, 0))

# pm.curve(name="curve", p=points)

# pm.circle(name="surface", nr=(0, 1, 0), c=(0, 0, 0), r=0.1)
# pm.extrude('surface', "curve", et=2, scale=0.5)

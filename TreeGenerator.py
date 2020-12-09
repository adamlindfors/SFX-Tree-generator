# L-system implementation

# TODO -----------------------------------------------------------
# Fix holes in tree
# Add leafs to tree
# Add shader to tree
# Add gui
# Add different radius to tree
# Fix different angles from the same branch
# No downward branches
# Fix better angles
# ---------------------------------------------------------------


import pymel.core as pm
from pymel.all import *
import pymel.core.datatypes as dt
import maya.cmds as cmds
import math
import random

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

points.append(currentPos)

# Rewrite rules


def applyRules(lhch):
    rhch = ""
    if(lhch == "F"):
        rhch = "^F[&+F]F[->FL][&FB]"  # Rule 1
    if(lhch == "-"):
        rhch = "-"      # Rule 2
    if(lhch == "+"):
        rhch = "+"      # Rule 3
    if(lhch == "<"):
        rhch = "<"
    if(lhch == ">"):
        rhch = ">"
    if(lhch == "^"):
        rhch = "^"
    if(lhch == "&"):
        rhch = "&"
    if(lhch == "["):
        rhch = "["      # Rule 4
    if(lhch == "]"):
        rhch = "]"      # Rule 5
    if(lhch == "s"):
        rhch = "s"

    return rhch

# How the 'turtle' should interpretend the characters


def turtleInterpretation(ch):
    global currentPos, currentDir, points
    if(ch == "F"):
        forwardStep()
        points.append(currentPos)
        directions.append(currentDir)
    if(ch == "-"):
        # Rotate -X (yaw left)
        randAngle = random.randint(2, 8)
        rotAxis = getRotationAxis(currentDir, dt.Vector(1.0, 0.0, 0.0))
        currentDir = currentDir.rotateBy(rotAxis, pi/randAngle)
        currentDir = currentDir.normal()
    if(ch == "+"):
        # Rotate +X (yaw right)
        randAngle = random.randint(2, 8)
        rotAxis = getRotationAxis(currentDir, dt.Vector(1.0, 0.0, 0.0))
        currentDir = currentDir.rotateBy(rotAxis, -1*pi/randAngle)
        currentDir = currentDir.normal()
    if(ch == "^"):
        # Rotate +Y (roll right)
        randAngle = random.randint(2, 8)
        rotAxis = getRotationAxis(currentDir, dt.Vector(0.0, 1.0, 0.0))
        currentDir = currentDir.rotateBy(rotAxis, 1*pi/randAngle)
        currentDir = currentDir.normal()
    if(ch == "&"):
        # Rotate -Y (roll left)
        randAngle = random.randint(2, 8)
        rotAxis = getRotationAxis(currentDir, dt.Vector(0.0, 1.0, 0.0))
        currentDir = currentDir.rotateBy(rotAxis, -1*pi/randAngle)
        currentDir = currentDir.normal()
    if(ch == "<"):
        # Rotate +Z (pitch down)
        randAngle = random.randint(2, 8)
        rotAxis = getRotationAxis(currentDir, dt.Vector(0.0, 0.0, 1.0))
        currentDir = currentDir.rotateBy(rotAxis, 1*pi/randAngle)
        currentDir = currentDir.normal()
    if(ch == ">"):
        # Rotate -Z (pitch up)
        randAngle = random.randint(2, 8)
        rotAxis = getRotationAxis(currentDir, dt.Vector(0.0, 0.0, 1.0))
        currentDir = currentDir.rotateBy(rotAxis, -1*pi/randAngle)
        currentDir = currentDir.normal()
    if(ch == "["):
        copyPoints = copyList(points)
        curvesStack.append(copyPoints)
        positionStack.append(currentPos)
        directionStack.append(currentDir)
        points *= 0
        points.append(currentPos)
    if(ch == "]"):
        copyPoints = copyList(points)
        curves.append(copyPoints)
        points *= 0
        points = curvesStack.pop()
        currentPos = positionStack.pop()
        currentDir = directionStack.pop()
    if(ch == "s"):
        curves.append(points)

        # Process string so the rules can be applied for each character


def getRotationAxis(dir, dir2):
    if(dir.isParallel(dir2)):
        return dir.cross(dt.Vector(1.0, 1.0, 1.0).__sub__(dir2))
    else:
        return dir2


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


def createCurve(arr, numIters):
    global currentDir, currentPos, count
    for ch in arr[numIters-1]:
        turtleInterpretation(ch)


def numberScale(start, stop, i):
    values = range(i)


def createMesh(crv):
    for i in range(len(crv)):
        if(len(crv[i]) >= 6):
            pm.curve(name="curve{}".format(i), p=crv[i], d=1)
            pm.circle(name="surface{}".format(i),
                      nr=crv[i][1] - crv[i][0], c=crv[i][0], r=0.1)
            temp = pm.extrude("surface{}".format(i), "curve{}".format(
                i), et=2, pivot=crv[i][0], scale=1, po=1)
            polys.append(temp)
        else:
            pm.curve(name="curve{}".format(i), p=crv[i], d=1)
            pm.circle(name="surface{}".format(i),
                      nr=crv[i][1] - crv[i][0], c=crv[i][0], r=0.03)
            temp = pm.extrude("surface{}".format(i), "curve{}".format(
                i), et=2, pivot=crv[i][0], scale=1, po=1)
            polys.append(temp)


n = 4
lSystem = []
polys = []
createLSystem(n, "F s", lSystem)
createCurve(lSystem, n)
createMesh(curves)

pm.polyUnite(polys, name="TreePoly")


# print(pm.objectType("TreePoly"))


# pm.circle(name="surface", nr=(0, 1, 0), c=(0, 0, 0), r=0.1)
# pm.extrude('surface', "curve", et=2, scale=0.5)

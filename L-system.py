# L-system implementation

import pymel.core as pm
import pymel.core.datatypes as dt
import maya.cmds as cmds
import math

HEIGHT = 1
count = 0
prevDir = [0.0, 0.5, 0.0]
currentDir = [0.0, 0.0, 0.0]


# Rewrite rules
def applyRules(lhch):
    rhch = ""
    if(lhch == "F"):
        rhch = "F - F"  # Rule 1

    return rhch

# How the 'turtle' should interpretend the characters


def turtleInterpretation(ch):
    global currentDir, count, prevDir
    if(ch == "F"):
        name = "cylinder{}".format(count)
        count = count + 1

        pm.polyCylinder(name=name, height=HEIGHT, radius=0.1, axis=prevDir)
        pivot = [prevDir[0]*-1, prevDir[1]*-1, prevDir[2]*-1]
        print(pivot)
        pm.move(pivot[0], pivot[1], pivot[2], name +
                ".scalePivot", name + ".rotatePivot", ls=True)

       # pm.move(name, prevDir, absolute=True, rpr=True, ws=True)
        forwardStep()
    if(ch == "-"):
        theta = 30
        phi = 12
        r = 1
        prevDir = normalize3(arrayAdd3(prevDir, [r * math.sin(phi) * math.cos(theta),
                                                 r * math.sin(phi) * math.sin(theta), r * math.cos(phi)]))

# Process string so the rules can be applied for each character


def processString(oldStr):
    newstr = ""
    for ch in oldStr:
        newstr = newstr + applyRules(ch)

    return newstr

# Create and save the system


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
    global prevDir
    # currentPos = normalize3(arrayAdd3(currentPos, normalize3(
    # arrayAdd3(currentPos, currentDir))))

    prevDir = [prevDir[0]*2, prevDir[1]*2, prevDir[2]*2]


# Add the elements of an array of size 3


def arrayAdd3(arr1, arr2):
    return [arr1[0] + arr2[0], arr1[1] + arr2[1], arr1[2] + arr2[2]]


def arraySub3(arr1, arr2):
    return [arr1[0] - arr2[0], arr1[1] - arr2[1], arr1[2] - arr2[2]]

# Normalize an array of size 3


def normalize3(vector):
    x = vector[0]/math.sqrt(vector[0]*vector[0] + vector[1]
                            * vector[1] + vector[2]*vector[2])
    y = vector[1]/math.sqrt(vector[0]*vector[0] + vector[1]
                            * vector[1] + vector[2]*vector[2])
    z = vector[2]/math.sqrt(vector[0]*vector[0] + vector[1]
                            * vector[1] + vector[2]*vector[2])
    return [x*0.5, y*0.5, z*0.5]


def norm3(vector):
    res = math.sqrt(vector[0]*vector[0] + vector[1]
                    * vector[1] + vector[2]*vector[2])
    return res


# Create the mesh, loops through all the characters


def createMesh(arr):
    global currentDir, currentPos, count
    for i in range(len(arr)):
        for ch in arr[i]:
            turtleInterpretation(ch)


lSystem = []
createLSystem(1, "F", lSystem)
createMesh(lSystem)

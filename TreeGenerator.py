# L-system implementation

# TODO -----------------------------------------------------------
# Fix holes in tree
# Add gui
# Multiple trees
# ---------------------------------------------------------------


import pymel.core as pm
from pymel.all import *
import pymel.core.datatypes as dt
import maya.cmds as cmds
import math
import random


cmds.file(force=True, newFile=True)
curves = []
curvesStack = []
directionStack = []
positionStack = []
directions = []
points = []
leafs = []
flowers = []
HEIGHT = 1
leafCount = 0
blossomCount = 0


currentPos = dt.Vector(0, 0, 0)
currentDir = dt.Vector(0, 1, 0)

points.append(currentPos)

# Rewrite rules


def applyRules(lhch):
    rhch = ""
    if(lhch == "F"):
        rhch = "^F[&+FL]F[->FL][&FLB]"  # Rule 1
    if(lhch == "-"):
        rhch = "-"
    if(lhch == "+"):
        rhch = "+"
    if(lhch == "<"):
        rhch = "<"
    if(lhch == ">"):
        rhch = ">"
    if(lhch == "^"):
        rhch = "^"
    if(lhch == "&"):
        rhch = "&"
    if(lhch == "["):
        rhch = "["
    if(lhch == "]"):
        rhch = "]"
    if(lhch == "L"):
        rhch = "L"
    if(lhch == "B"):
        rhch = "B"
    if(lhch == "s"):
        rhch = "s"

    return rhch

# How the 'turtle' should interpretend the characters


def turtleInterpretation(ch):
    global currentPos, currentDir, points, leafCount, blossomCount, leafGeo, blossomGeo
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
    if(ch == "L"):
        pm.duplicate("leaf_geo_mb:pPlaneShape1",
                     name="leaf" + str(leafCount))
        pm.select("leaf" + str(leafCount))
        pm.move(currentPos.x, currentPos.y, currentPos.z)
        pm.rotate("leaf" + str(leafCount), [str(random.randint(0, 360)) + "deg", str(
            random.randint(0, 360)) + "deg", str(random.randint(0, 360)) + "deg"])
        pm.scale(0.05, 0.05, 0.05)
        leafs.append("leaf" + str(leafCount))
        leafCount = leafCount+1
    if(ch == "B"):
        pm.duplicate("blossom_geo_mb:polySurfaceShape2",
                     name="blossom" + str(blossomCount))
        pm.select("blossom" + str(blossomCount))
        pm.move(currentPos.x, currentPos.y, currentPos.z)
        pm.rotate("blossom" + str(blossomCount), [str(random.randint(0, 360)) + "deg", str(
            random.randint(0, 360)) + "deg", str(random.randint(0, 360)) + "deg"])
        pm.scale(0.2, 0.2, 0.2)
        flowers.append("blossom" + str(blossomCount))
        blossomCount = blossomCount+1
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
    global currentDir, currentPos
    for ch in arr[numIters-1]:
        turtleInterpretation(ch)


def loadGeo(fileName):
    dir_path = cmds.internalVar(userScriptDir=1)
    pm.importFile(dir_path+"/Objects/" + fileName, i=True,
                  namespace=str(fileName))


def createMesh(crv):
    for i in range(len(crv)):
        if(len(crv[i]) == 2):
            pm.curve(name="curve{}".format(i), p=crv[i], d=1)
            pm.circle(name="surface{}".format(i),
                      nr=crv[i][1] - crv[i][0], c=crv[i][0], r=random.uniform(0.01, 0.05))
            temp = pm.extrude("surface{}".format(i), "curve{}".format(
                i), et=2, pivot=crv[i][0], po=1, dl=0.5)
            polys.append(temp)
        else:
            pm.curve(name="curve{}".format(i), p=crv[i], d=1)
            crl = pm.circle(name="surface{}".format(i),
                            nr=crv[i][1] - crv[i][0], c=crv[i][0], r=0.1)
            temp = pm.extrude("surface{}".format(i), "curve{}".format(
                i), et=2, pivot=crv[i][0], scale=0.5, po=1, dl=0.5)
            polys.append(temp)


loadGeo("leaf_geo.mb")
loadGeo("blossom_geo.mb")
n = 4
lSystem = []
polys = []
createLSystem(n, "F s", lSystem)
createCurve(lSystem, n)
createMesh(curves)
pm.delete("leaf_geo_mb:pPlaneShape1")
pm.delete("blossom_geo_mb:polySurfaceShape2")

TreePoly = pm.polyUnite(polys, name="TreePoly")
LeafPoly = pm.polyUnite(leafs, name="LeafPoly")
BlossomPoly = pm.polyUnite(flowers, name="BlossomPoly")
pm.polyReduce(TreePoly, p=90)
pm.polyReduce(LeafPoly, p=50)

# -----------------------Shaders----------------------------------------------


def createShader(obj, texturePathColor, texturePathBump):
    objectName = obj[0]
    shaderName = "shader"+objectName
    fileTextureNameColor = "filePathImageColor"+objectName
    fileTextureNameBump = "filePathImageBump"+objectName
    uvImageName = "uvFileImage"+objectName

    pm.shadingNode('lambert', asShader=True, name=shaderName)
    pm.shadingNode('file', asTexture=True, name=fileTextureNameColor)
    pm.shadingNode('file', asTexture=True, name=fileTextureNameBump)
    pm.shadingNode('bump2d', asTexture=True, name="bumpMap" + objectName)

    pm.connectAttr(fileTextureNameColor + '.outColor', shaderName + '.color')
    pm.connectAttr(fileTextureNameBump + '.outAlpha',
                   "bumpMap" + objectName + ".bumpValue")
    pm.connectAttr("bumpMap" + objectName + ".outNormal",
                   shaderName + '.normalCamera')
    cmds.setAttr(shaderName + ".ambientColor", 0.5, 0.5, 0.5)
    pm.setAttr(fileTextureNameColor+'.fileTextureName',
               texturePathColor, type='string')
    pm.setAttr(fileTextureNameBump+' .fileTextureName',
               texturePathColor, type='string')

    pm.select(objectName, replace=True)
    pm.hyperShade(assign=shaderName)
    pm.shadingNode('place2dTexture', asUtility=True, name=uvImageName)
    pm.defaultNavigation(connectToExisting=True,
                         source=uvImageName, destination=fileTextureNameColor)

# ----------------------------------------------------------------------------


# Add textures folder to where script is being run from within maya
dir_path = cmds.internalVar(userScriptDir=1)
createShader(TreePoly, dir_path + "/Shaders/TreeBark/color.tif",
             dir_path + "Shaders/TreeBark/bump.tif")

createShader(LeafPoly, dir_path + "/Shaders/Leaf/grass.tif",
             dir_path + "Shaders/Leaf/Leaf_Ulmus_Bump.tga")
createShader(BlossomPoly, dir_path + "/Shaders/Blossom/iridescent_paper.tif",
             dir_path + "Shaders/Leaf/Leaf_Ulmus_Bump.tga")
# print(LeafPoly)

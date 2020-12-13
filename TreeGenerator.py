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
leafs = []
flowers = []
leafCount = 0
blossomCount = 0


class Tree:
    def __init__(self, startPos):
        self.lSys = []
        self.startPos = startPos
        self.poly = 0

        self.currentPos = self.startPos
        self.currentDir = dt.Vector(0, 1, 0)
        self.curves = []
        self.curves = []
        self.curvesStack = []
        self.directionStack = []
        self.positionStack = []
        self.points = []
        self.points.append(self.startPos)
        self.polys = []
        self.leafs = []
        self.flowers = []
        self.numIters = 0

    def createLSystem(self, numIters, axiom):
        startString = axiom
        self.numIters = numIters
        endString = ""
        lSystem = []
        for i in range(self.numIters):
            endString = processString(startString)
            lSystem.append(endString)
            startString = endString

        self.lSys = endString

    def forwardStep(self):
        self.currentPos = self.currentPos.__add__(self.currentDir)

    def turtleInterpretation(self, ch):
        global leafCount, blossomCount
        if(ch == "F"):
            self.forwardStep()
            self.points.append(self.currentPos)
            # self.directions.append(self.currentDir)
        if(ch == "-"):
            # Rotate -X (yaw left)
            randAngle = random.randint(2, 8)
            rotAxis = getRotationAxis(
                self.currentDir, dt.Vector(1.0, 0.0, 0.0))
            self.currentDir = self.currentDir.rotateBy(rotAxis, pi/randAngle)
            self.currentDir = self.currentDir.normal()
        if(ch == "+"):
            # Rotate +X (yaw right)
            randAngle = random.randint(2, 8)
            rotAxis = getRotationAxis(
                self.currentDir, dt.Vector(1.0, 0.0, 0.0))
            self.currentDir = self.currentDir.rotateBy(
                rotAxis, -1*pi/randAngle)
            self.currentDir = self.currentDir.normal()
        if(ch == "^"):
            # Rotate +Y (roll right)
            randAngle = random.randint(2, 8)
            rotAxis = getRotationAxis(
                self.currentDir, dt.Vector(0.0, 1.0, 0.0))
            self.currentDir = self.currentDir.rotateBy(rotAxis, 1*pi/randAngle)
            self.currentDir = self.currentDir.normal()
        if(ch == "&"):
            # Rotate -Y (roll left)
            randAngle = random.randint(2, 8)
            rotAxis = getRotationAxis(
                self.currentDir, dt.Vector(0.0, 1.0, 0.0))
            self.currentDir = self.currentDir.rotateBy(
                rotAxis, -1*pi/randAngle)
            self.currentDir = self.currentDir.normal()
        if(ch == "<"):
            # Rotate +Z (pitch down)
            randAngle = random.randint(2, 8)
            rotAxis = getRotationAxis(
                self.currentDir, dt.Vector(0.0, 0.0, 1.0))
            self.currentDir = self.currentDir.rotateBy(rotAxis, 1*pi/randAngle)
            self.currentDir = self.currentDir.normal()
        if(ch == ">"):
            # Rotate -Z (pitch up)
            randAngle = random.randint(2, 8)
            rotAxis = getRotationAxis(
                self.currentDir, dt.Vector(0.0, 0.0, 1.0))
            self.currentDir = self.currentDir.rotateBy(
                rotAxis, -1*pi/randAngle)
            self.currentDir = self.currentDir.normal()
        if(ch == "["):
            copyPoints = copyList(self.points)
            self.curvesStack.append(copyPoints)
            self.positionStack.append(self.currentPos)
            self.directionStack.append(self.currentDir)
            self.points *= 0
            self.points.append(self.currentPos)
        if(ch == "]"):
            copyPoints = copyList(self.points)
            self.curves.append(copyPoints)
            self.points *= 0
            self.points = self.curvesStack.pop()
            self.currentPos = self.positionStack.pop()
            self.currentDir = self.directionStack.pop()
        if(ch == "L"):
            pm.duplicate("leaf_geo_mb:pPlaneShape1",
                         name="leaf" + str(leafCount))
            pm.select("leaf" + str(leafCount))
            pm.move(self.currentPos.x, self.currentPos.y, self.currentPos.z)
            pm.rotate("leaf" + str(leafCount), [str(random.randint(0, 360)) + "deg", str(
                random.randint(0, 360)) + "deg", str(random.randint(0, 360)) + "deg"])
            pm.scale(0.05, 0.05, 0.05)
            self.leafs.append("leaf" + str(leafCount))
            leafCount = leafCount+1
        if(ch == "B"):
            pm.duplicate("blossom_geo_mb:polySurfaceShape2",
                         name="blossom" + str(blossomCount))
            pm.select("blossom" + str(blossomCount))
            pm.move(self.currentPos.x, self.currentPos.y, self.currentPos.z)
            pm.rotate("blossom" + str(blossomCount), [str(random.randint(0, 360)) + "deg", str(
                random.randint(0, 360)) + "deg", str(random.randint(0, 360)) + "deg"])
            pm.scale(0.2, 0.2, 0.2)
            self.flowers.append("blossom" + str(blossomCount))
            blossomCount = blossomCount+1
        if(ch == "s"):
            self.curves.append(self.points)

    def createCurve(self):
        for ch in self.lSys:
            self.turtleInterpretation(ch)

    def createMesh(self, j):
        for i in range(len(self.curves)):
            if(len(self.curves[i]) == 2):
                pm.curve(name="curve{}".format(j) +
                         "_" + str(i), p=self.curves[i], d=1)
                pm.circle(name="surface{}".format(j) + "_" + str(i),
                          nr=self.curves[i][1] - self.curves[i][0], c=self.curves[i][0], r=random.uniform(0.01, 0.05))
                temp = pm.extrude("surface{}".format(j) + "_" + str(i), "curve{}".format(
                    j) + "_" + str(i), et=2, pivot=self.curves[i][0], po=1, dl=0.5)
                self.polys.append(temp)
            else:
                pm.curve(name="curve{}".format(j) +
                         "_" + str(i), p=self.curves[i], d=1)
                pm.circle(name="surface{}".format(j) + "_" + str(i),
                          nr=self.curves[i][1] - self.curves[i][0], c=self.curves[i][0], r=0.1)
                temp = pm.extrude("surface{}".format(j) + "_" + str(i), "curve{}".format(
                    j) + "_" + str(i), et=2, pivot=self.curves[i][0], scale=0.5, po=1, dl=0.5)
                self.polys.append(temp)


def applyRules(lhch):
    rhch = ""
    if(lhch == "F"):
        rhch = "^F[&+FL]F[->FL][&FLB]"
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

# Create the mesh, loops through all the characters


def loadGeo(fileName):
    dir_path = cmds.internalVar(userScriptDir=1)
    pm.importFile(dir_path+"/Objects/" + fileName, i=True,
                  namespace=str(fileName))


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


loadGeo("leaf_geo.mb")
loadGeo("blossom_geo.mb")

n = 4
Trees = []
myTree1 = Tree(dt.Vector(random.randint(-5, 5),
                         0, random.randint(-5, 5)))
myTree2 = Tree(dt.Vector(random.randint(-5, 5),
                         0, random.randint(-5, 5)))

myTree3 = Tree(dt.Vector(random.randint(-5, 5),
                         0, random.randint(-5, 5)))
myTree4 = Tree(dt.Vector(random.randint(-5, 5),
                         0, random.randint(-5, 5)))
myTree5 = Tree(dt.Vector(random.randint(-5, 5),
                         0, random.randint(-5, 5)))
Trees.append(myTree1)
Trees.append(myTree2)
Trees.append(myTree3)
Trees.append(myTree4)
Trees.append(myTree5)


dir_path = cmds.internalVar(userScriptDir=1)

for i in range(len(Trees)):
    Trees[i].createLSystem(n, "F s")
    Trees[i].createCurve()
    Trees[i].createMesh(i)
    TreePoly = pm.polyUnite(Trees[i].polys, name="TreePoly")
    LeafPoly = pm.polyUnite(Trees[i].leafs, name="LeafPoly")
    BlossomPoly = pm.polyUnite(Trees[i].flowers, name="BlossomPoly")
    pm.polyReduce(TreePoly, p=90)
    pm.polyReduce(LeafPoly, p=50)

    # Add textures folder to where script is being run from within maya
    createShader(TreePoly, dir_path + "/Shaders/TreeBark/color.tif",
                 dir_path + "Shaders/TreeBark/bump.tif")

    createShader(LeafPoly, dir_path + "/Shaders/Leaf/grass.tif",
                 dir_path + "Shaders/Leaf/Leaf_Ulmus_Bump.tga")
    createShader(BlossomPoly, dir_path + "/Shaders/Blossom/iridescent_paper.tif",
                 dir_path + "Shaders/Leaf/Leaf_Ulmus_Bump.tga")

pm.delete("leaf_geo_mb:pPlaneShape1")
pm.delete("blossom_geo_mb:polySurfaceShape2")

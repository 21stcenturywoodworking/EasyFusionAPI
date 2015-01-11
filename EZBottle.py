# Author Dirk Van Essendelft
# Copyright 1/2/2015 21st Century Woodworking

import adsk.core, adsk.fusion, traceback, math

from .EasyFusionAPI import EZFusionAPI

fa = EZFusionAPI()
# scale of the bottle size
scale = 2.0

# unit - cm
height = 21
topWidth = 2.8
topHight = 1.9
bodyTopWidth = 0.4
bottomWidth = 3.2
upperArcCenterToTop = 4.5
upperArcRadius = 16
lowerArcRadius = 15
filletRadius = 0.5
thickness = 0.3

# used for direct modeling
upperArcMidPtXOffset = -0.18
upperArcMidPtYOffset = -4.1
upperArcEndPtXOffset = 0.46
upperArcEndPtYOffset = -7.2
lowerArcMidPtXOffsetFromOriginPt = 4.66
lowerArcMidPtYOffsetFromOriginPt = 5.9

bottomCenter = adsk.core.Point3D.create(0, 0, 0)
bottleMaterial = 'Glass'
bottleAppearance = 'Glass (Green)'
materialLibName = 'Fusion 360 Material Library'
appearanceLibName = 'Fusion 360 Appearance Library'

nearZero = 0.000001

app = adsk.core.Application.get()
ui  = app.userInterface

def createBottle():
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    currentDesignType = design.designType
    # scale the size
    global height, topWidth, topHight, bodyTopWidth, bottomWidth, upperArcCenterToTop, upperArcRadius, lowerArcRadius, filletRadius, thickness
    height = height * scale
    topWidth = topWidth * scale
    topHight = topHight * scale
    bodyTopWidth = bodyTopWidth * scale
    bottomWidth = bottomWidth * scale
    upperArcCenterToTop = upperArcCenterToTop * scale
    upperArcRadius = upperArcRadius * scale
    lowerArcRadius = lowerArcRadius * scale
    filletRadius = filletRadius * scale
    thickness = thickness * scale

    if currentDesignType == adsk.fusion.DesignTypes.DirectDesignType:
        global upperArcMidPtXOffset, upperArcMidPtYOffset, upperArcEndPtXOffset, upperArcEndPtYOffset, lowerArcMidPtXOffsetFromOriginPt, lowerArcMidPtYOffsetFromOriginPt
        upperArcMidPtXOffset = upperArcMidPtXOffset * scale
        upperArcMidPtYOffset = upperArcMidPtYOffset * scale
        upperArcEndPtXOffset = upperArcEndPtXOffset * scale
        upperArcEndPtYOffset = upperArcEndPtYOffset * scale
        lowerArcMidPtXOffsetFromOriginPt = lowerArcMidPtXOffsetFromOriginPt * scale
        lowerArcMidPtYOffsetFromOriginPt = lowerArcMidPtYOffsetFromOriginPt * scale

    #create Sketch
    baseSketch = fa.EZSketch(fa.__base__.rootComp.xYConstructionPlane)
    #sketch = baseSketch.get_Sketch()

    # add sketch curves

    endPt = bottomCenter.copy() #start from bottomCenter
    endPt.y = bottomCenter.y + height
    heightLine = baseSketch.create.line(bottomCenter, endPt)

    endPt.x = endPt.x + topWidth
    topLine = baseSketch.create.line(heightLine.endSketchPoint, endPt)

    endPt.y = endPt.y - topHight
    topHightLine = baseSketch.create.line(topLine.endSketchPoint, endPt)

    endPt.x = endPt.x + bodyTopWidth
    topBodyLine = baseSketch.create.line(topHightLine.endSketchPoint, endPt)

    #sketchArcs = sketch.sketchCurves.sketchArcs

    if currentDesignType == adsk.fusion.DesignTypes.DirectDesignType:
        endPt.x = topBodyLine.endSketchPoint.geometry.x + upperArcEndPtXOffset
        endPt.y = topBodyLine.endSketchPoint.geometry.y + upperArcEndPtYOffset
        ptOnArc = baseSketch.create.point(topBodyLine.endSketchPoint.geometry.x + upperArcMidPtXOffset, topBodyLine.endSketchPoint.geometry.y + upperArcMidPtYOffset)
        upperArc = baseSketch.create.arc([topBodyLine.endSketchPoint, ptOnArc, endPt],'3p')

        endPt = bottomCenter.copy()
        endPt.x = bottomWidth
        ptOnArc = baseSketch.create.point(lowerArcMidPtXOffsetFromOriginPt, lowerArcMidPtYOffsetFromOriginPt)
    else:
        deltPos = 0.1
        endPt.x = topWidth + bodyTopWidth + bodyTopWidth
        endPt.y = height / 2
        ptOnArc = baseSketch.create.point(endPt.x - deltPos, endPt.y + deltPos)
        upperArc = baseSketch.create.arc([topBodyLine.endSketchPoint, ptOnArc, endPt],'3p')

        endPt = bottomCenter.copy()
        endPt.x = bottomWidth
        ptOnArc = baseSketch.create.point(endPt.x + deltPos, endPt.y + deltPos)

    lowerArc = baseSketch.create.arc([upperArc.endSketchPoint, ptOnArc, endPt], '3p')
    buttomLine = baseSketch.create.line(lowerArc.startSketchPoint, heightLine.startSketchPoint)

    # add constraints
    #sketchConstraints = sketch.geometricConstraints
    baseSketch.set.object_Fix(heightLine.startSketchPoint,True)
    baseSketch.constrain.geometric([buttomLine],'h')
    baseSketch.constrain.geometric([buttomLine, heightLine],'perp')
    baseSketch.constrain.geometric([heightLine, topLine],'perp')
    baseSketch.constrain.geometric([topLine, topHightLine],'perp')
    baseSketch.constrain.geometric([topHightLine, topBodyLine],'perp')

    # add dimensions
    baseSketch.constrain.dimension([heightLine.startSketchPoint,heightLine.endSketchPoint])
    baseSketch.constrain.dimension([topLine.startSketchPoint,topLine.endSketchPoint])
    baseSketch.constrain.dimension([topHightLine.startSketchPoint,topHightLine.endSketchPoint])
    baseSketch.constrain.dimension([topBodyLine.startSketchPoint, topBodyLine.endSketchPoint])
    baseSketch.constrain.dimension([buttomLine.startSketchPoint, buttomLine.endSketchPoint])

    if currentDesignType == adsk.fusion.DesignTypes.DirectDesignType:
        baseSketch.constrain.dimension([topLine.endSketchPoint, upperArc.centerSketchPoint],orientation='Vertical')
    else:
        baseSketch.constrain.dimension([topLine.endSketchPoint, upperArc.centerSketchPoint], orientation='Vertical', value = upperArcCenterToTop)
        baseSketch.constrain.dimension(upperArc,value=upperArcRadius)
        baseSketch.constrain.dimension(lowerArc,value=lowerArcRadius)

    # create revolve
    revolveFeat = fa.EZFeatures()
    revolveFeat.create.revolve(baseSketch.get.profiles()[0], heightLine)

    # create fillets
    # select the edges to do fillets
    body = revolveFeat.get.bRepBody()
    edgeCol = adsk.core.ObjectCollection.create()
    for edge in body.edges:
        circle = edge.geometry
        if math.fabs(circle.radius - bottomWidth) < nearZero or math.fabs(circle.radius - topWidth - bodyTopWidth) < nearZero:
            edgeCol.add(edge)
    
    revolveFeat.modify.fillet(edgeCol,filletRadius,distanceUnits = 'cm')

    # create shell
    # select the faces to remove
    faces = revolveFeat.get.faces()
    faceCol = adsk.core.ObjectCollection.create()
    for face in faces:
        # find the top face
        if face.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType:
            edge0 = face.edges[0]
            if edge0.geometry.center.isEqualTo(heightLine.endSketchPoint.worldGeometry):
                faceCol.add(face)
                break
            
    revolveFeat.modify.shell(faceCol,thickness,distanceUnits='cm')
    
    revolveFeat.modify.material(bottleMaterial)
    revolveFeat.modify.appearance(bottleAppearance)

    app.activeViewport.refresh()

def main():
    try:
        createBottle();

    except:
        if ui:
           ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

main()

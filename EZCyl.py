#Author-
#Description-

import adsk.core, adsk.fusion, traceback

from .EasyFusionAPI import EZFusionAPI

def main():
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        fa = EZFusionAPI()
        
        fa.create_UserParameter('PinHandleLength',2,units = 'in',favorite=True)
        fa.create_UserParameter('PinHandleDiameter',0.5,units = 'in',favorite=True)
        fa.create_UserParameter('PinLength',10,units = 'in',favorite=True)
        fa.create_UserParameter('PinDiameter',2,units = 'in',favorite=True)
        fa.create_UserParameter('PinFilletRad',0.25,units = 'in',favorite=True)
        
        
        s1 = fa.EZSketch(fa.__base__.rootComp.xYConstructionPlane)
        s1.create.circle((0,0),'cr',expression = 'PinHandleDiameter')
        
        end1 = fa.EZFeatures()
        end1.create.extrude(s1.get.profiles()[0],'PinHandleLength')
        
        s2 = fa.EZSketch(end1.get.faces('end')[0],startCurveConstruction = True)
        s2.create.circle((0,0),'cr',expression = 'PinDiameter')
        
        middle = fa.EZFeatures()
        middle.create.extrude(s2.get.profiles()[0],'PinLength')
        
        s3 = fa.EZSketch(middle.get.faces('end')[0],startCurveConstruction=True)
        s3.create.circle((0,0),'cr',expression='PinHandleDiameter')
    
        end2 = fa.EZFeatures()
        end2.create.extrude(s3.get.profiles()[0],'PinHandleLength')
        
        middle.modify.fillet(middle.get.allEdges_ObjectCollection(),'PinFilletRad')
        
        end1.modify.material('Wood')
        end2.modify.material('Wood')
        middle.modify.material('Wood')
    
    
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

main()

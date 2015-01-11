#Author-Dirk Van Essendelft
#Description- Creates an ice cube in a parametric way
#copyright 2015 21st Century Woodworking Inc

import adsk.core, adsk.fusion, traceback

from .EasyFusionAPI import EZFusionAPI

def main():
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        fa = EZFusionAPI()
        fa.create_UserParameter('CubeWidth',1,units='in',favorite=True)
        fa.create_UserParameter('CubeLength',1,units='in',favorite=True)
        fa.create_UserParameter('CubeHeight',1,units='in',favorite=True)
        fa.create_UserParameter('CubeFillet',0.25,units='in',favorite=True)
        sketch1 = fa.EZSketch()
        sketch1.create.rectangle([(0,0),(1,1)],'2pr',fixPoint = 0,expressions=['CubeWidth','CubeLength'])
        
        box = fa.EZFeatures()
        box.create.extrude(sketch1.get.profiles()[0],'CubeHeight')
        box.modify.fillet(box.get.allEdges_ObjectCollection(),'CubeFillet')
        
        box.modify.material('Glass')
        box.modify.appearance('Glass - Heavy Color (Blue)')

        

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

main()

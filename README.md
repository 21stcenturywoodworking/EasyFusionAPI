<!-- TITLE/ -->
# EZFusionAPI
<!-- TITLE/ -->

<!-- /SHORT DESCRIPTION -->
Fast, Program Oriented Geometry Generation for Fusion 360 Through the Autodesk Python API 
<!-- /SHORT DESCRIPTION -->

<!-- /DESCRIPTION -->
## What is the EZFusionAPI?

The EZFusionAPI is a python class that makes using the Autodesk Fusion 360 API a snap.  Autodesk has been developing an API for Fusion 360 and exposing functionality through python, Java, and eventually C++.  Their API is extremely powerful for generatig geometry and parametrically conrolling geometry from another program.  However, the basic exposure through the Autodesk API means that the coding is relatively low level which makes your programs repetative and long.  The EZFusionAPI groups commonly used tasks into methods that can be called in a single line.  It also employs smart decision making based on the objects sent into the methods to automatically determine user intent.  This is done in a very simmilar way to what is done in the GUI within Fusion 360.  The objective of this project is to create a class that enables a user to make geometry in Fusion 360 as fast as possible in a programming environment while maintaining access to all the basic exposure of the Autodesk API should it be.
<!-- /DESCRIPTION -->

<!-- /ABOUTSPONSOR -->
## Who Makes EZFusionAPI?
[![Sponsor Website](https://img.shields.io/badge/sponsor-website-yellow.svg)](http://www.21stcenturywoodworking.com "21st Century Woodworking Home")

The EZFusionAPI is being developed by maintained by 21st Century Woodworking LLC.  21st Century Woodworking LLC is a small company based out of Morgantown, WV and exists to provide woodworkers with the tools needed to use 21st century tools like CNC routers, lasers, and 3d printers into their shop and into their project workflows.  21st Century Woodworking LLC is working towards a "1 click print" capability for the woodworking world through the use of Fusion 360 and has been developing the EZFusionAPI as part of this effort.
<!-- /ABOUTSPONSOR -->

## Is EZFusionAPI Free?
[![PayPay donate button](https://img.shields.io/badge/paypal-donate-yellow.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=4RJ9CKBDMVYRY "Donate to Keep Project Going")

Yes!  However, the time to develop this capability is valuable and we believe that the EZFusionAPI will also save you valuable time in your end epplication as well.  We are offering this code at no cost and asking our users to consider supporting this work via donation to keep it growing.  We will do our best to respond to questions and provide user support
and add features uppon request.  We also ask that you consider subsequent donation if obtaining a newer version.

## How is EZFusionAPI Licensed?
[![Code License](https://img.shields.io/badge/code-license-yellow.svg)](https://github.com/21stcenturywoodworking/EasyFusionAPI/blob/master/LICENSE "GNU GPL V3.0")

EZFusionAPI is covered under the GNU GPL v3.0 license.  We ask that you do not change the header in the code if it is used so that proper credit is given and copyright notice is given.  Any derivative work of this code must maintain a GNU GPL v3.0 license.

## How do I use EZFusionAPI?
1) The download the latest copy of the EZFusionAPI via github

2) Copy the EasyFusionAPI.py file into the "My Scripts" folder in Fusion 360

    Locating the "My Scripts" Folder
    1) To get to the "My Scripts" folder, open Fusion 360 and navigate to File -> Scripts...
    2) You will see a My Scripts folder with a green "+" at the top of the Scripts Manager window
    3) If you don't have a script started yet, click on the green "+" icon and create a python script
    4) Highlight a python script and activate the Details "+" button near the bottom of the Scripts Manager
    5) Click on the button next to the Full Path box (it hass 3 dots on it)
    6) This will bring up a file manager window to the "My Scripts" folder where you need to copy the
       EasyFusionAPI.py
  
3)Import the EZFusionAPI into your script using:
```python
from .EasyFusionAPI import EZFusionAPI
```
4) Either create an instance of the Easy Fusion API or Inherit it into your class

## Examples

Here is a simple way to create a cube that is parametrically controlled and looks like an ice cube

```python
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
```


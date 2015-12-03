# Maxwell MXS to ASCII Translator
# --------------------------------------------
# 2015-12-03 6:14 am v0.1
# By Andrew Hazelden 
# Email: andrew@andrewhazelden.com
# Blog: http://www.andrewhazelden.com

# Description
# -----------
# This tool will convert a binary format MXS scene file into a plain text ascii format that is easier for a rendering TD to review and edit.


# Script Installation
# -------------------
# Copy the mxs2ascii.py python file to your Maxwell 3.2 scripts directory:

# Windows
# C:/Program Files/Next Limit/Maxwell 3/scripts/

# Linux
# /opt/maxwell/3/scripts/

# Mac
# /Applications/Maxwell 3/scripts/


# How do I use the script?
# ------------------------

# Step 1.
# Launch PyMaxwell and open up the `mxs2ascii.py` python script.

# Step 2.
# Edit the "mxsFilePath" variable in the main function near the bottom of this script and specify your Maxwell Studio based MXS scene file.

# Step 3. Select the Script > Run menu item in PyMaxwell.

# The script will start running. First the script will verify the mxs scene file exists. Then the scene will be opened in Maxwell and all of the scene elements and parameters will be exported to an ASCII text document with the name of `<scene>.mas`. This new file is saved to the same folder as the original mxs scene file.

# -----------------------------------------

from pymaxwell import *
from math import *
import os
import sys


# :
# Example: writeAsciiScene('/Cube.mas')
def writeAsciiScene(mxsFilePath):
  print('\n\n')
  print('Maxwell MXS to ASCII Translator for Maxwell Studio')
  print('By Andrew Hazelden <andrew@andrewhazelden.com>')
  print('-----------------------------------------------\n')
  # Find out the current scene file
  dirName = os.path.dirname(mxsFilePath)
  sceneName = os.path.basename(mxsFilePath)
  scenePathNoExt = os.path.splitext(mxsFilePath)[0]

  # Find out the current scene
  scene = Cmaxwell(mwcallback)
  scene.readMXS(mxsFilePath)
  it = CmaxwellCameraIterator()

  # Camera Details
  #camera = it.first(scene)
  camera = scene.getActiveCamera()
  cameraName = camera.getName()

  # Camera Parameters
  position,focalPoint,up,focalLength,fStop,stepTime,ok = camera.getStep(0)

  # Get object position (camera target)
  #target,ok = camera.getPosition()

  # Camera Resolution
  res = camera.getResolution()
  width = res[0]
  height = res[1]

  print('[Working Directory] ' + dirName)
  print('[Input Scene] ' + sceneName + ' [Camera] ' + str(cameraName) + ' [Resolution] ' + str(width) + 'x' + str(height))


  # -------------------------------------------------------
  # Write the ASCII text format scene to disk
  # -------------------------------------------------------
 
  asciiSceneFilename = scenePathNoExt + '.mas'
  print('[Maxwell Ascii Scene] ' + os.path.basename(asciiSceneFilename))
  
  #ok = scene.writeMXS(asciiSceneFilename)
  #if ok == 0:
  #  print('There was an error saving: ' + asciiSceneFilename)
  #  return 0

  print('\n--------------------------------------')
  print('Ascii Scene Export Complete')
  return 1


# This code is the "main" section that is run automatically when the python script is loaded in pyMaxwell:
if __name__ == "__main__":

  # Choose a Maxwell MXS scene file to process:
  mxsFilePath = '/Applications/Maxwell 3/scripts/stereo/CubeX.mxs'
  # mxsFilePath = 'C:/Program Files/Next Limit/Maxwell 3/scripts/stereo/CubeX.mxs'
  # mxsFilePath = '/opt/maxwell-3.2/scripts/stereo/CubeX.mxs'
  # mxsFilePath = '/home/andrew/maxwell-3.2/scripts/stereo/CubeX.mxs'

  # Launch the automagic stereo camera set up command
  if os.path.exists(mxsFilePath):
    # Generate the stereo project files
  	ok = writeAsciiScene(mxsFilePath,)
  else:
    print('[MXS File Not Found] ' + mxsFilePath)


# Maxwell MXS to ASCII Translator
# --------------------------------------------
# 2015-12-03 7:43 am v0.1
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
import datetime

# Write the Maxell Ascii Scene to Disk
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

 #Scene.imagePath

  textDocument = ''
  
  # Temporary Placeholder values
  time_limit = 1440
  sampling_level = 16
  multilight = 'intensity'
  multilight_output = 'composite'
  cpu_threads = 'Automatic'
  priority = 'low'
  quality = 'production'
  command_line = ''
  depth = 16
  image = '/Users/Andrew/Documents/maxwell/image.png'
  mxi = '/Users/Andrew/Documents/maxwell/image.mxi'
  materials_override = ''
  materials_default = ''
  materials_search_path = '/Users/Andrew/Documents/maxwell'
  motion_blur = 'on'
  displacement = 'on'
  dispersion = 'on'
  extra_sampling_enabled = 'off'
  extra_sampling_mask = 'Custom'
  extra_sampling_level = 14
  extra_sampling_custom_alpha = ''
  extra_sampling_bitmap = ''
  extra_sampling_invert_mask = 'off'
  channels_output_mode = 'separate'
  channels_render = 'off'
  channels_alpha = 'off'
  channels_opaque = 'off'
  channels_zbuffer = 'off'
  channels_zbuffer_meters = "1.0 1.0"
  channels_shadow = 'off'
  channels_material_id = 'off'
  channels_object_id = 'off'
  channels_motion_vector = 'off'
  channels_roughness = 'off'
  channels_fresnel = 'off'
  channels_normals = 'off'
  channels_normals_mode = 'World'
  channels_position  = 'off'
  channels_position_mode = 'World'
  channels_deep = 'off'
  channels_deep_mode = 'Alpha'
  channels_deep_min_distance_meters = 0.2
  channels_deep_max_samples = 20
  channels_uv = 'off'
  channels_custom_alpha = 'off'
  channels_reflectance = 'off'
  tone_mapping_color_space = 'sRGB IEC61966-2.1'
  tone_mapping_white_point = 6500
  tone_mapping_tint = 0.0
  tone_mapping_burn = 0.8
  tone_mapping_monitor_gamma = 2.20
  tone_mapping_sharpness_enabled = 'off'
  tone_mapping_sharpness = 60.0
  simulens_aperture_map = ''
  simulens_obstacle_map = ''
  simulens_diffraction = 1250.0
  simulens_frequency = 1250.0
  simulens_scattering = 250.0
  simulens_devingetting = 100.0
  illumination = 'Both'
  reflection_caustics = 'Both'
  refraction_caustics = 'Both'
  fire_floating_shadows = 'off'
  fire_floating_refractions = 'off'
  overlay_text = ''
  overlay_text_position = ''
  overlay_text_color = '1.0 1.0 1.0'
  overlay_text_background = '0.0 0.0 0.0'
  
  # Add the Maxwell ASCII header text
  now = datetime.datetime.now()
  textDocument += '# Generated:  ' + now.strftime('%Y-%m-%d %H:%M:%S %p') + '\n'
  textDocument += '# Using: Maxwell 3.2.0.2 Mac OS X 10.10.5\n\n'

  # Indent spacer - either a tab or two spaces
  # indent = '\t'
  indent = '  '
  
  
  # Add the render_options section
  textDocument += 'render_options\n'
  textDocument += '{\n'
  
  textDocument += indent + 'time_limit ' + str(time_limit) + '\n'
  textDocument += indent + 'sampling_level ' + str(sampling_level) + '\n'
  textDocument += indent + 'multilight "' + str(multilight) + '"\n'
  textDocument += indent + 'multilight_output "' + str(multilight_output) + '"\n'
  textDocument += indent + 'cpu_threads "' + str(cpu_threads) + '"\n'
  textDocument += indent + 'priority "' + str(priority) + '"\n'
  textDocument += indent + 'quality "' + str(quality) + '"\n'
  textDocument += indent + 'command_line "' + str(command_line) + '"\n'
  textDocument += indent + 'depth ' + str(depth) + '\n'
  textDocument += indent + 'image "' + str(image) + '"\n'
  textDocument += indent + 'mxi "' + str(mxi) + '"\n'
  textDocument += indent + 'materials_override "' + str(materials_override) + '"\n'
  textDocument += indent + 'materials_default "' + str(materials_default) + '"\n'
  textDocument += indent + 'materials_search_path "' + str(materials_search_path) + '"\n'
  textDocument += indent + 'motion_blur ' + str(motion_blur) + '\n'
  textDocument += indent + 'displacement ' + str(displacement) + '\n'
  textDocument += indent + 'dispersion ' + str(dispersion) + '\n'
  textDocument += indent + 'extra_sampling_enabled ' + str(extra_sampling_enabled) + '\n'
  textDocument += indent + 'extra_sampling_mask "' + str(extra_sampling_mask) + '"\n'
  textDocument += indent + 'extra_sampling_level ' + str(extra_sampling_level) + '\n'
  textDocument += indent + 'extra_sampling_custom_alpha ' + str(extra_sampling_custom_alpha) + '\n'
  textDocument += indent + 'extra_sampling_bitmap ' + str(extra_sampling_bitmap) + '\n'
  textDocument += indent + 'extra_sampling_invert_mask ' + str(extra_sampling_invert_mask) + '\n'
  textDocument += indent + 'channels_output_mode "' + str(channels_output_mode) + '"\n'
  textDocument += indent + 'channels_render ' + str(channels_render) + '\n'
  textDocument += indent + 'channels_alpha ' + str(channels_alpha) + '\n'
  textDocument += indent + 'channels_opaque ' + str(channels_opaque) + '\n'
  textDocument += indent + 'channels_zbuffer ' + str(channels_zbuffer) + '\n'
  textDocument += indent + 'channels_zbuffer_meters ' + str(channels_zbuffer_meters) + '\n'
  textDocument += indent + 'channels_shadow ' + str(channels_shadow) + '\n'
  textDocument += indent + 'channels_material_id ' + str(channels_material_id) + '\n'
  textDocument += indent + 'channels_object_id ' + str(channels_object_id) + '\n'
  textDocument += indent + 'channels_motion_vector ' + str(channels_motion_vector) + '\n'
  textDocument += indent + 'channels_roughness ' + str(channels_roughness) + '\n'
  textDocument += indent + 'channels_fresnel ' + str(channels_fresnel) + '\n'
  textDocument += indent + 'channels_normals ' + str(channels_normals) + '\n'
  textDocument += indent + 'channels_normals_mode "' + str(channels_normals_mode) + '"\n'
  textDocument += indent + 'channels_position ' + str(channels_position) + '\n'
  textDocument += indent + 'channels_position_mode "' + str(channels_position_mode) + '"\n'
  textDocument += indent + 'channels_deep ' + str(channels_deep) + '\n'
  textDocument += indent + 'channels_deep_mode "' + str(channels_deep_mode) + '"\n'
  textDocument += indent + 'channels_deep_min_distance_meters ' + str(channels_deep_min_distance_meters) + '\n'
  textDocument += indent + 'channels_deep_max_samples ' + str(channels_deep_max_samples) + '\n'
  textDocument += indent + 'channels_uv ' + str(channels_uv) + '\n'
  textDocument += indent + 'channels_custom_alpha ' + str(channels_custom_alpha) + '\n'
  textDocument += indent + 'channels_reflectance ' + str(channels_reflectance) + '\n'
  textDocument += indent + 'tone_mapping_color_space "' + str(tone_mapping_color_space) + '"\n'
  textDocument += indent + 'tone_mapping_white_point ' + str(tone_mapping_white_point) + '\n'
  textDocument += indent + 'tone_mapping_tint ' + str(tone_mapping_tint) + '\n'
  textDocument += indent + 'tone_mapping_burn ' + str(tone_mapping_burn) + '\n'
  textDocument += indent + 'tone_mapping_monitor_gamma ' + str(tone_mapping_monitor_gamma) + '\n'
  textDocument += indent + 'tone_mapping_sharpness_enabled ' + str(tone_mapping_sharpness_enabled) + '\n'
  textDocument += indent + 'tone_mapping_sharpness ' + str(tone_mapping_sharpness) + '\n'
  textDocument += indent + 'simulens_aperture_map ' + str(simulens_aperture_map) + '\n'
  textDocument += indent + 'simulens_obstacle_map ' + str(simulens_obstacle_map) + '\n'
  textDocument += indent + 'simulens_diffraction ' + str(simulens_diffraction) + '\n'
  textDocument += indent + 'simulens_frequency ' + str(simulens_frequency) + '\n'
  textDocument += indent + 'simulens_scattering ' + str(simulens_scattering) + '\n'
  textDocument += indent + 'simulens_devingetting ' + str(simulens_devingetting) + '\n'
  textDocument += indent + 'simulens_devingetting ' + str(simulens_devingetting) + '\n'
  textDocument += indent + 'illumination "' + str(illumination) + '"\n'
  textDocument += indent + 'reflection_caustics "' + str(reflection_caustics) + '"\n'
  textDocument += indent + 'refraction_caustics "' + str(refraction_caustics) + '"\n'
  textDocument += indent + 'fire_floating_shadows ' + str(fire_floating_shadows) + '\n'
  textDocument += indent + 'fire_floating_refractions ' + str(fire_floating_refractions) + '\n'
  textDocument += indent + 'overlay_text ' + str(overlay_text) + '\n'
  textDocument += indent + 'overlay_text_position ' + str(overlay_text_position) + '\n'
  textDocument += indent + 'overlay_text_color ' + str(overlay_text_color) + '\n'
  textDocument += indent + 'overlay_text_background ' + str(overlay_text_background) + '\n'
  
  # Close the render_options section
  textDocument += '}\n'
  
  # -------------------------------------------------------
  # Write the ASCII text format scene to disk
  # -------------------------------------------------------
 
  asciiSceneFilename = scenePathNoExt + '.mas'
  print('[Maxwell Ascii Scene] ' + os.path.basename(asciiSceneFilename))
  print('[Document Contents] \n' + textDocument)

  asciiFile = open(asciiSceneFilename, 'w')
  ok = asciiFile.write(textDocument)
  asciiFile.close
  
  if ok == 0:
    print('\n--------------------------------------')
    print('There was an error saving: ' + asciiSceneFilename)
    return 0
  else:
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


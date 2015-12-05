# Maxwell MXS to ASCII Translator
# --------------------------------------------
# 2015-12-04 9.00 pm v0.1
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

# The script will start running. First the script will verify the mxs scene file exists. Then the scene will be opened in Maxwell and all of the scene elements and parameters will be exported to an ASCII text document with the name of `<scene>.mxa`. This new file is saved to the same folder as the original mxs scene file.

# -----------------------------------------

from pymaxwell import *
from math import *
import os
import sys
import datetime

# Write the Maxell Ascii Scene to Disk
# Example: writeAsciiScene('/Cube.mas')
def b2a_writeAsciiScene(mxsFilePath):

  # Release Version
  b2a_version = "0.1"


  print('\n\n')
  print('Maxwell MXS to ASCII Scene Translator v' + b2a_version)
  print('By Andrew Hazelden <andrew@andrewhazelden.com>')
  print('http://www.andrewhazelden.com/blog')
  print('-----------------------------------------------\n')
  

  # Find out the current scene file
  dirName = os.path.dirname(mxsFilePath)
  sceneName = os.path.basename(mxsFilePath)
  scenePathNoExt = os.path.splitext(mxsFilePath)[0]

  # Find out the current scene
  scene = Cmaxwell(mwcallback)
  scene.readMXS(mxsFilePath)
  it = CmaxwellCameraIterator()

  #print('[MXS Scene Created in] ' + str(scene.getPluginID))
  
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

  textDocument = ''
  
  # MXS Scene Render Opton Values
  active_camera = cameraName
  
  # Scene
  time_limit = scene.getRenderParameter('STOP TIME')[0] / 60
  sampling_level = scene.getRenderParameter('SAMPLING LEVEL')[0]
  
  # USE MULTILIGHT = 'intensity'
  multilight = ''
  if scene.getRenderParameter('USE MULTILIGHT')[0] == 0:
    # No multilight
    multilight = 'disabled'
  elif scene.getRenderParameter('USE MULTILIGHT')[0] == 1:
    # Intensity multilight
    multilight = 'intensity'
  elif scene.getRenderParameter('USE MULTILIGHT')[0] == 2:
    # Color multilight
    multilight = 'color'
  else:
    multilight = 'unknown'
  
  # SAVE LIGHTS IN SEPARATE FILES
  multilight_output = 'separate' if scene.getRenderParameter('SAVE LIGHTS IN SEPARATE FILES')[0] else 'composite'
  
  # NUM THREADS Automatic = 0
  #cpu_threads = scene.getRenderParameter('NUM THREADS')[0]
  cpu_threads = scene.getRenderParameter('NUM THREADS')[0] if scene.getRenderParameter('NUM THREADS')[0] else '"automatic"'
  
  # priority = 'low'
  
  # ENGINE is the render quality
  quality = ''
  if scene.getRenderParameter('ENGINE')[0] == 'RS0':
    quality = 'draft'
  elif scene.getRenderParameter('ENGINE')[0] == 'RS1':
    quality = 'production'
  else:
    quality = 'unknown'
  
  # command_line = ''

  # Output
  depth = 16
  #Scene.imagePath
  
  # COPY IMAGE AFTER RENDER '/Users/Andrew/Documents/maxwell/image.png'
  image = scene.getRenderParameter('COPY IMAGE AFTER RENDER')[0]
  
  # COPY MXI AFTER RENDER 'Users/Andrew/Documents/maxwell/image.mxi'
  mxi = scene.getRenderParameter('COPY MXI AFTER RENDER')[0]
 
  # Materials
  materials_override_enable = "on" if scene.getOverrideMaterialEnabled() else "off"
  materials_override  = scene.getOverrideMaterial()
  materials_default = scene.getDefaultMaterial()
  materials_search_path = ''

  # Globals
  motion_blur = "on" if scene.getRenderParameter('DO MOTION BLUR')[0] else "off"
  displacement = "on" if scene.getRenderParameter('DO DISPLACEMENT')[0] else "off"
  dispersion = "on" if scene.getRenderParameter('DO DISPERSION')[0] else "off"

  # Extra Sampling
  extra_sampling_enabled = "on" if scene.getRenderParameter('DO EXTRA SAMPLING')[0] else "off"
  
  extra_sampling_mask = ''
  if scene.getRenderParameter('EXTRA SAMPLING MASK')[0] == EXTRA_SAMPLING_CUSTOM_ALPHA:
    extra_sampling_mask = 'custom alpha'
  elif scene.getRenderParameter('EXTRA SAMPLING MASK')[0] == EXTRA_SAMPLING_ALPHA:
    extra_sampling_mask = 'alpha'
  elif scene.getRenderParameter('EXTRA SAMPLING MASK')[0] == EXTRA_SAMPLING_USER_BITMAP:
    extra_sampling_mask = 'bitmap'
  else:
    extra_sampling_mask = 'unknown'
  
  extra_sampling_level = scene.getRenderParameter('EXTRA SAMPLING SL')[0]
  extra_sampling_custom_alpha = scene.getRenderParameter('EXTRA SAMPLING CUSTOM ALPHA')[0]
  extra_sampling_bitmap = scene.getRenderParameter('EXTRA SAMPLING USER BITMAP')[0]
  extra_sampling_invert_mask = "on" if scene.getRenderParameter('EXTRA SAMPLING INVERT')[0] else "off"
  
  # Channels
  # channels_output_mode = 'embedded'
  
  channels_render_layers = ''
  if scene.getRenderParameter('RENDER LAYERS')[0] == RENDER_LAYER_ALL:
    # RENDER_LAYER_ALL (all layers)
    channels_render_layers = 'all'
  elif scene.getRenderParameter('RENDER LAYERS')[0] == RENDER_LAYER_DIFFUSE:
    # RENDER_LAYER_DIFFUSE (diffuse)
    channels_render_layers = 'diffuse'
  elif scene.getRenderParameter('RENDER LAYERS')[0] == RENDER_LAYER_REFLECTIONS:
    # RENDER_LAYER_REFLECTIONS (reflections)
    channels_render_layers = 'reflections'
  elif scene.getRenderParameter('RENDER LAYERS')[0] == RENDER_LAYER_REFRACTIONS:
    # RENDER_LAYER_REFRACTIONS (refractions)
    channels_render_layers = 'refractions'
  elif scene.getRenderParameter('RENDER LAYERS')[0] == RENDER_LAYER_DIFFUSE_AND_REFLECTIONS:
    # RENDER_LAYER_DIFFUSE_AND_REFLECTIONS (diffuse and reflections)
    channels_render_layers = 'diffuse and reflections'
  elif scene.getRenderParameter('RENDER LAYERS')[0] == RENDER_LAYER_REFLECTIONS_AND_REFRACTIONS:
    # RENDER_LAYER_REFLECTIONS_AND_REFRACTIONS (reflections and refractions)
    channels_render_layers = 'reflections and refractions'
  else:
    # Fallback Unknown state
    channels_render_layers = 'unknown'
    
  channels_render = "on" if scene.getRenderParameter('DO RENDER CHANNEL')[0] else "off"
  channels_alpha = "on" if scene.getRenderParameter('DO ALPHA CHANNEL')[0] else "off"
  channels_opaque = "on" if scene.getRenderParameter('DO OPAQUE ALPHA')[0] else "off"
  channels_zbuffer = "on" if scene.getRenderParameter('DO ZBUFFER CHANNEL')[0] else "off"
  
  # print('[***ZBUFFER RANGE*** TUPPLE]' + str(scene.getRenderParameter('ZBUFFER RANGE')[0]))
  # channels_zbuffer_meters = "1.0 1.0"
  
  channels_shadow = "on" if scene.getRenderParameter('DO SHADOW PASS CHANNEL')[0] else "off"
  channels_material_id = "on" if scene.getRenderParameter('DO IDMATERIAL CHANNEL')[0] else "off"
  channels_object_id = "on" if scene.getRenderParameter('DO IDOBJECT CHANNEL')[0] else "off"
  channels_motion_vector = "on" if scene.getRenderParameter('DO MOTION CHANNEL')[0] else "off"
  channels_roughness = "on" if scene.getRenderParameter('DO ROUGHNESS CHANNEL')[0] else "off"
  channels_fresnel = "on" if scene.getRenderParameter('DO FRESNEL CHANNEL')[0] else "off"
  channels_normals = "on" if scene.getRenderParameter('DO NORMALS CHANNEL')[0] else "off"
  channels_normals_mode = "camera" if scene.getRenderParameter('NORMALS CHANNEL SPACE')[0] else "world"
  channels_position = "on" if scene.getRenderParameter('DO POSITION CHANNEL')[0] else "off"
  channels_position_mode = "camera" if scene.getRenderParameter('POSITION CHANNEL SPACE')[0] else "world"
  channels_motion_type = "reelsmart" if scene.getRenderParameter('MOTION CHANNEL TYPE')[0] else "other"
  channels_deep = "on" if scene.getRenderParameter('DO DEEP CHANNEL')[0] else "off"
  channels_deep_mode = "rgba" if scene.getRenderParameter('DEEP CHANNEL TYPE')[0] else "alpha"
  channels_deep_min_distance = scene.getRenderParameter('DEEP MIN DISTANCE')[0]
  #channels_deep_max_samples = scene.getRenderParameter('DEEP MAX SAMPLES')[0]
  channels_uv = "on" if scene.getRenderParameter('DO UV CHANNEL')[0] else "off"
  channels_custom_alpha = "on" if scene.getRenderParameter('DO ALPHA CUSTOM CHANNEL')[0] else "off"
  channels_reflectance = "on" if scene.getRenderParameter('DO REFLECTANCE CHANNEL')[0] else "off"

  # Tone Mapping
  tone_mapping_color_space = b2a_getColorSpace(scene)
  tone_mapping_white_point,tone_mapping_tint,ok = scene.getWhitePoint()
  tone_mapping_monitor_gamma,tone_mapping_burn,ok = scene.getToneMapping()
  # tone_mapping_sharpness_enabled = 'off'
  # tone_mapping_sharpness = 60.0

  # Simulens
    
  #isEnabled,simulens_diffraction,simulens_frequency,simulens_aperture_map,simulens_obstacle_map,ok = scene.getDiffraction()
  # simulens_aperture_map = ''
  # simulens_obstacle_map = ''
  # simulens_diffraction = 1250.0
  # simulens_frequency = 1250.0
  # simulens_scattering = 250.0
  # simulens_devingetting = 100.0

  # Illumination and Caustics
  # illumination = 'Both'
  # reflection_caustics = 'Both'
  # refraction_caustics = 'Both'

  # Fire
  # fire_floating_shadows = 'off'
  # fire_floating_refractions = 'off'

  # Overlay Text
  # overlay_text = ''
  # overlay_text_position = ''
  # overlay_text_color = '1.0 1.0 1.0'
  # overlay_text_background = '0.0 0.0 0.0'
  

  # Check the OS time
  now = datetime.datetime.now()
  
  # Check the OS Platform
  mxPlatform = b2a_getPlatform()
  # print('Running on ' + mxPlatform + '\n')
  
  # Maxwell Release number - like "3.2.0.2"
  mxVersion = getPyMaxwellVersion()
  
  # Add the Maxwell ASCII header text
  textDocument += '# Maxwell ASCII Scene v' + b2a_version + '\n'
  textDocument += '# Generated: ' + now.strftime('%Y-%m-%d %H:%M:%S %p') + '\n'
  textDocument += '# Source MXS: ' + mxsFilePath + '\n'
  textDocument += '# Using: Maxwell ' + mxVersion + ' on ' + mxPlatform + '\n\n'
  
  # Indent spacer - either a tab or two spaces
  # indent = '\t'
  indent = '  '
  
  
  # Add the render_options section
  textDocument += 'render_options\n'
  textDocument += '{\n'
  textDocument += indent + 'active_camera "' + str(active_camera) + '"\n'
  textDocument += indent + 'time_limit ' + str(time_limit) + '\n'
  textDocument += indent + 'sampling_level ' + str(sampling_level) + '\n'
  textDocument += indent + 'multilight "' + str(multilight) + '"\n'
  textDocument += indent + 'multilight_output "' + str(multilight_output) + '"\n'
  textDocument += indent + 'cpu_threads ' + str(cpu_threads) + '\n'
  # textDocument += indent + 'priority "' + str(priority) + '"\n'
  textDocument += indent + 'quality "' + str(quality) + '"\n'
  # textDocument += indent + 'command_line "' + str(command_line) + '"\n'

  textDocument += indent + 'depth ' + str(depth) + '\n'
  textDocument += indent + 'image "' + str(image) + '"\n'
  textDocument += indent + 'mxi "' + str(mxi) + '"\n'

  textDocument += indent + 'materials_override_enable ' + str(materials_override_enable) + '\n'
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

  #textDocument += indent + 'channels_output_mode "' + str(channels_output_mode) + '"\n'
  textDocument += indent + 'channels_render_layers "' + str(channels_render_layers) + '"\n'
  textDocument += indent + 'channels_render ' + str(channels_render) + '\n'
  textDocument += indent + 'channels_alpha ' + str(channels_alpha) + '\n'
  textDocument += indent + 'channels_opaque ' + str(channels_opaque) + '\n'
  textDocument += indent + 'channels_zbuffer ' + str(channels_zbuffer) + '\n'
  # textDocument += indent + 'channels_zbuffer_meters ' + str(channels_zbuffer_meters) + '\n'
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
  textDocument += indent + 'channels_deep_min_distance ' + str(channels_deep_min_distance) + '\n'
  #textDocument += indent + 'channels_deep_max_samples ' + str(channels_deep_max_samples) + '\n'
  textDocument += indent + 'channels_uv ' + str(channels_uv) + '\n'
  textDocument += indent + 'channels_custom_alpha ' + str(channels_custom_alpha) + '\n'
  textDocument += indent + 'channels_reflectance ' + str(channels_reflectance) + '\n'

  textDocument += indent + 'tone_mapping_color_space "' + str(tone_mapping_color_space) + '"\n'
  textDocument += indent + 'tone_mapping_white_point ' + str(tone_mapping_white_point) + '\n'
  textDocument += indent + 'tone_mapping_tint ' + str(tone_mapping_tint) + '\n'
  textDocument += indent + 'tone_mapping_burn ' + str(tone_mapping_burn) + '\n'
  textDocument += indent + 'tone_mapping_monitor_gamma ' + str(tone_mapping_monitor_gamma) + '\n'
  # textDocument += indent + 'tone_mapping_sharpness_enabled ' + str(tone_mapping_sharpness_enabled) + '\n'
  # textDocument += indent + 'tone_mapping_sharpness ' + str(tone_mapping_sharpness) + '\n'

  # textDocument += indent + 'simulens_aperture_map ' + str(simulens_aperture_map) + '\n'
  # textDocument += indent + 'simulens_obstacle_map ' + str(simulens_obstacle_map) + '\n'
  # textDocument += indent + 'simulens_diffraction ' + str(simulens_diffraction) + '\n'
  # textDocument += indent + 'simulens_frequency ' + str(simulens_frequency) + '\n'
  # textDocument += indent + 'simulens_scattering ' + str(simulens_scattering) + '\n'
  # textDocument += indent + 'simulens_devingetting ' + str(simulens_devingetting) + '\n'
  # textDocument += indent + 'simulens_devingetting ' + str(simulens_devingetting) + '\n'

  # textDocument += indent + 'illumination "' + str(illumination) + '"\n'
  # textDocument += indent + 'reflection_caustics "' + str(reflection_caustics) + '"\n'
  # textDocument += indent + 'refraction_caustics "' + str(refraction_caustics) + '"\n'

  # textDocument += indent + 'fire_floating_shadows ' + str(fire_floating_shadows) + '\n'
  # textDocument += indent + 'fire_floating_refractions ' + str(fire_floating_refractions) + '\n'

  # textDocument += indent + 'overlay_text ' + str(overlay_text) + '\n'
  # textDocument += indent + 'overlay_text_position ' + str(overlay_text_position) + '\n'
  # textDocument += indent + 'overlay_text_color ' + str(overlay_text_color) + '\n'
  # textDocument += indent + 'overlay_text_background ' + str(overlay_text_background) + '\n'
  
  # Close the render_options section
  textDocument += '}\n'
  
  # -------------------------------------------------------
  # Write the ASCII text format scene to disk
  # -------------------------------------------------------
  asciiExt = 'mxa'
  asciiSceneFilename = scenePathNoExt + '.' + asciiExt

  print('[Maxwell ASCII Scene] ' + os.path.basename(asciiSceneFilename))
  print('[Document Contents] \n' + textDocument)

  asciiFile = open(asciiSceneFilename, 'w')
  ok = asciiFile.write(textDocument)
  asciiFile.close
  
  if ok == 0:
    print('\n--------------------------------------')
    print('[There was an error saving] ' + asciiSceneFilename)
    return 0
  else:
    print('\n--------------------------------------')
    print('[ASCII Scene Export Complete]')
    return 1


# Check the operating system
# Example: mxPlatform = b2a_getPlatform()
def b2a_getPlatform():
  import platform

  osPlatform = str(platform.system())

  mxPlatform = ''
  if osPlatform == 'Windows':
    mxPlatform = 'Windows'
  elif osPlatform == 'win32':
    mxPlatform = 'Windows'
  elif osPlatform == 'Darwin':
   mxPlatform = "Mac"
  elif osPlatform== 'Linux':
    mxPlatform =  'Linux'
  elif osPlatform == 'Linux2':
    mxPlatform = 'Linux'
  else:
    mxPlatform = 'Linux'
  
  # print('Running on ' + mxPlatform + '\n')
  return mxPlatform


# Get the Color Space
# Example: scene = Cmaxwell(mwcallback); colorSpace = b2a_getColorSpace(scene)
def b2a_getColorSpace(scene):
  colorSpace = ''

  colorSpaceValue = scene.getColorSpace()
  if colorSpaceValue == COLOR_SPACE_SRGB:
    colorSpace = 'sRGB IEC61966-2.1'
  elif colorSpaceValue == COLOR_SPACE_ADOBE98:
    colorSpace = 'Adobe RGB'
  elif colorSpaceValue == COLOR_SPACE_APPLE:
    colorSpace = 'Apple RGB'
  elif colorSpaceValue == COLOR_SPACE_PAL:
    colorSpace = 'PAL'
  elif colorSpaceValue == COLOR_SPACE_NTSC:
    colorSpace = 'NTSC 1953'
  elif colorSpaceValue == COLOR_SPACE_NTSC1979:
    colorSpace = 'NSTC 1979'
  elif colorSpaceValue == COLOR_SPACE_WIDEGAMUT:
    colorSpace = 'Wide Gamut RGB'
  elif colorSpaceValue == COLOR_SPACE_PROPHOTO:
    colorSpace = 'Pro Photo RGB'
  elif colorSpaceValue == COLOR_SPACE_ECIRRGB:
    colorSpace = 'ECI RGB'
  elif colorSpaceValue == COLOR_SPACE_CIE1931:
    colorSpace = 'CIE 1931'
  elif colorSpaceValue == COLOR_SPACE_BRUCERGB:
    colorSpace = 'Bruce RGB'
  elif colorSpaceValue == COLOR_SPACE_COLORMATCH:
    colorSpace = 'ColorMatch RGB'
  elif colorSpaceValue == COLOR_SPACE_BESTRGB:
    colorSpace = 'Best RGB'
  elif colorSpaceValue == COLOR_SPACE_DONRGB4:
    colorSpace = 'Don RGB 4'
  elif colorSpaceValue == COLOR_SPACE_REC709:
    colorSpace = 'REC.709'
  elif colorSpaceValue == COLOR_SPACE_ACES:
    colorSpace = 'ACES'
  elif colorSpaceValue == COLOR_SPACE_UNKNOWN:
    colorSpace = 'unknown'
  else:
    colorSpace = 'unknown'

  print('[Color Space] ' + str(colorSpace))

  return colorSpace

# Get the Color Temperature
# Example: scene = Cmaxwell(mwcallback); colorTemperature = b2a_getColorTemperature(scene)
def b2a_getColorTemperature(scene):
  colorTemperatureValue =  scene.getCorrelatedcolorTemperature()

  print('[Color Temperature] ' + str(colorTemperatureValue))

  return colorTemperatureValue

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
  	ok = b2a_writeAsciiScene(mxsFilePath,)
  else:
    print('[MXS File Not Found] ' + mxsFilePath)


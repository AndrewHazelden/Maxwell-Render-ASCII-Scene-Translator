# Maxwell MXS to ASCII Translator
# --------------------------------------------
# 2015-12-13 14.06 PM v0.1.2
# By Andrew Hazelden 
# Email: andrew@andrewhazelden.com
# Blog: http://www.andrewhazelden.com

# Description
# -----------
# This tool will convert a binary format Maxwell Render MXS scene file into a plain text ASCII format that is easier for a rendering TD to review and edit.


# Script Installation
# -------------------
# Copy the mxs2ascii.py python file to your Maxwell 3.2 scripts directory:

# Windows
# C:/Program Files/Next Limit/Maxwell 3/scripts/

# Linux
# /opt/maxwell-3.2/scripts/
# or
# $home/maxwell64-3.2/scripts/

# Mac
# /Applications/Maxwell 3/scripts/


# How do I use the script?
# ------------------------

# Step 1.
# Launch PyMaxwell and open up the `mxs2ascii.py` python script.

# Step 2. Choose if you want to process a single MXS or a directory filled with of MXS files.

# Process a Single MXS File
# If you want to process a single MXS file edit the "mxsFilePath" variable in the main function near the bottom of this script and specify your Maxwell Studio based MXS scene file.

# Then uncomment the code block just below to the section "# Process a single MXS File". Then add python based `#` number sign comments at the beginning of the lines in the "# Or process a whole directory of MXS files" section of code.

# Process a Whole Directory of MXS Files

# If you want to automatically process an entire folder filled with MXS files then you should edit the "mxsDirPath" to specify the folder location that holds your Maxwell Studio based MXS scene files.

# Make sure the code block just below to the section "# Process a single MXS File" is commented with python based `#` number sign comments at the beginning of each of the lines.

# Then you might need to uncomment the code block lines just below the "# Or process a whole directory of MXS files" section of code.

# Step 3. Select the Script > Run menu item in PyMaxwell.

# The script will start running. First the script will verify the mxs scene file exists.

# Then the scene will be opened in Maxwell and the scene elements and parameters will be exported to an ASCII text document with the name of `<scene>.mxa`. This new file is saved to the same folder as the original mxs scene file.


# -----------------------------------------

from pymaxwell import *
from math import *
import os
import sys
import datetime

# Write the Maxell Ascii Scene to Disk
# Example: writeAsciiScene('/Cube.mas')
def mxa_writeAsciiScene(mrt_version, mxsFilePath):
  
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
  print('[Input Scene] ' + sceneName + ' [Active Camera] ' + str(cameraName) + ' [Resolution] ' + str(width) + 'x' + str(height))

  # Check the OS time
  now = datetime.datetime.now()
  
  # Check the OS Platform
  mxPlatform = mrt_getPlatform()
  # print('Running on ' + mxPlatform + '\n')
  
  # Maxwell Release number - like "3.2.0.2"
  mxVersion = getPyMaxwellVersion()
  
  # Add the Maxwell ASCII header text
  textDocument = ''
  textDocument += '# Maxwell ASCII Scene v' + mrt_version + '\n'
  textDocument += '# Generated: ' + now.strftime('%Y-%m-%d %H:%M:%S %p') + '\n'
  textDocument += '# Source MXS: ' + mxsFilePath + '\n'
  textDocument += '# Using: Maxwell ' + mxVersion + ' on ' + mxPlatform + '\n\n'
  
  # Indent spacer - either a tab or two spaces
  # indent = '\t'
  indent = '  '
  
  # Add the render_options section
  textDocument += mxa_getRenderOptionsBlock(scene)
  
  # Add the camera section
  textDocument += mxa_getCameraBlock(scene)
  
  # Add the environment section
  textDocument += mxa_getEnvironmentBlock(scene)
  
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
    print('[ASCII Scene Export Complete] ' + asciiSceneFilename)
    return 1


# Check the operating system
# Example: mxPlatform = mrt_getPlatform()
def mrt_getPlatform():
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


# Get the Render Options
# Example: scene = Cmaxwell(mwcallback); renderOptionsText = mxa_getRenderOptionsBlock(scene)
def mxa_getRenderOptionsBlock(scene):
  camera = scene.getActiveCamera()
  cameraName = camera.getName()
  active_camera = cameraName
  
  # MXS Scene Render Option Values
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
  
  # Search Paths
  # TODO -  Translate the "materials_search_path" array results: (['/Applications/Maxwell 3/scripts/stereo/', '/Applications/Maxwell 3/materials database/textures/', '/Applications/Maxwell 3/materials database/ies/', '/Applications/Maxwell 3/materials database/iors/', 'C:/Program Files/Next Limit/Maxwell 3/scripts/stereo/', 'C:\\Program Files\\Next Limit\\Maxwell 3\\scripts\\stereo\\', 'C:\\Program Files\\Next Limit\\Maxwell 3\\materials database\\textures\\', 'C:\\Program Files\\Next Limit\\Maxwell 3\\materials database\\ies\\', 'C:\\Program Files\\Next Limit\\Maxwell 3\\materials database\\iors\\', 'M:\\Render\\Maxwell\\LatLong_Stereo_CubeX_sep\\', 'M:\\Render\\Maxwell\\', 'C:\\Users\\Administrator\\Desktop\\maxwell_latlong_stereo_cubex\\', 'C:\\Users\\Administrator\\Desktop\\maxwell\\Maxwell_LatLong_Stereo_CubeX\\', 'C:\\', 'M:\\Render\\Maxwell\\Maxwell_Stereo_Projects\\mxs\\Maxwell_LatLong_Stereo_CubeX\\', 'M:\\Render\\Maxwell\\Maxwell_Stereo_Projects\\mxs\\Maxwell_LatLong_Stereo_CubeX_v9\\', 'C:/Users/Administrator/Desktop/maxwell/Maxwell_LatLong_Stereo_CubeX/'], 1)
  
  materials_search_path = ''
  #print '[Search Paths] ' + str(scene.getSearchingPaths()) + '\n'

  # Globals
  motion_blur = "on" if scene.getRenderParameter('DO MOTION BLUR')[0] else "off"
  displacement = "on" if scene.getRenderParameter('DO DISPLACEMENT')[0] else "off"
  dispersion = "on" if scene.getRenderParameter('DO DISPERSION')[0] else "off"

  # Extra Sampling
  extra_sampling_enabled = "on" if scene.getRenderParameter('DO EXTRA SAMPLING')[0] else "off"
  extra_sampling_level = scene.getRenderParameter('EXTRA SAMPLING SL')[0]
  
  extra_sampling_mask = ''
  if scene.getRenderParameter('EXTRA SAMPLING MASK')[0] == EXTRA_SAMPLING_CUSTOM_ALPHA:
    extra_sampling_mask = 'custom alpha'
  elif scene.getRenderParameter('EXTRA SAMPLING MASK')[0] == EXTRA_SAMPLING_ALPHA:
    extra_sampling_mask = 'alpha'
  elif scene.getRenderParameter('EXTRA SAMPLING MASK')[0] == EXTRA_SAMPLING_USER_BITMAP:
    extra_sampling_mask = 'bitmap'
  else:
    extra_sampling_mask = 'unknown'
  
  extra_sampling_custom_alpha = scene.getRenderParameter('EXTRA SAMPLING CUSTOM ALPHA')[0]
  extra_sampling_bitmap = scene.getRenderParameter('EXTRA SAMPLING USER BITMAP')[0]
  extra_sampling_invert_mask = "on" if scene.getRenderParameter('EXTRA SAMPLING INVERT')[0] else "off"
  
  # Channels
  channels_output_mode = "embedded" if scene.getRenderParameter('EMBED CHANNELS')[0] else "separate"
  #print '[channels_output_mode] ' + channels_output_mode + ' ' + str(scene.getRenderParameter('EMBED CHANNELS')[0])


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
  channels_opaque = "on" if scene.getRenderParameter('OPAQUE ALPHA')[0] else "off"
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
  channels_motion_mode = "other" if scene.getRenderParameter('MOTION CHANNEL TYPE')[0] else "reelsmart"
  channels_deep = "on" if scene.getRenderParameter('DO DEEP CHANNEL')[0] else "off"
  channels_deep_mode = "rgba" if scene.getRenderParameter('DEEP CHANNEL TYPE')[0] else "alpha"
  channels_deep_min_distance = scene.getRenderParameter('DEEP MIN DISTANCE')[0]
  ##channels_deep_max_samples = scene.getRenderParameter('DEEP MAX SAMPLES')[0]
  channels_uv = "on" if scene.getRenderParameter('DO UV CHANNEL')[0] else "off"
  channels_custom_alpha = "on" if scene.getRenderParameter('DO ALPHA CUSTOM CHANNEL')[0] else "off"
  channels_reflectance = "on" if scene.getRenderParameter('DO REFLECTANCE CHANNEL')[0] else "off"

  # Tone Mapping
  tone_mapping_color_space = mxa_getColorSpace(scene)
  tone_mapping_white_point,tone_mapping_tint,ok = scene.getWhitePoint()
  tone_mapping_monitor_gamma,tone_mapping_burn,ok = scene.getToneMapping()
  tone_mapping_sharpness_enabled = "on" if scene.getRenderParameter('DO SHARPNESS')[0] else "off"
  tone_mapping_sharpness = scene.getRenderParameter('SHARPNESS')[0]

  # Simulens
    
  #isEnabled,simulens_diffraction,simulens_frequency,simulens_aperture_map,simulens_obstacle_map,ok = scene.getDiffraction()
  # simulens_aperture_map = ''
  # simulens_obstacle_map = ''
  # simulens_diffraction = 1250.0
  # simulens_frequency = 1250.0
  simulens_scattering_enabled = "on" if scene.getRenderParameter('DO SCATTERING_LENS')[0] else "off"
  # Note the Maxwell Studio GUI settings - If "Scattering" is set to 2500 then SCATTERING_LENS=1.0
  simulens_scattering = scene.getRenderParameter('SCATTERING_LENS')[0]
  simulens_devingetting_enabled = "on" if scene.getRenderParameter('DO DEVIGNETTING')[0] else "off"
  simulens_devingetting = scene.getRenderParameter('DEVIGNETTING')[0]

  # Illumination and Caustics
  # illumination = 'Both'
  # reflection_caustics = 'Both'
  # refraction_caustics = 'Both'

  # Fire
  fire_floating_shadows = "on" if scene.getRenderParameter('DO FLOATING SHADOWS')[0] else "off"
  fire_floating_refractions = "on" if scene.getRenderParameter('DO FLOATING REFLECTIONS')[0] else "off"

  # Overlay Text
  # overlay_text = 1.0
  # overlay_text_position = ''
  # overlay_text_color = '1.0 1.0 1.0'
  # overlay_text_background = '0.0 0.0 0.0'
  
  # -----------------------------------------------------------------
  
  # Indent spacer - either a tab or two spaces
  # indent = '\t'
  indent = '  '
  
  # Add the render_options section
  textDocument = ''
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
  textDocument += indent + 'extra_sampling_level ' + str(extra_sampling_level) + '\n'
  textDocument += indent + 'extra_sampling_mask "' + str(extra_sampling_mask) + '"\n'
  textDocument += indent + 'extra_sampling_custom_alpha "' + str(extra_sampling_custom_alpha) + '"\n'
  textDocument += indent + 'extra_sampling_bitmap "' + str(extra_sampling_bitmap) + '"\n'
  textDocument += indent + 'extra_sampling_invert_mask ' + str(extra_sampling_invert_mask) + '\n'

  textDocument += indent + 'channels_output_mode "' + str(channels_output_mode) + '"\n'
  textDocument += indent + 'channels_render_layers "' + str(channels_render_layers) + '"\n'
  textDocument += indent + 'channels_render ' + str(channels_render) + '\n'
  textDocument += indent + 'channels_alpha ' + str(channels_alpha) + '\n'
  textDocument += indent + 'channels_opaque ' + str(channels_opaque) + '\n'
  textDocument += indent + 'channels_zbuffer ' + str(channels_zbuffer) + '\n'
  ## textDocument += indent + 'channels_zbuffer_meters ' + str(channels_zbuffer_meters) + '\n'
  textDocument += indent + 'channels_shadow ' + str(channels_shadow) + '\n'
  textDocument += indent + 'channels_material_id ' + str(channels_material_id) + '\n'
  textDocument += indent + 'channels_object_id ' + str(channels_object_id) + '\n'
  textDocument += indent + 'channels_motion_vector ' + str(channels_motion_vector) + '\n'
  textDocument += indent + 'channels_roughness ' + str(channels_roughness) + '\n'
  textDocument += indent + 'channels_fresnel ' + str(channels_fresnel) + '\n'
  textDocument += indent + 'channels_normals ' + str(channels_normals) + '\n'
  textDocument += indent + 'channels_normals_mode "' + str(channels_normals_mode) + '"\n'
  textDocument += indent + 'channels_motion_mode "' + str(channels_motion_mode) + '"\n'
  textDocument += indent + 'channels_position ' + str(channels_position) + '\n'
  textDocument += indent + 'channels_position_mode "' + str(channels_position_mode) + '"\n'
  textDocument += indent + 'channels_deep ' + str(channels_deep) + '\n'
  textDocument += indent + 'channels_deep_mode "' + str(channels_deep_mode) + '"\n'
  textDocument += indent + 'channels_deep_min_distance ' + str(channels_deep_min_distance) + '\n'
  ##textDocument += indent + 'channels_deep_max_samples ' + str(channels_deep_max_samples) + '\n'
  textDocument += indent + 'channels_uv ' + str(channels_uv) + '\n'
  textDocument += indent + 'channels_custom_alpha ' + str(channels_custom_alpha) + '\n'
  textDocument += indent + 'channels_reflectance ' + str(channels_reflectance) + '\n'

  textDocument += indent + 'tone_mapping_color_space "' + str(tone_mapping_color_space) + '"\n'
  textDocument += indent + 'tone_mapping_white_point ' + str(tone_mapping_white_point) + '\n'
  textDocument += indent + 'tone_mapping_tint ' + str(tone_mapping_tint) + '\n'
  textDocument += indent + 'tone_mapping_burn ' + str(tone_mapping_burn) + '\n'
  textDocument += indent + 'tone_mapping_monitor_gamma ' + str(tone_mapping_monitor_gamma) + '\n'
  
  textDocument += indent + 'tone_mapping_sharpness_enabled ' + str(tone_mapping_sharpness_enabled) + '\n'
  # Note the Maxwell Studio GUI if "Sharpness" is set to 100 then tone_mapping_sharpness=1.0
  textDocument += indent + 'tone_mapping_sharpness ' + str(tone_mapping_sharpness) + '\n'

  # textDocument += indent + 'simulens_aperture_map ' + str(simulens_aperture_map) + '\n'
  # textDocument += indent + 'simulens_obstacle_map ' + str(simulens_obstacle_map) + '\n'
  # textDocument += indent + 'simulens_diffraction ' + str(simulens_diffraction) + '\n'
  # textDocument += indent + 'simulens_frequency ' + str(simulens_frequency) + '\n'
  textDocument += indent + 'simulens_scattering_enabled ' + str(simulens_scattering_enabled) + '\n'
  textDocument += indent + 'simulens_scattering ' + str(simulens_scattering) + '\n'
  textDocument += indent + 'simulens_devingetting_enabled ' + str(simulens_devingetting_enabled) + '\n'
  textDocument += indent + 'simulens_devingetting ' + str(simulens_devingetting) + '\n'

  # textDocument += indent + 'illumination "' + str(illumination) + '"\n'
  # textDocument += indent + 'reflection_caustics "' + str(reflection_caustics) + '"\n'
  # textDocument += indent + 'refraction_caustics "' + str(refraction_caustics) + '"\n'

  textDocument += indent + 'fire_floating_shadows ' + str(fire_floating_shadows) + '\n'
  textDocument += indent + 'fire_floating_refractions ' + str(fire_floating_refractions) + '\n'

  # textDocument += indent + 'overlay_text ' + str(overlay_text) + '\n'
  # textDocument += indent + 'overlay_text_position ' + str(overlay_text_position) + '\n'
  # textDocument += indent + 'overlay_text_color ' + str(overlay_text_color) + '\n'
  # textDocument += indent + 'overlay_text_background ' + str(overlay_text_background) + '\n'
  
  # Close the render_options section
  textDocument += '}\n'
  textDocument += '\n'
  
  return textDocument


# Get the Camera
# Example: scene = Cmaxwell(mwcallback); cameraText = mxa_getCameraBlock(scene)
def mxa_getCameraBlock(scene):
  camera = scene.getActiveCamera()
  name = camera.getName()
  camera_lens = camera.getLensType()
    
  # The camera's render resolution
  res = camera.getResolution()
  width = res[0]
  height = res[1]
  resolution = str(width) + ' ' + str(height)
  
  # Cropped Screen Render Region
  x1,y1,x2,y2,render_region_mode_raw,ok = camera.getScreenRegion()
  #render_region = "0 0 " + str(width) + ' ' + str(height)
  render_region = str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2)
  
  render_region_mode = ''
  if render_region_mode_raw == 'REGION':
    render_region_mode = 'region'
  elif render_region_mode_raw == 'BLOW UP':
    render_region_mode = 'blow up'
  else:
    render_region_mode = 'unknown'
  
  position_raw,target_raw,up_raw,focal_length_raw,f_stop,step_time,ok = camera.getStep(0)
  position = str(round(position_raw[0],3)) + ' ' + str(round(position_raw[1],3)) + ' ' + str(round(position_raw[2],3))
  target = str(round(target_raw[0],3)) + ' ' + str(round(target_raw[1],3)) + ' ' + str(round(target_raw[2],3))
  up = str(round(up_raw[0],3)) + ' ' + str(round(up_raw[1],3)) + ' ' + str(round(up_raw[2],3))
  roll_angle = 0.0
  lens = mxa_lensTypeName(camera_lens)
  focal_length = round((focal_length_raw * 1000.0), 0)
  #lock_exposure = "off"
  shutter = camera.getShutter()[0]
  #ev_number = 0
  filmWidthRaw,filmHeightRaw,ok = camera.getFilmSize()
  film_width = round((filmWidthRaw * 1000.0), 1)
  film_height = round((filmHeightRaw * 1000.0), 1)
  iso = camera.getIso()[0]
  
  diaphragm_mode_raw,angle,blades,ok = camera.getDiaphragm()
  diaphragm_mode = ''
  if diaphragm_mode_raw == 'CIRCULAR':
    diaphragm_mode = 'circular'
  elif diaphragm_mode_raw == 'POLYGONAL':
    diaphragm_mode = 'polygonal'
  else:
    diaphragm_mode = 'unknown'
     
  fps = camera.getFPS()[0]
  pixel_aspect = camera.getPixelAspect()[0]
  x_shift,y_shift,ok = camera.getShiftLens()
  hidden =  "on" if camera.isHide()[0] else "off"
  
  z_near_clip_plane,z_far_clip_plane,z_clip_planes_enabled_raw,ok = camera.getCutPlanes()
  z_clip_planes_enabled = "on" if z_clip_planes_enabled_raw else "off"
  
  # print "[nSteps] " + str(nSteps) + "\n"
  
  # Indent spacer - either a tab or two spaces
  # indent = '\t'
  indent = '  '
  
  # Add the camera section
  textDocument = ''
  textDocument += 'camera\n'
  textDocument += '{\n'
  
  textDocument += indent + 'name "' + str(name) + '"\n'
  textDocument += indent + 'position ' + str(position) + '\n'
  textDocument += indent + 'target ' + str(target) + '\n'
  textDocument += indent + 'up ' + str(up) + '\n'
  textDocument += indent + 'resolution ' + str(resolution) + '\n'
  textDocument += indent + 'render_region ' + str(render_region) + '\n'
  textDocument += indent + 'render_region_mode "' + str(render_region_mode) + '"\n'
  textDocument += indent + 'lens "' + str(lens) + '"\n'
  textDocument += indent + 'focal_length ' + str(focal_length) + '\n'
  #textDocument += indent + 'lock_exposure ' + str(lock_exposure) + '\n'
  textDocument += indent + 'shutter ' + str(shutter) + '\n'
  textDocument += indent + 'f_stop ' + str(f_stop) + '\n'
  #textDocument += indent + 'ev_number ' + str(ev_number) + '\n'
  textDocument += indent + 'iso ' + str(iso) + '\n'
  textDocument += indent + 'film_width ' + str(film_width) + '\n'
  textDocument += indent + 'film_height ' + str(film_height) + '\n'
  textDocument += indent + 'diaphragm_mode "' + str(diaphragm_mode) + '"\n'
  textDocument += indent + 'blades ' + str(blades) + '\n'
  textDocument += indent + 'fps ' + str(fps) + '\n'
  textDocument += indent + 'step_time ' + str(step_time) + '\n'
  textDocument += indent + 'pixel_aspect ' + str(pixel_aspect) + '\n'
  textDocument += indent + 'x_shift ' + str(x_shift) + '\n'
  textDocument += indent + 'y_shift ' + str(y_shift) + '\n'
  textDocument += indent + 'z_clip_planes_enabled ' + str(z_clip_planes_enabled) + '\n'
  textDocument += indent + 'z_near_clip_plane ' + str(z_near_clip_plane) + '\n'
  textDocument += indent + 'z_far_clip_plane ' + str(z_far_clip_plane) + '\n'
  textDocument += indent + 'hidden ' + str(hidden) + '\n'
  
  # Close the camera section
  textDocument += '}\n'
  textDocument += '\n'
  return textDocument

# Get the Environment
# Example: scene = Cmaxwell(mwcallback); environmentText = mxa_getEnvironmentBlock(scene)
def mxa_getEnvironmentBlock(scene):
  camera = scene.getActiveCamera()
  enviro = scene.getEnvironment()
  
  sky_type_raw = str(enviro.getActiveSky())
  #print '[sky_mode_raw] ' + str(sky_type_raw)
  
  sky_type = ''
  if sky_type_raw == 'None':
    sky_type = 'none'
  elif sky_type_raw == 'CONSTANT':
    sky_type = 'constant'
  elif sky_type_raw == 'PHYSICAL':
    sky_type = 'physical'
  else:
   sky_type = 'unknown'

  # Physical Sky
  intensity,ozone,water,turbidity_coefficient,wavelength_exponent,reflectance,asymmetry,planet_reflecton,ok = enviro.getPhysicalSkyAtmosphere()

  # Sun
  sun_type_raw,sun_temperature,sun_power,sun_radius_factor,constantColor,ok = enviro.getSunProperties()
  sun_color = str(constantColor[0]) + ' ' + str(constantColor[1]) + ' ' + str(constantColor[2])
  
  sun_type = ''
  if sun_type_raw == SUN_DISABLED:
    sun_type = 'none'
  elif sun_type_raw == SUN_PHYSICAL:
    sun_type = 'physical'
  elif sun_type_raw == SUN_CONSTANT:
    sun_type = 'constant'
  else:
   sun_type = 'unknown'
  
  # print '[sun_color] ' + str(sun_color)

  # Ground Rotation comes back as radians - We are going to store it in degrees for simplicity
  ground_rotation_radians,ok = enviro.getSunRotation()
  ground_rotation = ground_rotation_radians * (180/pi)
  
  # Sun location and time of year
  longitude,latitude,gmt,day_of_year,time_of_day,ok = enviro.getSunLongitudeAndLatitude()
  
  # IBL Lighting
  # With getEnvironmentLayer(layerType) the layerType is set to either: IBL_LAYER_BACKGROUND, IBL_LAYER_REFLECTION, IBL_LAYER_REFRACTION, or IBL_LAYER_ILLUMINATION
  # Note The ibl_spherical_mapping option is un-used at this point
  # Note: That the ibl_screen_mapping option hasn't been extracted from the params yet
  
  background_map,background_type,ibl_spherical_mapping,interpolation,background_intensity,u_tile,v_tile,u_tile_offset,v_tile_offset,ok = enviro.getEnvironmentLayer(IBL_LAYER_BACKGROUND)
  background_scale = str(u_tile) + ' ' + str(v_tile)
  background_offset = str(u_tile_offset) + ' ' + str(v_tile_offset)
    
  reflection_map,reflection_type,ibl_spherical_mapping,interpolation,reflection_intensity,u_tile,v_tile,u_tile_offset,v_tile_offset,ok = enviro.getEnvironmentLayer(IBL_LAYER_REFLECTION)
  reflection_scale = str(u_tile) + ' ' + str(v_tile)
  reflection_offset = str(u_tile_offset) + ' ' + str(v_tile_offset)
  
  refraction_map,refraction_type,ibl_spherical_mapping,interpolation,refraction_intensity,u_tile,v_tile,u_tile_offset,v_tile_offset,ok = enviro.getEnvironmentLayer(IBL_LAYER_REFRACTION)
  refraction_scale = str(u_tile) + ' ' + str(v_tile)
  refraction_offset = str(u_tile_offset) + ' ' + str(v_tile_offset)

  illumination_map,illumination_type,ibl_spherical_mapping,interpolation,illumination_intensity,u_tile,v_tile,u_tile_offset,v_tile_offset,ok = enviro.getEnvironmentLayer(IBL_LAYER_ILLUMINATION)
  illumination_scale = str(u_tile) + ' ' + str(v_tile)
  illumination_offset = str(u_tile_offset) + ' ' + str(v_tile_offset)
  
  ibl_interpolation = "on" if interpolation else "off"
  
  ibl_intensity,ok = enviro.getEnvironmentWeight()

  # Indent spacer - either a tab or two spaces
  # indent = '\t'
  indent = '  '
  
  # Add the environment section
  textDocument = ''
  textDocument += 'environment\n'
  textDocument += '{\n'
  
  textDocument += indent + 'sky_type "' + str(sky_type) + '"\n'
  textDocument += indent + 'intensity ' + str(intensity) + '\n'
  textDocument += indent + 'planet_reflecton ' + str(planet_reflecton) + '\n'
  textDocument += indent + 'ozone ' + str(ozone) + '\n'
  textDocument += indent + 'water ' + str(water) + '\n'
  textDocument += indent + 'turbidity_coefficient ' + str(turbidity_coefficient) + '\n'
  textDocument += indent + 'wavelength_exponent ' + str(wavelength_exponent) + '\n'
  textDocument += indent + 'reflectance ' + str(reflectance) + '\n'
  textDocument += indent + 'asymmetry ' + str(asymmetry) + '\n'
  textDocument += indent + 'sun_type "' + str(sun_type) + '"\n'
  textDocument += indent + 'sun_power ' + str(sun_power) + '\n'
  textDocument += indent + 'sun_radius_factor ' + str(sun_radius_factor) + '\n'
  textDocument += indent + 'sun_temperature ' + str(sun_temperature) + '\n'
  textDocument += indent + 'sun_color ' + str(sun_color) + '\n'
#   textDocument += indent + 'location ' + str('') + '\n'
#   textDocument += indent + 'city "' + str('') + '"\n'
  textDocument += indent + 'latitude ' + str(latitude) + '\n'
  textDocument += indent + 'longitude ' + str(longitude) + '\n'
  textDocument += indent + 'day_of_year ' + str(day_of_year) + '\n'
  textDocument += indent + 'time_of_day ' + str(time_of_day) + '\n'
  textDocument += indent + 'gmt ' + str(gmt) + '\n'
  textDocument += indent + 'ground_rotation ' + str(ground_rotation) + '\n'
#   textDocument += indent + 'zenith ' + str('') + '\n'
#   textDocument += indent + 'horizon ' + str('') + '\n'
#   textDocument += indent + 'mid_point ' + str('') + '\n'
  textDocument += indent + 'ibl_intensity ' + str(ibl_intensity) + '\n'
  textDocument += indent + 'ibl_interpolation ' + str(ibl_interpolation) + '\n'
#   textDocument += indent + 'ibl_screen_mapping ' + str(ibl_screen_mapping) + '\n'
  textDocument += indent + 'background_type ' + str(background_type) + '\n'
  textDocument += indent + 'background_map "' + str(background_map) + '"\n'
  textDocument += indent + 'background_intensity ' + str(background_intensity) + '\n'
  textDocument += indent + 'background_scale ' + str(background_scale) + '\n'
  textDocument += indent + 'background_offset ' + str(background_offset) + '\n'
  textDocument += indent + 'reflection_type ' + str(reflection_type) + '\n'
  textDocument += indent + 'reflection_map "' + str(reflection_map) + '"\n'
  textDocument += indent + 'reflection_intensity ' + str(reflection_intensity) + '\n'
  textDocument += indent + 'reflection_scale ' + str(reflection_scale) + '\n'
  textDocument += indent + 'reflection_offset ' + str(reflection_offset) + '\n'
  textDocument += indent + 'refraction_type ' + str(refraction_type) + '\n'
  textDocument += indent + 'refraction_map "' + str(refraction_map) + '"\n'
  textDocument += indent + 'refraction_intensity ' + str(refraction_intensity) + '\n'
  textDocument += indent + 'refraction_scale ' + str(refraction_scale) + '\n'
  textDocument += indent + 'refraction_offset ' + str(refraction_offset) + '\n'
  textDocument += indent + 'illumination_type ' + str(illumination_type) + '\n'
  textDocument += indent + 'illumination_map "' + str(illumination_map) + '"\n'
  textDocument += indent + 'illumination_intensity ' + str(illumination_intensity) + '\n'
  textDocument += indent + 'illumination_scale ' + str(illumination_scale) + '\n'
  textDocument += indent + 'illumination_offset ' + str(illumination_offset) + '\n'

  # Close the environment section
  textDocument += '}\n'
  textDocument += '\n'
  return textDocument
  
# Get the Color Space
# Example: scene = Cmaxwell(mwcallback); colorSpace = mxa_getColorSpace(scene)
def mxa_getColorSpace(scene):
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

  # print('[Color Space] ' + str(colorSpace))

  return colorSpace
  
# Return the lens type name as a string
# Example: it = CmaxwellCameraIterator(); camera = it.first(scene); cameraLens = cameraParams.getLensType(); lens = mxa_lensTypeName(cameraLens)
def mxa_lensTypeName(cameraLens):

  lensTypeName = ''
  if cameraLens[0] == TYPE_CYLINDRICAL_LENS:
    lensTypeName = 'cylindrical'
  elif cameraLens[0] == TYPE_EXTENSION_LENS:
    lensTypeName = 'extension lens'
  elif cameraLens[0] == TYPE_FISHEYE_LENS:
    lensTypeName = 'fisheye'
  elif cameraLens[0] == TYPE_ORTHO_LENS:
    lensTypeName = 'ortho'
  elif cameraLens[0] == TYPE_PINHOLE_LENS:
    lensTypeName = 'pinhole'
  elif cameraLens[0] == TYPE_SPHERICAL_LENS:
    lensTypeName = 'spherical'
  elif cameraLens[0] == TYPE_THIN_LENS:
    lensTypeName = 'thin'

  return lensTypeName

# Get the Color Temperature
# Example: scene = Cmaxwell(mwcallback); colorTemperature = mxa_getColorTemperature(scene)
def mxa_getColorTemperature(scene):
  colorTemperatureValue =  scene.getCorrelatedcolorTemperature()

  print('[Color Temperature] ' + str(colorTemperatureValue))

  return colorTemperatureValue


# Open a folder window up using your desktop file browser
# Example: mrt_openDirectory('/Applications/')
def mrt_openDirectory(filenameNativePath):
  mxPlatform = mrt_getPlatform()
  
  # Convert a path to a file into a directory path
  dirName = ''
  if os.path.isfile(filenameNativePath):
    dirName = os.path.dirname(filenameNativePath)
  else:
    dirName = filenameNativePath
  
  # Check OS platform for Windows/Mac/Linux Paths
  if mxPlatform == 'Windows':
    dirName = dirName.replace("/","\\")
    # Check if the program is running on Windows 
    os.system('explorer "' + dirName + '"')
  elif mxPlatform == 'Linux':
    # Check if the program is running on Linux
    os.system('nautilus "' + dirName + '" &')
  elif mxPlatform == 'Mac':
    # Check if the program is running on Mac
    os.system('open "' + dirName + '" &')
  else:
    # Create the empty variable as a fallback mode
    dirName = ''
    
  print('[Opening the Directory] ' + dirName)
  return dirName
  
  
# Open the MaxwellRenderToolbox temporary images folder window up using your desktop file browser
# Example: mrt_openTempImagesDirectory()
def mrt_openTempImagesDirectory():
  filenameNativePath = ''
  mxPlatform = mrt_getPlatform()
  
  #Check OS platform for Windows/Mac/Linux Paths
  if mxPlatform == 'Windows':
    # Check if the program is running on Windows 
    filenameNativePath = mrt_tempImagesDirectory()
    os.system('explorer "' + filenameNativePath + '"')
  elif mxPlatform == 'Linux':
    # Check if the program is running on Linux
    filenameNativePath = mrt_tempImagesDirectory()
    os.system('nautilus "' + filenameNativePath + '" &')
  elif mxPlatform == 'Mac':
    # Check if the program is running on Mac
    filenameNativePath = mrt_tempImagesDirectory()
    os.system('open "' + filenameNativePath + '" &')
  else:
    # Create the empty variable as a fallback mode
    filenameNativePath = ''
    
  print('[Opening the Temporary Images Directory] ' + filenameNativePath)
  return filenameNativePath
  

# -------------------------------------------------------------------
# -------------------------------------------------------------------
# This code is the "main" section that is run automatically when the python script is loaded in pyMaxwell:
if __name__ == "__main__":
  # Release Version
  mrt_version = '0.1'

  print('-----------------------------------------------')
  print('Maxwell MXS to ASCII Scene Translator v' + mrt_version)
  print('By Andrew Hazelden <andrew@andrewhazelden.com>')
  print('http://www.andrewhazelden.com/blog')
  print('-----------------------------------------------\n')

  # MXS scene file extension
  mxsFileExt = 'mxs'
  
  # ------------------------------------------
  # Process a single Maxwell MXS File
  # ------------------------------------------
  # mxsFilePath = '/Applications/MaxwellRenderToolbox/examples/stereo/CubeX.mxs'
  # mxsFilePath = 'C:/Program Files/MaxwellRenderToolbox/examples/stereo/CubeX.mxs'
  # mxsFilePath = '/opt/MaxwellRenderToolbox/examples/stereo/CubeX.mxs'
  # mxsFilePath = '/home/andrew/MaxwellRenderToolbox/examples/stereo/CubeX.mxs'

  # ---------------------------------------------------
  # Or process a whole directory of Maxwell MXS files
  # ---------------------------------------------------
  mxsFilePath = '/Applications/MaxwellRenderToolbox/examples/stereo/'
  # mxsFilePath = 'C:/Program Files/MaxwellRenderToolbox/examples/stereo/'
  # mxsFilePath = '/opt/MaxwellRenderToolbox/examples/stereo/'
  # mxsFilePath = '/home/andrew/MaxwellRenderToolbox/examples/stereo/'
  # mxsFilePath = '/Applications/Maxwell 3/library/Scenes/Guggenheim_museum_Bilbao/'
  
  # Check if we are going to process 1 MXS file or a whole directory of MXS files
  if os.path.isfile(mxsFilePath):
    # Launch the MXS single file processing command
    print('[Entering MXS Single File Processing Mode]')
    # Generate the new MXA ASCII scene file
    ok = mxa_writeAsciiScene(mrt_version, mxsFilePath)
    if ok == 1:
     # Open a folder window up using your desktop file browser
     mrt_openDirectory(mxsFilePath)
  elif os.path.isdir(mxsFilePath):
    print('[Entering MXS Directory Processing Mode]')
    # Build a list of MXS files in the current directory
    mxsFileList = getFilesFromPath(mxsFilePath, mxsFileExt)
    mxsNumber=0
    # Iterate through each of the active MXS files is the current directory
    for file in mxsFileList:
      mxsNumber += 1
      mxsFileDirPath = mxsFilePath + file
      print '[MXS File] ' + mxsFileDirPath
      # Generate the new MXA ASCII scene file
      ok = mxa_writeAsciiScene(mrt_version, mxsFileDirPath)
      if ok == 1 and mxsNumber == 1:
        # Open a folder window up using your desktop file browser
        mrt_openDirectory(mxsFilePath)
  else:
    print('[MXS File Not Found] ' + mxsFilePath)

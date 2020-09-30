# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from __future__ import print_function
import math
import sys
import random
import argparse
import json
import os
from datetime import datetime as dt
import numpy as np
import errno
from movement_record import MovementRecord
import logging
import itertools


"""
Renders random scenes using Blender, each with with a random number of objects;
each object has a random size, position, color, and shape. Objects will be
nonintersecting but may partially occlude each other. Output images will be
written to disk as PNGs, and we will also write a JSON file for each image with
ground-truth scene information.

This file expects to be run from Blender like this:

blender --background --python render_images.py -- [arguments to this script]
"""

INSIDE_BLENDER = True
try:
    import bpy
    from mathutils import Vector
except ImportError as e:
    INSIDE_BLENDER = False
if INSIDE_BLENDER:
    try:
        import utils_video as utils
    except ImportError as e:
        print("\nERROR")
        print("Running render_images.py from Blender and cannot import "
              "utils.py. You may need to add a .pth file to the site-packages "
              "of Blender's bundled python with a command like this:\n "
              "echo $PWD >> $BLENDER/$VERSION/python/lib/python3.5/site-packages/clevr.pth"  # noQA
              "\nWhere $BLENDER is the directory where Blender is installed, "
              "and $VERSION is your Blender version (such as 2.78).")
        sys.exit(1)

parser = argparse.ArgumentParser()

# Input options
parser.add_argument(
    '--base_scene_blendfile',
    # default='data/base_scene.blend',
    default='data/base_scene_withAxes.blend',
    help="Base blender file on which all scenes are based; includes " +
         "ground plane, lights, and camera.")
parser.add_argument(
    '--properties_json', default='data/properties.json',
    help="JSON file defining objects, materials, sizes, and colors. " +
         "The \"colors\" field maps from CLEVR color names to RGB values; " +
         "The \"sizes\" field maps from CLEVR size names to scalars used to " +
         "rescale object models; the 'materials' and 'shapes' fields map " +
         "from CLEVR material and shape names to .blend files in the " +
         "--object_material_dir and --shape_dir directories respectively.")
parser.add_argument(
    '--shape_dir', default='data/shapes',
    help="Directory where .blend files for object models are stored")
parser.add_argument(
    '--material_dir', default='data/materials',
    help="Directory where .blend files for materials are stored")
parser.add_argument(
    '--shape_color_combos_json', default=None,
    help="Optional path to a JSON file mapping shape names to a list of " +
         "allowed color names for that shape. This allows rendering images " +
         "for CLEVR-CoGenT.")

# Settings for objects
parser.add_argument(
    '--min_objects', default=5, type=int,
    help="The minimum number of objects to place in each scene")
parser.add_argument(
    '--max_objects', default=10, type=int,
    help="The maximum number of objects to place in each scene")
parser.add_argument(
    '--min_dist', default=0.25, type=float,
    help="The minimum allowed distance between object centers")
parser.add_argument(
    '--margin', default=0.4, type=float,
    help="Along all cardinal directions (left, right, front, back), all " +
         "objects will be at least this distance apart; making resolving " +
         "spatial relationships slightly less ambiguous.")
parser.add_argument(
    '--min_pixels_per_object', default=200, type=int,
    help="All objects will have at least this many visible pixels in the " +
         "final rendered images; this ensures that no objects are fully " +
         "occluded by other objects.")
parser.add_argument(
    '--max_retries', default=50, type=int,
    help="The number of times to try placing an object before giving up and " +
         "re-placing all objects in the scene.")

# Output settings
parser.add_argument(
    '--start_idx', default=0, type=int,
    help="The index at which to start for numbering rendered images. " +
         "Setting " +
         "this to non-zero values allows you to distribute rendering across " +
         "multiple machines and recombine the results later.")
parser.add_argument(
    '--num_videos', default=1, type=int,
    help="The number of images to render")
parser.add_argument(
    '--parallel_mode', action='store_true',
    help="Set if running on multiple nodes/GPUs. Will use lock files "
         "to synchronize.")
parser.add_argument(
    '--filename_prefix', default='CLEVR',
    help="This prefix will be prepended to rendered images and JSON scenes")
parser.add_argument(
    '--split', default='new',
    help="Name of the split for which we are rendering. " +
         "This will be added to " +
         "the names of rendered images, and will also be stored in the JSON " +
         "scene structure for each image.")
parser.add_argument(
    '--output_dir', default='/output/video_dir/',
    help="The directory where output images will be stored. It will be " +
         "created if it does not exist.")
parser.add_argument(
    '--output_image_dir', default='/output/video_dir/videos/',
    help="The directory where output images will be stored. It will be " +
         "created if it does not exist.")
parser.add_argument(
    '--output_scene_dir', default='/output/video_dir/scenes/',
    help="The directory where output JSON scene structures will be stored. " +
         "It will be created if it does not exist.")
parser.add_argument(
    '--output_scene_file', default='../output/video_dir/CLEVR_scenes.json',
    help="Path to write a single JSON file containing all scene information")
parser.add_argument(
    '--output_blend_dir', default='/output/video_dir/blendfiles',
    help="The directory where blender scene files will be stored, if the " +
         "user requested that these files be saved using the " +
         "--save_blendfiles flag; in this case it'll be created if it does " +
         "not already exist.")
parser.add_argument(
    '--save_blendfiles', type=int, default=0,
    help="Setting --save_blendfiles 1 will cause the blender scene file for " +
         "each generated image to be stored in the directory specified by " +
         "the --output_blend_dir flag. These files are not saved by default " +
         "because they take up ~5-10MB each.")
parser.add_argument(
    '--version', default='1.0',
    help="String to store in the \"version\" field of the generated JSON file")
parser.add_argument(
    '--license',
    default="Creative Commons Attribution (CC-BY 4.0)",
    help="String to store in the \"license\" field of the generated JSON file")
parser.add_argument(
    '--date', default=dt.today().strftime("%m/%d/%Y"),
    help="String to store in the \"date\" field of the generated JSON file; " +
         "defaults to today's date")

# Rendering options
parser.add_argument(
    '--cpu', action='store_true', default=False,
    help="Setting true disables GPU-accelerated rendering using CUDA. " +
         "You must have an NVIDIA GPU with the CUDA toolkit installed for " +
         "GPU rendering to work. For specifying a GPU, use "
         "CUDA_VISIBLE_DEVICES before running singularity.")
parser.add_argument(
    '--width', default=320, type=int,
    help="The width (in pixels) for the rendered images")
parser.add_argument(
    '--height', default=240, type=int,
    help="The height (in pixels) for the rendered images")
parser.add_argument(
    '--key_light_jitter', default=1.0, type=float,
    help="The magnitude of random jitter to add to the key light position.")
parser.add_argument(
    '--fill_light_jitter', default=1.0, type=float,
    help="The magnitude of random jitter to add to the fill light position.")
parser.add_argument(
    '--back_light_jitter', default=1.0, type=float,
    help="The magnitude of random jitter to add to the back light position.")
parser.add_argument(
    '--camera_jitter', default=0.5, type=float,
    help="The magnitude of random jitter to add to the camera position")
parser.add_argument(
    '--render_num_samples', default=128, type=int,  # CLEVR was 512
    help="The number of samples to use when rendering. Larger values will " +
         "result in nicer images but will cause rendering to take longer.")
parser.add_argument(
    '--render_min_bounces', default=2, type=int,  # default 8
    help="The minimum number of bounces to use for rendering.")
parser.add_argument(
    '--render_max_bounces', default=2, type=int,  # default 8
    help="The maximum number of bounces to use for rendering.")
parser.add_argument(
    '--render_tile_size', default=256, type=int,
    help="The tile size to use for rendering. This should not affect the " +
         "quality of the rendered image but may affect the speed; CPU-based " +
         "rendering may achieve better performance using smaller tile sizes " +
         "while larger tile sizes may be optimal for GPU-based rendering.")

# Video options
parser.add_argument(
    '--num_frames', default=90, type=int,
    help="Number of frames to render.")
parser.add_argument(
    '--num_flips', default=10, type=int,
    help="Number of flips to render.")
parser.add_argument(
    '--fps', default=24, type=int,
    help="Video FPS.")
parser.add_argument(
    '--render', default=True, type=bool,
    help="Render the video. Otherwise will only store the blend file.")
parser.add_argument(
    "--random_camera", help="Render the video with random camera motion",
    action="store_true")
parser.add_argument(
    "--max_motions",
    help="Number of max objects to move in the single object case. "
         "This ensures the actions are sparser, and random perf lower.",
    type=int, default=999999)

parser.add_argument(
    '-d', '--debug', action='store_true',
    help="Run in debug mode. Will crash on exceptions.")
parser.add_argument(
    '--suppress_blender_logs', action='store_true',
    help="Dont print extra blender logs.")
parser.add_argument(
    "-v", "--verbose", help="increase output verbosity",
    action="store_true")


## input file 
parser.add_argument('--input_file_json', default="data.json",
    help="The tile size to use for rendering. This should not affect the " +
         "quality of the rendered image but may affect the speed; CPU-based " +
         "rendering may achieve better performance using smaller tile sizes " +
         "while larger tile sizes may be optimal for GPU-based rendering.")


random.seed(42)
np.random.seed(42)


def mkdir_p(path):
    """
    Make all directories in `path`. Ignore errors if a directory exists.
    Equivalent to `mkdir -p` in the command line, hence the name.
    """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def lock(fpath):
    lock_fpath = fpath + '.lock'
    if os.path.exists(lock_fpath):
        os.rmdir(lock_fpath)
    try:
        mkdir_p(lock_fpath)
        return True
    except Exception as e:
        logging.warning('Unable to lock {} due to {}'.format(fpath, e))
        return False


def unlock(fpath):
    lock_fpath = fpath + '.lock'
    try:
        os.rmdir(lock_fpath)
    except Exception as e:
        logging.warning('Maybe some other job already finished {}. Got {}'
                        .format(fpath, e))


def main(args):
    num_digits = 6
    prefix = '%s_%s_' % (args.filename_prefix, args.split)
    img_template = '%s%%0%dd.avi' % (prefix, num_digits)
    scene_template = '%s%%0%dd.json' % (prefix, num_digits)
    blend_template = '%s%%0%dd.blend' % (prefix, num_digits)
    output_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) 
    img_template = os.path.join(output_dir+args.output_image_dir, img_template)
    scene_template = os.path.join(output_dir+args.output_scene_dir, scene_template)
    blend_template = os.path.join(output_dir+args.output_blend_dir, blend_template)


    if not os.path.isdir(output_dir+args.output_image_dir):
        os.makedirs(output_dir+args.output_image_dir)
    if not os.path.isdir(output_dir+args.output_scene_dir):
        os.makedirs(output_dir+args.output_scene_dir)
    if args.save_blendfiles == 1 and not os.path.isdir(output_dir+args.output_blend_dir):
        os.makedirs(output_dir+args.output_blend_dir)



    all_scene_paths = []
    for i in range(args.num_videos):
        img_path = img_template % (i + args.start_idx)
        if not lock(img_path):
            continue
        logging.info('Working on {}'.format(img_path))
        scene_path = scene_template % (i + args.start_idx)
        all_scene_paths.append(scene_path)
        blend_path = None
        if args.save_blendfiles == 1:
            blend_path = blend_template % (i + args.start_idx)
        num_objects = random.randint(args.min_objects, args.max_objects)
        try:
            render_scene(
                args,
                num_objects=num_objects,
                output_index=(i + args.start_idx),
                output_split=args.split,
                output_image=img_path,
                output_scene=scene_path,
                output_blendfile=blend_path,
            )
        except Exception as e:
            if args.debug:
                unlock(img_path)
                raise e
            logging.warning('Didnt work for {} due to {}. Ignoring for now..'
                            .format(img_path, e))
        unlock(img_path)
        logging.info('Done for {}'.format(img_path))

    # After rendering all images, combine the JSON files for each scene into a
    # single JSON file.
    all_scenes = []
    for scene_path in all_scene_paths:
        with open(scene_path, 'r') as f:
            all_scenes.append(json.load(f))
    output = {
        'info': {
            'date': args.date,
            'version': args.version,
            'split': args.split,
            'license': args.license,
        },
        'scenes': all_scenes
    }
    with open(args.output_scene_file, 'w') as f:
        json.dump(output, f)


def rand(L):
    return 2.0 * L * (random.random() - 0.5)

def _add_keyframe(blender_objects, frame_id, data_path='location'):
    # If only a single object
    if not isinstance(blender_objects, list):
        blender_objects = [blender_objects]
    for obj in blender_objects:
        obj.keyframe_insert(data_path=data_path, frame=frame_id)    

# https://github.com/benckx/blender-python-examples
def rotate(obj, axis, angle, frame_begin, frame_end):
   print("inside add_rotation") 
   axis_int = ['x', 'y', 'z'].index(axis)
   obj.keyframe_insert('rotation_euler', index=axis_int, frame=frame_begin)
   obj.rotation_euler[axis_int] = math.radians(angle)
   obj.keyframe_insert('rotation_euler', index=axis_int, frame=frame_end)

def slide(obj, init_loc, start_frame, end_frame, x, y, keyframe_all_x, keyframe_all_y, keyframe_all_r, i):
    _add_keyframe(obj, start_frame)
    new_loc = (x, y, init_loc[2])
    return move_without_collision(obj, init_loc, new_loc, start_frame, end_frame, keyframe_all_x, keyframe_all_y, keyframe_all_r, i)

def bounce(obj, init_loc, start_frame, end_frame, z=None):
    #_add_keyframe(obj, start_frame)
    new_loc = (init_loc[0], init_loc[1], z)
    mid_frame = int((start_frame + end_frame)/2)
    move_to_location(obj, init_loc, new_loc, start_frame, mid_frame)  
    return move_to_location(obj, new_loc, init_loc, mid_frame+1, end_frame)

def shake(obj, init_loc, start_frame, end_frame, radius=3, freq=10):
    #_add_keyframe(obj, start_frame)
    new_loc = (init_loc[0]+radius, init_loc[1] + radius, init_loc[2])
    mid_frame = int((end_frame - start_frame + 1)/freq) - 1
    for i in range(int(freq/2)):
        move_to_location(obj, init_loc, new_loc, start_frame, start_frame + mid_frame)
        start_frame = start_frame + mid_frame + 1
        move_to_location(obj, new_loc, init_loc, start_frame, start_frame + mid_frame)
        start_frame = start_frame + mid_frame + 1    

def move_to_location(obj, init_loc, new_loc, start_frame, end_frame):
    # Compute linear interpolation between these two points
    pts_2 = []
    pts = []
    for i in range(3):
        pts.append(np.interp(
            range(start_frame, end_frame + 1),
            [start_frame, end_frame],
            [init_loc[i], new_loc[i]]).reshape((-1,)).tolist())

        pts_2.append(np.interp(
            range(start_frame, end_frame + 1),
            [start_frame, end_frame],
            [init_loc[i], new_loc[i]]).tolist())

    res = list(zip(*pts))
    assert len(res) == (end_frame - start_frame + 1), 'Must match {} to {}' \
        .format(len(res), end_frame - start_frame + 1)
    # Now effect it

    for i in range(start_frame, end_frame + 1):
        obj.location = (pts_2[0][i-start_frame], pts_2[1][i-start_frame], pts_2[2][i-start_frame])
        _add_keyframe(obj, i)
    # obj.keyframe_insert('slide', frame=end_frame)
    return res   

def move_without_collision(obj, init_loc, new_loc, start_frame, end_frame, keyframe_all_x, keyframe_all_y, keyframe_all_r, cur_iter):
    # Compute linear interpolation between these two points
    pts_2 = []
    pts = []
    for i in range(3):
        pts.append(np.interp(
            range(start_frame, end_frame + 1),
            [start_frame, end_frame],
            [init_loc[i], new_loc[i]]).reshape((-1,)).tolist())

        pts_2.append(np.interp(
            range(start_frame, end_frame + 1),
            [start_frame, end_frame],
            [init_loc[i], new_loc[i]]).tolist())

    res = list(zip(*pts))
    assert len(res) == (end_frame - start_frame + 1), 'Must match {} to {}' \
        .format(len(res), end_frame - start_frame + 1)
    # Now effect it

    flag_iter = 0  
    for i in range(start_frame, end_frame + 1):
        dists_good = True
        for j in range(0, keyframe_all_x.shape[0]):
            if  j != cur_iter:
                dx, dy = pts_2[0][i-start_frame] - keyframe_all_x[j][i], pts_2[1][i-start_frame] - keyframe_all_y[j][i]
                dist = math.sqrt(dx * dx + dy * dy)
                if dist - keyframe_all_r[j] - keyframe_all_r[cur_iter] < 1:
                    dists_good = False
                    break

        if not dists_good:
            break
        obj.location = (pts_2[0][i-start_frame], pts_2[1][i-start_frame], pts_2[2][i-start_frame])
        _add_keyframe(obj, i)
        keyframe_all_x[cur_iter][i], keyframe_all_y[cur_iter][i] = pts_2[0][i-start_frame], pts_2[1][i-start_frame]
        flag_iter = i
    # obj.keyframe_insert('slide', frame=end_frame)
    keyframe_all_x[cur_iter][flag_iter:].fill(pts_2[0][flag_iter-start_frame])
    keyframe_all_y[cur_iter][flag_iter:].fill(pts_2[1][flag_iter-start_frame])
    return keyframe_all_x[cur_iter], keyframe_all_y[cur_iter]    


def setup_scene(
    args,
    num_objects=5,
    output_index=0,
    output_split='none',
    output_image='render.png',
    output_scene='render_json',
  ):

    # This will give ground-truth information about the scene and its objects
    scene_struct = {
        'split': output_split,
        'image_index': output_index,
        'image_filename': os.path.basename(output_image),
        'objects': [],
        'directions': {},
    }

    # Put a plane on the ground so we can compute cardinal directions
    bpy.ops.mesh.primitive_plane_add(radius=5)
    plane = bpy.context.object

    # Add random jitter to camera position
    if args.camera_jitter > 0:
        for i in range(3):
            bpy.data.objects['Camera'].location[i] += rand(args.camera_jitter)
    # Figure out the left, up, and behind directions along the plane and record
    # them in the scene structure
    camera = bpy.data.objects['Camera']

    plane_normal = plane.data.vertices[0].normal
    cam_behind = camera.matrix_world.to_quaternion() * Vector((0, 0, -1))
    cam_left = camera.matrix_world.to_quaternion() * Vector((-1, 0, 0))
    cam_up = camera.matrix_world.to_quaternion() * Vector((0, 1, 0))
    plane_behind = (cam_behind - cam_behind.project(plane_normal)).normalized()
    plane_left = (cam_left - cam_left.project(plane_normal)).normalized()
    plane_up = cam_up.project(plane_normal).normalized()

    # Save all six axis-aligned directions in the scene struct
    scene_struct['directions']['behind'] = tuple(plane_behind)
    scene_struct['directions']['front'] = tuple(-plane_behind)
    scene_struct['directions']['left'] = tuple(plane_left)
    scene_struct['directions']['right'] = tuple(-plane_left)
    scene_struct['directions']['above'] = tuple(plane_up)
    scene_struct['directions']['below'] = tuple(-plane_up)

    # Delete the plane; we only used it for normals anyway. The base scene file
    # contains the actual ground plane.
    utils.delete_object(plane)

    # Add random jitter to lamp positions
    if args.key_light_jitter > 0:
        for i in range(3):
            bpy.data.objects['Lamp_Key'].location[i] += rand(
                args.key_light_jitter)
    if args.back_light_jitter > 0:
        for i in range(3):
            bpy.data.objects['Lamp_Back'].location[i] += rand(
                args.back_light_jitter)
    if args.fill_light_jitter > 0:
        for i in range(3):
            bpy.data.objects['Lamp_Fill'].location[i] += rand(
                args.fill_light_jitter)

    # objects = cup_game(scene_struct, num_objects, args, camera)
    objects, blender_objects, keyframe_all_x, keyframe_all_y, keyframe_all_r = add_random_objects(
        scene_struct, num_objects, args, camera)
    print(objects)
    for iter, i in enumerate(objects):
        obj = blender_objects[iter]
        print(i['motion'] , obj)
        if i['motion'] == "spinning":
                rotate(obj, 'x', 180, 0, 30)
                # rotate(obj, 'x', 180, 20, 35)
        elif i['motion'] == "bouncing":
            bounce(obj, obj.location.copy(), 1, 17, z=obj.location[2]+ 4)
            bounce(obj, obj.location.copy(), 18, 34, z=obj.location[2]+ 1)
            bounce(obj, obj.location.copy(), 35, 51, z=obj.location[2]+ 4)
            bounce(obj, obj.location.copy(), 51, 67, z=obj.location[2]+ 1)
        elif i['motion'] == "rocking":
            shake(obj, obj.location.copy(), 1, 80, radius = 0.1, freq = 15)
        elif i['motion'] == "moving":
            #print(keyframe_all_x[iter])
            keyframe_all_x[iter], keyframe_all_y[iter] = slide(obj, obj.location.copy(), 16, 50, obj.location[0]+5, obj.location[1], keyframe_all_x, keyframe_all_y, keyframe_all_r, iter)    
#             print(keyframe_all_x[iter])

    # Render the scene and dump the scene data structure
    scene_struct['objects'] = objects
    scene_struct['relationships'] = compute_all_relationships(scene_struct)
    #scene_struct['movements'] = record.get_dict()
    with open(output_scene, 'w') as f:
        json.dump(scene_struct, f, indent=2)


def render_scene(
        args,
        num_objects=5,
        output_index=0,
        output_split='none',
        output_image='render.png',
        output_scene='render_json',
        output_blendfile=None):
    # Load the main blendfile
    bpy.ops.wm.open_mainfile(filepath=args.base_scene_blendfile)

    # Load materials
    utils.load_materials(args.material_dir)

    # Set render arguments so we can get pixel coordinates later.
    # We use functionality specific to the CYCLES renderer so BLENDER_RENDER
    # cannot be used.
    bpy.ops.screen.frame_jump(end=False)
    render_args = bpy.context.scene.render
    render_args.engine = "CYCLES"
    render_args.filepath = output_image
    render_args.resolution_x = args.width
    render_args.resolution_y = args.height
    render_args.resolution_percentage = 100
    render_args.tile_x = args.render_tile_size
    render_args.tile_y = args.render_tile_size
    render_args.image_settings.file_format = 'AVI_JPEG'
    # Video params
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = args.num_frames  # same as kinetics
    render_args.fps = args.fps

    if args.cpu is False:
        # Blender changed the API for enabling CUDA at some point
        if bpy.app.version < (2, 78, 0):
            bpy.context.user_preferences.system.compute_device_type = 'CUDA'
            bpy.context.user_preferences.system.compute_device = 'CUDA_0'
        else:
            cycles_prefs = bpy.context.user_preferences.addons[
                'cycles'].preferences
            cycles_prefs.compute_device_type = 'CUDA'
            # # In case more than 1 device passed in, use only the first one
            # Not effective, CUDA_VISIBLE_DEVICES before running singularity
            # works fastest.
            # if len(cycles_prefs.devices) > 2:
            #     for device in cycles_prefs.devices:
            #         device.use = False
            #     cycles_prefs.devices[1].use = True
            #     print('Too many GPUs ({}). Using {}. Set only 1 before '
            #           'running singularity.'.format(
            #               len(cycles_prefs.devices),
            #               cycles_prefs.devices[1]))

    # Some CYCLES-specific stuff
    bpy.data.worlds['World'].cycles.sample_as_light = True
    bpy.context.scene.cycles.blur_glossy = 2.0
    bpy.context.scene.cycles.samples = args.render_num_samples
    bpy.context.scene.cycles.transparent_min_bounces = args.render_min_bounces
    bpy.context.scene.cycles.transparent_max_bounces = args.render_max_bounces
    if args.cpu is False:
        bpy.context.scene.cycles.device = 'GPU'

    if output_blendfile is not None and os.path.exists(output_blendfile):
        logging.info('Loading pre-defined BLEND file from {}'.format(
            output_blendfile))
        bpy.ops.wm.open_mainfile(filepath=output_blendfile)
    else:
        setup_scene(
            args, num_objects, output_index, output_split,
            output_image, output_scene)
    print_camera_matrix()
    if args.random_camera:
        add_random_camera_motion(args.num_frames)
    if output_blendfile is not None and not os.path.exists(output_blendfile):
        bpy.ops.wm.save_as_mainfile(filepath=output_blendfile)
    max_num_render_trials = 10
    if args.render:
        while max_num_render_trials > 0:
            try:
                if args.suppress_blender_logs:
                    # redirect output to log file
                    logfile = 'logfile'
                    open(logfile, 'a').close()
                    old = os.dup(1)
                    sys.stdout.flush()
                    os.close(1)
                    os.open(logfile, os.O_WRONLY)
                bpy.ops.render.render(animation=True)
                if args.suppress_blender_logs:
                    # disable output redirection
                    os.close(1)
                    os.dup(old)
                    os.close(old)
                break
            except Exception as e:
                max_num_render_trials -= 1
                print(e)


def print_camera_matrix():
    # from
    # https://blender.stackexchange.com/questions/16472/how-can-i-get-the-cameras-projection-matrix
    camera = bpy.data.objects['Camera']
    render = bpy.context.scene.render
    modelview_matrix = camera.matrix_world.inverted()
    projection_matrix = camera.calc_matrix_camera(
        render.resolution_x,
        render.resolution_y,
        render.pixel_aspect_x,
        render.pixel_aspect_y,
    )
    final_mat = projection_matrix * modelview_matrix
    print('Overall camera matrix:', final_mat)


def get_new_camera_location():
    # Don't move in X and Y at the same time, as it crosses the 0,0,z point
    # which is a singularity
    new_x, new_y, new_z = None, None, None
    if np.random.random() > 0.5:
        # Move in X
        new_x = np.random.choice([-10, 10])
    else:
        # Move in Y
        new_y = np.random.choice([-10, 10])
    new_z = np.random.choice([8, 10, 12])
    return new_x, new_y, new_z


def add_random_camera_motion(num_frames):
    # Now go through these locations in a random order
    shift_interval = 30
    # Start from the same position everytime, as I want to be able to track
    # positions
    add_camera_position(0, (None, None, None))
    for frame_id in range(shift_interval, num_frames, shift_interval):
        last_loc = get_new_camera_location()
        add_camera_position(frame_id, last_loc)
    add_camera_position(num_frames, last_loc)


def add_camera_position(frame_id, loc):
    obj = bpy.data.objects['Camera']
    if loc[0] is not None:
        obj.location.x = loc[0]
    if loc[1] is not None:
        obj.location.y = loc[1]
    if loc[2] is not None:
        obj.location.z = loc[2]
    obj.keyframe_insert(data_path='location', frame=frame_id)


def add_random_objects(scene_struct, num_objects, args, camera):
    """
    Add random objects to the current blender scene
    """

    input_file = open(args.input_file_json, 'r')
    input_objects = json.load(input_file)
    input_file.close()

    # Load the property file
    with open(args.properties_json, 'r') as f:
        properties = json.load(f)
        color_name_to_rgba = {}
        for name, rgb in properties['colors'].items():
            rgba = [float(c) / 255.0 for c in rgb] + [1.0]
            color_name_to_rgba[name] = rgba
        material_mapping = [(v, k) for k, v in properties['materials'].items()]
        object_mapping = [(v, k) for k, v in properties['shapes'].items()]
        size_mapping = list(properties['sizes'].items())

    shape_color_combos = None
    if args.shape_color_combos_json is not None:
        with open(args.shape_color_combos_json, 'r') as f:
            shape_color_combos = list(json.load(f).items())

    positions = []
    objects = []
    blender_objects = []

    keyframe_all_x = np.empty((len(input_objects['objects']),args.num_frames))
    keyframe_all_y = np.empty((len(input_objects['objects']),args.num_frames))
    keyframe_all_r = np.empty(len(input_objects['objects']))

    for i in range(len(input_objects['objects'])):
        # Choose a random size
        if input_objects['objects'][i]['size_name'] == 'any':
            size_name, r = random.choice(size_mapping)
        else:
            size_name = input_objects['objects'][i]['size_name']
            r = properties['sizes'][size_name]
        
        if input_objects['objects'][i]['obj_name'] == 'any':
            obj_name, obj_name_out = random.choice(object_mapping)
        else:
            obj_name_out = input_objects['objects'][i]['obj_name']
            obj_name = properties['shapes'][obj_name_out] 
            
        if input_objects['objects'][i]['color_name'] == 'any':
            color_name, rgba = random.choice(list(color_name_to_rgba.items()))
        else:
            color_name = input_objects['objects'][i]['color_name']
            rgba = color_name_to_rgba[color_name]

        if input_objects['objects'][i]["mat_name"] == 'any':
            mat_name, mat_name_out = random.choice(material_mapping)
        else:
            mat_name_out = input_objects['objects'][i]["mat_name"]
            mat_name = properties['materials'][mat_name_out] 
           

        # Try to place the object, ensuring that we don't intersect any
        # existing objects and that we are more than the desired margin away
        # from all existing objects along all cardinal directions.
        num_tries = 0
        while True:
            # If we try and fail to place an object too many times, then
            # delete all the objects in the scene and start over.
            num_tries += 1
            if num_tries > args.max_retries:
                for obj in blender_objects:
                    utils.delete_object(obj)
                return add_random_objects(scene_struct, num_objects, args,
                                          camera)
            x = random.uniform(-3, 3)
            y = random.uniform(-3, 3)
            # Check to make sure the new object is further than min_dist from
            # all other objects, and further than margin along the four
            # cardinal directions
            dists_good = True
            margins_good = True
            for (xx, yy, rr) in positions:
                dx, dy = x - xx, y - yy
                dist = math.sqrt(dx * dx + dy * dy)
                if dist - r - rr < args.min_dist:
                    dists_good = False
                    break
                for direction_name in ['left', 'right', 'front', 'behind']:
                    direction_vec = scene_struct['directions'][direction_name]
                    assert direction_vec[2] == 0
                    margin = dx * direction_vec[0] + dy * direction_vec[1]
                    if 0 < margin < args.margin:
                        logging.debug('{} {} {}'.format(
                            margin, args.margin, direction_name))
                        logging.debug('BROKEN MARGIN!')
                        margins_good = False
                        break
                if not margins_good:
                    break
            if dists_good and margins_good:
                break

        # For cube, adjust the size a bit
        if obj_name == 'Cube':
            r /= math.sqrt(2)

        # Choose random orientation for the object.
        theta = 360.0 * random.random()

        # Actually add the object to the scene
        utils.add_object(args.shape_dir, obj_name, r, (x, y), theta=theta)
        obj = bpy.context.object
        blender_objects.append(obj)
        positions.append((x, y, r))

        keyframe_all_x[i].fill(x)
        keyframe_all_y[i].fill(y)
        keyframe_all_r[i].fill(r)

        # Actually add material
        utils.add_material(mat_name, Color=rgba)

        # Record data about the object in the scene data structure
        pixel_coords = utils.get_camera_coords(camera, obj.location)

        motion_name_out = input_objects['objects'][i]["motion_name"]

        
        objects.append({
            'shape': obj_name_out,
            'size': size_name,
            'sized': r,
            'material': mat_name_out,
            '3d_coords': tuple(obj.location),
            'rotation': theta,
            'pixel_coords': pixel_coords,
            'color': color_name,
            'instance': obj.name,
            'motion' : motion_name_out
        })
    return objects, blender_objects, keyframe_all_x, keyframe_all_y, keyframe_all_r


def compute_all_relationships(scene_struct, eps=0.2):
    """
    Computes relationships between all pairs of objects in the scene.

    Returns a dictionary mapping string relationship names to lists of lists of
    integers, where output[rel][i] gives a list of object indices that have the
    relationship rel with object i. For example if j is in output['left'][i]
    then object j is left of object i.
    """
    all_relationships = {}
    for name, direction_vec in scene_struct['directions'].items():
        if name == 'above' or name == 'below':
            continue
        all_relationships[name] = []
        for i, obj1 in enumerate(scene_struct['objects']):
            coords1 = obj1['3d_coords']
            related = set()
            for j, obj2 in enumerate(scene_struct['objects']):
                if obj1 == obj2:
                    continue
                coords2 = obj2['3d_coords']
                diff = [coords2[k] - coords1[k] for k in [0, 1, 2]]
                dot = sum(diff[k] * direction_vec[k] for k in [0, 1, 2])
                if dot > eps:
                    related.add(j)
                all_relationships[name].append(sorted(list(related)))
    return all_relationships


if __name__ == '__main__':
    if INSIDE_BLENDER:
        # Run normally
        argv = utils.extract_args()
        args = parser.parse_args(argv)
        if args.verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        main(args)
    elif '--help' in sys.argv or '-h' in sys.argv:
        parser.print_help()
    else:
        print('This script is intended to be called from blender like this:')
        print()
        print('blender --background --python render_images.py -- [args]')
        print()
        print('You can also run as a standalone python script to view all')
        print('arguments like this:')
        print()
        print('python render_images.py --help')

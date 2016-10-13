# this script makes convert setting to monochrome lineart for comics
# use for Blender Render (no support cycles Render )

#Copyright (c) 2014 Shunnich Fujiwara
#Released under the MIT license
#http://opensource.org/licenses/mit-license.php

import bpy

################### misc ###########################
def removeRenderingFolder():
    # avoid to backup file incrementaly
    import os
    import shutil
    path = os.path.expanduser("~/Desktop/rendering/1")
    dst = os.path.expanduser("~/Desktop/rendering/bk")
    shutil.rmtree(dst, ignore_errors=True)
    if os.path.exists(path):
        os.replace(path, dst)
    return


# back drop on
def useBackDrop():
    a = bpy.context.area
    a_temp = a.type
    a.type = 'NODE_EDITOR'
    space = a.spaces.active
    space.show_backdrop = True
    a.type = a_temp
    return


# join objects to clear non-manified edges
def objectJoin():
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH':
            ob.select = True
            bpy.context.scene.objects.active = ob
        else:
            ob.select = False
    bpy.ops.object.join()
    return


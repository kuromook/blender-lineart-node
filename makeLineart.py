# this script convert setting to monochrome lineart for comics
import bpy


# set white materials whole objects, then set edge and freestyle line
def makeLineart(name="lineartWhite"):

    edge_threshold = 44
    line_thickness = 1.1

    # apply white material and edge
    for item in bpy.data.objects:
        if item.type == 'MESH':
            item.data.materials.append(bpy.data.materials[name])

    bpy.context.scene.render.use_edge_enhance = True
    bpy.context.scene.render.edge_threshold = edge_threshold

    bpy.context.scene.render.use_freestyle = True
    bpy.data.linestyles["LineStyle"].panel = "THICKNESS"
    bpy.data.linestyles["LineStyle"].thickness = line_thickness
    bpy.data.linestyles["LineStyle"].thickness_position = 'RELATIVE'
    bpy.data.linestyles["LineStyle"].thickness_ratio = 0

    # background tranceparency
    bpy.context.scene.render.alpha_mode = 'TRANSPARENT'
    # bpy.context.scene.color_mode = 'RGBA'   # not work
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    return


# add lineart white material
def addLineartMaterial(name="lineartWhite"):
    mat = bpy.data.materials.new(name)
    mat.use_shadeless = True
    mat.diffuse_color = (float(1), float(1), float(1))
    return


# import lineart white material from blend file, if you'd like to use
def appendMaterial(name="lineartWhite"):

    desktop = os.path.expanduser("~/Desktop")
    whiteCubeMaterial = desktop + "/blend/material_test/whitecube.blend/Material/"

    # material append
    bpy.ops.wm.link_append(directory=whiteCubeMaterial, link=False, filename=name)
    return


# clear lamps and materials exist
def clearObjects():

    scn = bpy.context.scene
    for ob in scn.objects:
        if ob.type == 'LAMP':
        #    if ob.type == 'CAMERA' or ob.type == 'LAMP':
            scn.objects.unlink(ob)

    for item in bpy.data.objects:
        if item.type == 'MESH':
            while item.data.materials:
                item.data.materials.pop(0, update_data=True)
    return


################### add on setting section###########################
bl_info = {
    "name": "Conver Comic Lineart",
    "category": "Object",
}

import bpy


class ComicLineart(bpy.types.Operator):
    """lineart converter"""
    bl_idname = "lineart.comic"
    bl_label = "comic lineart"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):    
        clearObjects()
        addLineartMaterial()
        makeLineart()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ComicLineart)


def unregister():
    bpy.utils.unregister_class(ComicLineart)


if __name__ == "__main__":
    register()

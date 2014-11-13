# this script convert setting to monochrome lineart for comics
import bpy

def comicLineartNode():
    # this script convert setting to monochrome lineart for comics
     
    s = bpy.context.scene

    edge_threshold = 44
    line_thickness = 1.1

    percentage = s.render.resolution_percentage
    x = s.render.resolution_x * percentage / 100
    y = s.render.resolution_y * percentage / 100
    size = x if x >= y else y

    edge_threshold += int( size / 500) * 10
    line_thickness += int( size / 2000)


    s.render.use_freestyle = True
    s.render.alpha_mode = 'TRANSPARENT'
    s.render.image_settings.color_mode = 'RGBA'

    s.render.use_edge_enhance = True
    s.render.edge_threshold = edge_threshold

    # render layer setting
    f = s.render.layers.active
    f.name ="Freestyle"
    r= s.render.layers.new( "RenderLayer")

    r.use_freestyle = False

    f.use_strand = False
    f.use_edge_enhance = False
    f.use_sky = False
    f.use_solid = False
    f.use_halo = False
    f.use_ztransp = False


    bpy.data.linestyles["LineStyle"].panel = "THICKNESS"
    bpy.data.linestyles["LineStyle"].thickness = line_thickness
    bpy.data.linestyles["LineStyle"].thickness_position = 'RELATIVE'
    bpy.data.linestyles["LineStyle"].thickness_ratio = 0


    s.use_nodes = True

    # nodes
    n = s.node_tree.nodes
    l = s.node_tree.links
    g = bpy.data.node_groups

    composite = n["Composite"]
    composite.location = (1200, 100)
    render = n["Render Layers"]
    render.layer = 'RenderLayer'
    render.location = (0, 0)

    composite.use_alpha = True

    freestyleRender = n.new("CompositorNodeRLayers")
    freestyleRender.layer = 'Freestyle'
    freestyleRender.location=(0,500)

    alpha = n.new("CompositorNodeAlphaOver")
    rgb2Bw = n.new("CompositorNodeRGBToBW")
    val2Rgb = n.new("CompositorNodeValToRGB")
    setAlpha = n.new("CompositorNodeSetAlpha")
    dilate = n.new("CompositorNodeDilateErode")

    rgb2Bw.location = (200, 100)
    val2Rgb.location = (400, 100)
    alpha.location = (900,300)
    setAlpha.location = (700, 500)
    dilate.location = (400, 400)

    rgb = n.new("CompositorNodeRGB")
    alphaMerge = n.new("CompositorNodeAlphaOver")
    setAlphaMerge = n.new("CompositorNodeSetAlpha")

    rgb.location = (400, -200)
    alphaMerge.location = (900, -200)
    setAlphaMerge.location= (700, -200)

    l.new(render.outputs[0], rgb2Bw.inputs[0])
    l.new(rgb2Bw.outputs[0], val2Rgb.inputs[0])
    l.new(val2Rgb.outputs[0], setAlpha.inputs[0])
    l.new(render.outputs['Alpha'], dilate.inputs[0])
    l.new(dilate.outputs[0], setAlpha.inputs[1])
    l.new(setAlpha.outputs[0],alpha.inputs[1])

    l.new(freestyleRender.outputs[0], alpha.inputs[2])
    l.new(alpha.outputs[0], composite.inputs[0])

    l.new(rgb.outputs[0],setAlphaMerge.inputs[0])
    l.new(dilate.outputs[0], setAlphaMerge.inputs[1])
    l.new(setAlphaMerge.outputs[0], alphaMerge.inputs[1])
    l.new(freestyleRender.outputs[0], alphaMerge.inputs[2])

    # gray setting
    val2Rgb.color_ramp.interpolation = 'CONSTANT'
    #val2Rgb.color_ramp.color_mode="HSV"
    #val2Rgb.color_ramp.hue_interpolation = 'near'

    dilate.distance = -1

    val2Rgb.color_ramp.elements[1].color = (1, 1, 1, 1)
    val2Rgb.color_ramp.elements[0].color = (0.279524, 0.279524, 0.279524, 1)
    val2Rgb.color_ramp.elements[1].position=0.08
    val2Rgb.color_ramp.elements[1].position=0.0

    rgb.outputs[0].default_value = (1,1,1,1)

    # output to image file
    import os
    lineout = n.new("CompositorNodeOutputFile")
    lineout.name = "line out"
    lineout.location = (200, 600)
    lineout.base_path = os.path.expanduser("~/Desktop/rendering/l")
    lineout.file_slots.new("rendering")

    grayout = n.new("CompositorNodeOutputFile")
    grayout.name = "gray out"
    grayout.location = (1200, 600)
    grayout.base_path = os.path.expanduser("~/Desktop/rendering/g")
    grayout.file_slots.new("rendering")

    mergeout = n.new("CompositorNodeOutputFile")
    mergeout.name = "merge out"
    mergeout.location = (1200, -100)
    mergeout.base_path = os.path.expanduser("~/Desktop/rendering/m")
    mergeout.file_slots.new("rendering")

    l.new(freestyleRender.outputs[0], lineout.inputs[-1])
    l.new(setAlpha.outputs[0], grayout.inputs[-1])
    l.new(alphaMerge.outputs[0], mergeout.inputs[-1])







################### add on setting section###########################
bl_info = {
    "name": "Conver Comic Lineart　Node",
    "category": "Object",
}

import bpy


class ComicLineartNode(bpy.types.Operator):
    """lineart converter by Node"""
    bl_idname = "lineartgray.comic"
    bl_label = "comic lineart node"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):    
        comicLineartNode()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ComicLineartNode)


def unregister():
    bpy.utils.unregister_class(ComicLineartNode)


if __name__ == "__main__":
    register()

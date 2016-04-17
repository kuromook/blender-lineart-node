# this script makes convert setting to monochrome lineart for comics

#Copyright (c) 2014 Shunnich Fujiwara
#Released under the MIT license
#http://opensource.org/licenses/mit-license.php

import bpy


def comicLineartNode():
    '''make line art and shadow render'''
    s = bpy.context.scene

    line_thickness = 1.1
    edge_threshold = 44

    percentage = s.render.resolution_percentage
    x = s.render.resolution_x * percentage / 100
    y = s.render.resolution_y * percentage / 100
    size = x if x >= y else y

    edge_threshold += int( size / 500) * 40
    line_thickness += int( size / 2000)

    s.render.image_settings.file_format = 'PNG'

    s.render.use_freestyle = True
    s.render.alpha_mode = 'TRANSPARENT'
    s.render.image_settings.color_mode = 'RGBA'

    s.render.use_edge_enhance = True
    s.render.edge_threshold = edge_threshold


    #s.render.layers.active.freestyle_settings.crease_angle = 1.2


    # render layer setting
    f = s.render.layers.active
    f.name ="Freestyle"
    r= s.render.layers.new( "RenderLayer")

    r.use_freestyle = False
    r.use_pass_ambient_occlusion = True

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

    bpy.ops.scene.new(type="LINK_OBJECTS")
    aos = bpy.context.scene
    aos.name = "AO"
    w = bpy.data.worlds.new("AO")
    w.light_settings.use_ambient_occlusion = True
    aos.world = bpy.data.worlds["AO"]

    # nodes
    s.use_nodes = True

    n = s.node_tree.nodes
    l = s.node_tree.links
    g = bpy.data.node_groups

    composite = n["Composite"]
    composite.location = (1200, 100)
    render = n["Render Layers"]
    render.layer = 'RenderLayer'

    s.render.layers["RenderLayer"].use_pass_object_index = True

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
    viewer = n.new("CompositorNodeViewer")


    rgb2Bw.location = (200, 100)
    val2Rgb.location = (400, 100)
    alpha.location = (900, 300)
    setAlpha.location = (700, 500)
    dilate.location = (400, 400)
    viewer.location = (1300, 350)


    rgb = n.new("CompositorNodeRGB")
    alphaMerge = n.new("CompositorNodeAlphaOver")
    setAlphaMerge = n.new("CompositorNodeSetAlpha")

    rgb.location = (400, -200)
    alphaMerge.location = (900, -200)
    setAlphaMerge.location= (700, -200)

    render_ao = n.new(type="CompositorNodeRLayers")
    dilate_ao = n.new("CompositorNodeDilateErode")
    setAlpha_ao = n.new("CompositorNodeSetAlpha")

    render_ao.location = (-200, -300)
    dilate_ao.location = (100, -300)
    setAlpha_ao.location = (200, -500)
    render_ao.scene = bpy.data.scenes["AO"]
    render_ao.layer = 'RenderLayer'

    def getObjectPassIndex():
        o = bpy.data.objects
        index = [i.pass_index for i in o]
        unique = lambda x: list(set(x))
        index = unique(index)
        index.remove(0)     # ignore 0 as default value
        return index

    def makeNodeObIDMask(passIndex, count):
        import os
        objectid_mask = n.new(type='CompositorNodeIDMask')
        setMix_obj = n.new("CompositorNodeMixRGB")
        objectid_mask.index = passIndex
        objectid_mask.use_antialiasing = True

        objectid_mask.location = (800, -1000 + count*(-200))
        setMix_obj.location = (1000, -1000 + count*(-200))
        setMix_obj.inputs[2].default_value = (0.8, 0.8, 0.8, 1)
        l.new(render.outputs["IndexOB"], objectid_mask.inputs[0])
        l.new(objectid_mask.outputs[0], setMix_obj.inputs[0])

        objectMaskOut = n.new("CompositorNodeOutputFile")
        objectMaskOut.name = "ob mask out"
        objectMaskOut.location = (1200, -1000 + count*(-200))
        objectMaskOut.base_path = os.path.expanduser("~/Desktop/rendering/1")
        objectMaskOut.file_slots.new("rendering_OBmask" + str(passIndex) + "_")

        l.new(setMix_obj.outputs[0], objectMaskOut.inputs[-1])
        return

    objectPassIndexList = getObjectPassIndex()
    for i, v in enumerate(objectPassIndexList):
        makeNodeObIDMask(v, i)

    l.new(render.outputs[0], rgb2Bw.inputs[0])
    l.new(rgb2Bw.outputs[0], val2Rgb.inputs[0])
    l.new(val2Rgb.outputs[0], setAlpha.inputs[0])
    l.new(render.outputs['Alpha'], dilate.inputs[0])
    l.new(dilate.outputs[0], setAlpha.inputs[1])
    l.new(setAlpha.outputs[0], alpha.inputs[1])
    l.new(alpha.outputs[0], viewer.inputs[0])


    l.new(freestyleRender.outputs[0], alpha.inputs[2])
    l.new(alpha.outputs[0], composite.inputs[0])

    l.new(rgb.outputs[0], setAlphaMerge.inputs[0])
    l.new(dilate.outputs[0], setAlphaMerge.inputs[1])
    l.new(setAlphaMerge.outputs[0], alphaMerge.inputs[1])
    l.new(freestyleRender.outputs[0], alphaMerge.inputs[2])

    l.new(render_ao.outputs['AO'],setAlpha_ao.inputs[0])
    l.new(render_ao.outputs['AO'],dilate_ao.inputs[0])
    l.new(render_ao.outputs['Alpha'], dilate_ao.inputs[0])
    l.new(dilate_ao.outputs[0], setAlpha_ao.inputs[1])


    # gray setting
    val2Rgb.color_ramp.interpolation = 'CONSTANT'
    #val2Rgb.color_ramp.color_mode="HSV"
    #val2Rgb.color_ramp.hue_interpolation = 'near'

    dilate.distance = -1
    dilate_ao.distance = -1

    val2Rgb.color_ramp.elements[1].color = (1, 1, 1, 1)
    val2Rgb.color_ramp.elements[0].color = (0.279524, 0.279524, 0.279524, 1)
    val2Rgb.color_ramp.elements[1].position=0.08
    val2Rgb.color_ramp.elements[1].position=0.0

    rgb.outputs[0].default_value = (1,1,1,1)

    # output to image files
    import os
    lineout = n.new("CompositorNodeOutputFile")
    lineout.name = "line out"
    lineout.location = (200, 600)
    lineout.base_path = os.path.expanduser("~/Desktop/rendering/1")
    lineout.file_slots.new("rendering_lineart")

    grayout = n.new("CompositorNodeOutputFile")
    grayout.name = "gray out"
    grayout.location = (1200, 600)
    grayout.base_path = os.path.expanduser("~/Desktop/rendering/1")
    grayout.file_slots.new("rendering_shadow")

    aoout = n.new("CompositorNodeOutputFile")
    aoout.name = "ao out"
    aoout.location = (400, -400)
    aoout.base_path = os.path.expanduser("~/Desktop/rendering/1")
    aoout.file_slots.new("rendering_ao")


    l.new(freestyleRender.outputs[0], lineout.inputs[-1])
    l.new(setAlpha.outputs[0], grayout.inputs[-1])
    l.new(setAlpha_ao.outputs[0], aoout.inputs[-1])

    bpy.context.screen.scene = s
    return


def baseLayerNode():
    "make base render by using pass index"
    # pass index 1 to 10%, 2 to 20%, ...
    idMaskList = {1: 1, 2: 2, 3: 3, 4: 4}

    s = bpy.context.scene
    r = s.render.layers.new("BaseLayer")

    BS_LOCATION_X = 0
    BS_LOCATION_Y = -600

    s.render.layers["BaseLayer"].use_pass_material_index = True

    # nodes
    s.use_nodes = True
    m = bpy.data.materials
    n = s.node_tree.nodes
    l = s.node_tree.links
    g = bpy.data.node_groups

    g_base = g.new("base", "CompositorNodeTree")
    gn = g_base.nodes
    gl = g_base.links
    g_base.inputs.new("NodeSocketFloat", "index")
    input_node = g_base.nodes.new("NodeGroupInput")
    input_node.location = (0, 0)

    out = n['Composite']

    c = n.new(type="CompositorNodeRLayers")
    c.location = (0, BS_LOCATION_Y + 2000)
    c.name = "BaseLayer"
    c.layer = 'BaseLayer'

    def createBase(i, v):
        id_mask = gn.new(type='CompositorNodeIDMask')
        id_mask.index = i
        id_mask.location = (300, BS_LOCATION_Y + i*200)

        mix = gn.new(type='CompositorNodeMixRGB')
        mix.location = (600, BS_LOCATION_Y + i*200)
        val = 1.0-v*0.1
        mix.inputs[2].default_value = (val, val, val, 1)
        mix.name = str(i)

        gl.new(input_node.outputs["index"], id_mask.inputs[0])
        gl.new(id_mask.outputs[0], mix.inputs[0])
        return mix


    def multiNode(i, pre_mix, mix):
        multi = gn.new(type='CompositorNodeMixRGB')
        multi.blend_type = 'MULTIPLY'
        multi.location = (300 + i*300, BS_LOCATION_Y + i*200)

        gl.new(mix.outputs[0], multi.inputs[1])
        gl.new(pre_mix.outputs[0], multi.inputs[2])
        return multi

    def createOutput(pre):
        import os
        baseout = n.new("CompositorNodeOutputFile")
        baseout.name = "base out"
        baseout.location = (600, BS_LOCATION_Y + 2000)
        baseout.base_path = os.path.expanduser("~/Desktop/rendering/1")
        baseout.file_slots.new("rendering_base")

        l.new(pre.outputs[0], baseout.inputs[-1])
        return

    def createGroupOutput(pre):
        g_base.outputs.new("NodeSocketFloat", "image")
        output_node = g_base.nodes.new("NodeGroupOutput")
        output_node.location = (600 + len(idMaskList)*300, BS_LOCATION_Y + len(idMaskList) * 200 - 400)
        gl.new(pre.outputs[0], output_node.inputs[-1])
        return

    for i, v in idMaskList.items():
        mix = createBase(i, v)
        if i > 1:
            pre_mix = multiNode(i, pre_mix, mix)
        else:
            pre_mix = mix
    createGroupOutput(pre_mix)

    base_group = n.new("CompositorNodeGroup")
    base_group.location = (300, BS_LOCATION_Y+2000)
    base_group.node_tree = g_base
    l.new(c.outputs["IndexMA"], base_group.inputs[0])
    createOutput(base_group)
    return


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

################### add on setting section###########################
bl_info = {
    "name": "Convert Comic Lineart　Node",
    "category": "Object",
}

import bpy


class ComicLineartNode(bpy.types.Operator):
    """lineart converter by Node"""
    bl_idname = "lineartgray.comic"
    bl_label = "comic lineart node"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 
        bpy.context.scene.render.engine = 'BLENDER_RENDER'   
        removeRenderingFolder()  
        useBackDrop()  
        baseLayerNode()
        comicLineartNode()
        #objectJoin()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ComicLineartNode)


def unregister():
    bpy.utils.unregister_class(ComicLineartNode)


if __name__ == "__main__":
    register()

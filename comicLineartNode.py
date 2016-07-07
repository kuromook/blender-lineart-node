# this script makes convert setting to monochrome lineart for comics
# use for Blender Render (no support cycles Render )

#Copyright (c) 2014 Shunnich Fujiwara
#Released under the MIT license
#http://opensource.org/licenses/mit-license.php

import bpy

################### test  ###########################

def createLayerDivisionNodes():
    def makeObjMap():
        '''map in which mesh object exist'''
        obs = bpy.data.objects
        obs = [o for o in obs if o.type == "MESH"]

        ary = [[] for row in range(20)]
        for o in obs:
            if any(o.layers):
                i = list(o.layers).index(True)
                print(i)
                ary[i].append(o)
        return ary

    #bpy.context.scene.cycles.film_transparent = True

    def getRLayers():
        renderLayers = bpy.data.scenes['Scene'].render.layers
        renderLayers = [l for l in renderLayers if any(l.layers)]
        return renderLayers

    s = bpy.context.scene
    n = s.node_tree.nodes
    l = s.node_tree.links
    g = bpy.data.node_groups

    s.render.alpha_mode = 'TRANSPARENT'

    renderLayers = getRLayers()
    y = 0
    before = None
    for layer in renderLayers:
        # unless render layer has no objects, create render layer node
        c = n.new("CompositorNodeRLayers")
        c.layer = layer.name
        c.location = (0, y)
        if before is not None:
            alpha = n.new("CompositorNodeAlphaOver")
            alpha.location = (300, y)
            l.new(alpha.inputs[1], c.outputs[0])
            l.new(before.outputs[0], alpha.inputs[2])
            before = alpha
        else:
            before = c
        y += 300

    output = n.new("CompositorNodeComposite")
    l.new(before.outputs[0], output.inputs[0])
    return

################### node group ###########################
def createLineartGroup():
    '''linart & shadow converter group node'''
    g = bpy.data.node_groups

    g_line = g.new("lineart", "CompositorNodeTree")
    gn = g_line.nodes
    gl = g_line.links

    # group input
    g_line.inputs.new("NodeSocketColor", "render")
    g_line.inputs.new("NodeSocketFloat", "render_alpha")
    g_line.inputs.new("NodeSocketColor", "freestyle")
    g_line.inputs.new("NodeSocketFloat", "freestyle_alpha")
    g_line.inputs.new("NodeSocketColor", "ao")
    g_line.inputs.new("NodeSocketFloat", "ao_alpha")

    input_node = g_line.nodes.new("NodeGroupInput")
    input_node.location = (0, 0)

    # group output
    g_line.outputs.new("NodeSocketColor", "lineart")
    g_line.outputs.new("NodeSocketColor", "preview")
    g_line.outputs.new("NodeSocketColor", "ao")
    g_line.outputs.new("NodeSocketColor", "gray")
    g_line.outputs.new("NodeSocketColor", "line_with_mask")

    output_node = g_line.nodes.new("NodeGroupOutput")
    output_node.location = (1200, 0)

    # nodes lineart
    alpha = gn.new("CompositorNodeAlphaOver")
    rgb2Bw = gn.new("CompositorNodeRGBToBW")
    val2Rgb = gn.new("CompositorNodeValToRGB")
    setAlpha = gn.new("CompositorNodeSetAlpha")
    dilate = gn.new("CompositorNodeDilateErode")

    rgb2Bw.location = (200, 100)
    val2Rgb.location = (400, 100)
    alpha.location = (900, 300)
    setAlpha.location = (700, 500)
    dilate.location = (400, 400)

    #rgb = gn.new("CompositorNodeRGB")
    #alphaMerge = gn.new("CompositorNodeAlphaOver")
    setAlphaMerge = gn.new("CompositorNodeSetAlpha")

    #rgb.location = (400, -200)
    #alphaMerge.location = (900, -200)
    setAlphaMerge.location= (700, -200)

    dilate_ao = gn.new("CompositorNodeDilateErode")
    setAlpha_ao = gn.new("CompositorNodeSetAlpha")

    dilate_ao.location = (100, -300)
    setAlpha_ao.location = (400, -500)

    gl.new(input_node.outputs[0], rgb2Bw.inputs[0])
    gl.new(rgb2Bw.outputs[0], val2Rgb.inputs[0])
    gl.new(val2Rgb.outputs[0], setAlpha.inputs[0])
    gl.new(input_node.outputs[1], dilate.inputs[0])
    gl.new(dilate.outputs[0], setAlpha.inputs[1])
    gl.new(setAlpha.outputs[0], alpha.inputs[1])

    #gl.new(input_node.outputs[3], output_node.inputs[0])
    gl.new(alpha.outputs[0], output_node.inputs[1])

    #gl.new(rgb.outputs[0], setAlphaMerge.inputs[0])
    #gl.new(dilate.outputs[0], setAlphaMerge.inputs[1])
    gl.new(setAlphaMerge.inputs[0], input_node.outputs[2])
    gl.new(setAlphaMerge.inputs["Alpha"], input_node.outputs[3])

    #gl.new(input_node.outputs[3], alphaMerge.inputs[2])

    gl.new(input_node.outputs[4], setAlpha_ao.inputs[0])
    gl.new(input_node.outputs[5], dilate_ao.inputs[0])
    gl.new(dilate_ao.outputs[0], setAlpha_ao.inputs[1])

    #gl.new(output_node.inputs[1], setAlpha.outputs[0])
    gl.new(output_node.inputs[2], setAlpha_ao.outputs[0])
    gl.new(output_node.inputs[3], setAlpha.outputs[0])

    gl.new(setAlphaMerge.outputs[0], alpha.inputs[2])
    gl.new(setAlphaMerge.outputs[0], output_node.inputs[0])

    gl.new(input_node.outputs[1], output_node.inputs[4])

    # gray setting
    val2Rgb.color_ramp.interpolation = 'CONSTANT'
    #val2Rgb.color_ramp.color_mode="HSV"
    #val2Rgb.color_ramp.hue_interpolation = 'near'

    dilate.distance = -1
    dilate_ao.distance = -1

    val2Rgb.color_ramp.elements[1].color = (1, 1, 1, 1)
    val2Rgb.color_ramp.elements[0].color = (0.279524, 0.279524, 0.279524, 1)
    val2Rgb.color_ramp.elements[1].position = 0.08
    val2Rgb.color_ramp.elements[1].position = 0.0

    #rgb.outputs[0].default_value = (1, 1, 1, 1)

    setAlphaLineWth = gn.new("CompositorNodeSetAlpha")
    alphaLiheWith = gn.new("CompositorNodeAlphaOver")
    setAlphaLineWth.inputs[0].default_value = (1, 1, 1, 1)

    gl.new(input_node.outputs[1], setAlphaLineWth.inputs[1])
    gl.new(input_node.outputs[2], alphaLiheWith.inputs[2])
    gl.new(setAlphaLineWth.outputs[0], alphaLiheWith.inputs[1])
    gl.new(alphaLiheWith.outputs[0], output_node.inputs[4])

    return g_line

def createAlphaOverLineartGroup():
    # nodes

    g = bpy.data.node_groups
    g_alphaline = g.new("base", "CompositorNodeTree")
    gn = g_alphaline.nodes
    gl = g_alphaline.links

    g_alphaline.inputs.new("NodeSocketColor", "lineart")
    g_alphaline.inputs.new("NodeSocketColor", "lineart2")
    g_alphaline.inputs.new("NodeSocketColor", "gray")
    g_alphaline.inputs.new("NodeSocketColor", "gray2")

    input_node = g_alphaline.nodes.new("NodeGroupInput")
    input_node.location = (0, 0)

    g_alphaline.outputs.new("NodeSocketColor", "lineart")
    g_alphaline.outputs.new("NodeSocketColor", "gray")

    output_node = g_alphaline.nodes.new("NodeGroupOutput")
    output_node.location = (1000,0)

    alphaOver = gn.new("CompositorNodeAlphaOver")
    alphaOver.location = (600,100)

    gl.new(input_node.outputs["lineart"], alphaOver.inputs[2])
    gl.new(input_node.outputs["lineart2"], alphaOver.inputs[1])
    gl.new(alphaOver.outputs[0], output_node.inputs["lineart"])

    alphaOverGray = gn.new("CompositorNodeAlphaOver")
    alphaOverGray.location = (600, -200)
    gl.new(input_node.outputs["gray"], alphaOverGray.inputs[1])
    gl.new(input_node.outputs["gray2"], alphaOverGray.inputs[2])
    gl.new(output_node.inputs["gray"], alphaOverGray.outputs[0])

    return g_alphaline


def createBaseGroup():
    "make base render by using pass index"
    # pass index 1 to 10%, 2 to 20%, ...
    idMaskList = {1: 1, 2: 2, 3: 3, 4: 4}

    BS_LOCATION_X = 0
    BS_LOCATION_Y = -600

    # nodes

    g = bpy.data.node_groups

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

    def createGroupOutput(pre):
        g_base.outputs.new("NodeSocketFloat", "image")
        output_node = g_base.nodes.new("NodeGroupOutput")
        output_node.location = (600 + len(idMaskList)*300, BS_LOCATION_Y + len(idMaskList) * 200 - 400)

        setAlpha = gn.new("CompositorNodeSetAlpha")
        setAlpha.location = (600 + len(idMaskList)*300, BS_LOCATION_Y + len(idMaskList) * 200 - 400)
        output_node.location = (900 + len(idMaskList)*300, BS_LOCATION_Y + len(idMaskList) * 200 - 400)

        gl.new(input_node.outputs["alpha"], setAlpha.inputs[1])
        gl.new(pre.outputs[0], setAlpha.inputs[0])
        gl.new(setAlpha.outputs[0], output_node.inputs[-1])

        return

    g_base = g.new("base", "CompositorNodeTree")
    gn = g_base.nodes
    gl = g_base.links
    g_base.inputs.new("NodeSocketFloat", "index")
    g_base.inputs.new("NodeSocketFloat", "alpha")
    input_node = g_base.nodes.new("NodeGroupInput")
    input_node.location = (0, 0)

    for i, v in idMaskList.items():
        mix = createBase(i, v)
        if i > 1:
            pre_mix = multiNode(i, pre_mix, mix)
        else:
            pre_mix = mix
    createGroupOutput(pre_mix)



    return g_base

################### misc ###########################

def renderLayerSetVisible(r, suffix=""):
    for i in range(0, 15):
        r.layers[i] = False
    if suffix == "_front":
        for i in range(0, 5):
            r.layers[i] = True
    elif suffix == "_middle":
        for i in range(5, 10):
            r.layers[i] = True
    elif suffix == "_back":
        for i in range(10, 15):
            r.layers[i] = True
    for i in range(15, 20):
        r.layers[i] = True
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


################### nodes parts ###########################

def comicLineartNode(g_line, num=0, suffix=""):
    '''make line art and shadow ,ao render'''
    s = bpy.context.scene

    BS_LOCATION_X = 0
    BS_LOCATION_Y = 0 + num * 1200

    def setFreestyle():
        # line style setting
        line_thickness = 1.1
        edge_threshold = 44

        percentage = s.render.resolution_percentage
        x = s.render.resolution_x * percentage / 100
        y = s.render.resolution_y * percentage / 100
        size = x if x >= y else y

        edge_threshold += int(size / 500) * 40
        line_thickness += int(size / 2000)

        s.render.image_settings.file_format = 'PNG'

        s.render.use_freestyle = True
        s.render.alpha_mode = 'TRANSPARENT'
        s.render.image_settings.color_mode = 'RGBA'

        s.render.use_edge_enhance = True
        s.render.edge_threshold = edge_threshold

        #s.render.layers.active.freestyle_settings.crease_angle = 1.2

        bpy.data.linestyles["LineStyle"].panel = "THICKNESS"
        bpy.data.linestyles["LineStyle"].thickness = line_thickness
        bpy.data.linestyles["LineStyle"].thickness_position = 'RELATIVE'
        bpy.data.linestyles["LineStyle"].thickness_ratio = 0

        return

    def createFreestyleRenderLayer(name="Freestyle"):
        # render layer setting
        #f = s.render.layers.active
        f = s.render.layers.new(name)
        f.name = name

        f.use_strand = False
        f.use_edge_enhance = False
        f.use_sky = False
        f.use_solid = False
        f.use_halo = False
        f.use_ztransp = False

        return f

    def createGrayRenderLayer(name="Gray"):
        r = s.render.layers.new(name)

        r.use_freestyle = False
        r.use_pass_ambient_occlusion = True
        return r

    setFreestyle()
    f = createFreestyleRenderLayer(name="Freestyle"+suffix)
    f.freestyle_settings.linesets.new('LineStyle')
    renderLayerSetVisible(f, suffix)
    r = createGrayRenderLayer(name="Gray"+suffix)
    renderLayerSetVisible(r, suffix)

    #bpy.ops.scene.new(type="LINK_OBJECTS")
    #aos = bpy.context.scene
    #aos.name = "AO"
    #w = bpy.data.worlds.new("AO")
    #w.light_settings.use_ambient_occlusion = True
    #aos.world = bpy.data.worlds["AO"]

    # nodes
    s.use_nodes = True

    n = s.node_tree.nodes
    l = s.node_tree.links
    g = bpy.data.node_groups

    composite = n["Composite"]
    composite.location = (600, -600 + BS_LOCATION_Y)
    composite.use_alpha = True

    #render = n["Render Layers"]
    render = n.new("CompositorNodeRLayers")
    render.layer = 'Gray' + suffix
    render.location = (0, 0 + BS_LOCATION_Y)

    #s.render.layers["RenderLayer"].use_pass_object_index = True

    freestyleRender = n.new("CompositorNodeRLayers")
    freestyleRender.layer = 'Freestyle'+suffix
    freestyleRender.location = (0, -400 + BS_LOCATION_Y)

    #render_ao = n.new(type="CompositorNodeRLayers")
    #render_ao.location = (0, -800 + BS_LOCATION_Y)

    #render_ao.scene = bpy.data.scenes["AO"]
    #render_ao.layer = 'Gray'+suffix

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

    #objectPassIndexList = getObjectPassIndex()
    #for i, v in enumerate(objectPassIndexList):
    #    makeNodeObIDMask(v, i)

    line_group = n.new("CompositorNodeGroup")
    line_group.location = (300, 0 + BS_LOCATION_Y)
    line_group.node_tree = g_line

    # output to image files
    import os
    lineout = n.new("CompositorNodeOutputFile")
    lineout.name = "line out"
    lineout.location = (600, 0 + BS_LOCATION_Y)
    lineout.base_path = os.path.expanduser("~/Desktop/rendering/1")
    lineout.file_slots.new("rendering_lineart"+suffix)

    grayout = n.new("CompositorNodeOutputFile")
    grayout.name = "gray out"
    grayout.location = (600, -200 + BS_LOCATION_Y)
    grayout.base_path = os.path.expanduser("~/Desktop/rendering/1")
    grayout.file_slots.new("rendering_shadow"+suffix)

    #aoout = n.new("CompositorNodeOutputFile")
    #aoout.name = "ao out"
    #aoout.location = (600, -400 + BS_LOCATION_Y)
    #aoout.base_path = os.path.expanduser("~/Desktop/rendering/1")
    #aoout.file_slots.new("rendering_ao"+suffix)

    viewer = n.new("CompositorNodeViewer")
    viewer.location = (600, 200 + BS_LOCATION_Y)

    l.new(line_group.outputs[0], lineout.inputs[-1])
    l.new(line_group.outputs[3], grayout.inputs[-1])
    #l.new(line_group.outputs[2], aoout.inputs[-1])

    l.new(render.outputs[0], line_group.inputs[0])
    l.new(render.outputs["Alpha"], line_group.inputs[1])
    l.new(freestyleRender.outputs[0], line_group.inputs[2])
    l.new(freestyleRender.outputs["Alpha"], line_group.inputs[3])

    #l.new(render_ao.outputs["AO"], line_group.inputs[4])
    #l.new(render_ao.outputs["Alpha"], line_group.inputs[5])

    l.new(line_group.outputs[1], composite.inputs[0])
    l.new(line_group.outputs[1], viewer.inputs[0])

    bpy.context.screen.scene = s
    return line_group

def baseLayerNode(num=0, name="BaseLayer", suffix=""):
    "base render node group by using pass index"

    s = bpy.context.scene

    def createBaseLayer(name="BaseLayer"):
        s = bpy.context.scene
        r = s.render.layers.new(name)
        r.use_pass_material_index = True
        return r

    BS_LOCATION_X = 0
    BS_LOCATION_Y = -600 +num*320 +3000

    # nodes
    s.use_nodes = True
    m = bpy.data.materials
    n = s.node_tree.nodes
    l = s.node_tree.links
    g = bpy.data.node_groups

    # make base node tree
    g_base = createBaseGroup()

    # render layer
    r = createBaseLayer(name)
    renderLayerSetVisible(r, suffix)
    c = n.new(type="CompositorNodeRLayers")
    c.location = (0, BS_LOCATION_Y + 2000)
    c.name = name
    c.layer = name

    base_group = n.new("CompositorNodeGroup")
    base_group.location = (300, BS_LOCATION_Y+2000)
    base_group.node_tree = g_base

    l.new(c.outputs["IndexMA"], base_group.inputs[0])
    l.new(c.outputs["Alpha"], base_group.inputs[1])

    import os
    baseout = n.new("CompositorNodeOutputFile")
    baseout.name = "base out"
    baseout.location = (600, BS_LOCATION_Y + 2000)
    baseout.base_path = os.path.expanduser("~/Desktop/rendering/1")
    baseout.file_slots.new("rendering_base"+suffix)

    l.new(base_group.outputs[1], baseout.inputs[-1])
    return base_group

################### main compositor nodes ###########################

def baseLayerNodeDivided():
    bpy.context.scene.render.alpha_mode = 'TRANSPARENT'

    BS_LOCATION_X = 1000
    BS_LOCATION_Y = -600 + 3000

    # nodes
    s = bpy.context.scene

    s.use_nodes = True
    m = bpy.data.materials
    n = s.node_tree.nodes
    l = s.node_tree.links
    g = bpy.data.node_groups

    front = baseLayerNode(num=1, name="BaseLayer_front", suffix="_front")
    middle = baseLayerNode(num=2, name="BaseLayer_middle", suffix="_middle")
    back = baseLayerNode(num=3, name="BaseLayer_back", suffix="_back")

    y = 0
    before = None
    alpha = n.new("CompositorNodeAlphaOver")
    alpha.location = (300 + BS_LOCATION_X, y + BS_LOCATION_Y+ 300)
    l.new(alpha.inputs[1], middle.outputs[1])
    l.new(front.outputs[1], alpha.inputs[2])

    alpha2 = n.new("CompositorNodeAlphaOver")
    alpha2.location = (BS_LOCATION_X + 600, y + BS_LOCATION_Y + 600)
    l.new(back.outputs[1], alpha2.inputs[1])
    l.new(alpha2.inputs[2], alpha.outputs[0])


    output = n.new("CompositorNodeComposite")
    output.location = (900 + BS_LOCATION_X, y + BS_LOCATION_Y + 600)
    l.new(alpha2.outputs[0], output.inputs[0])

    import os
    baseout = n.new("CompositorNodeOutputFile")
    baseout.name = "base out"
    baseout.location = (1200 + BS_LOCATION_X, BS_LOCATION_Y + 1000)
    baseout.base_path = os.path.expanduser("~/Desktop/rendering/1")
    baseout.file_slots.new("rendering_base")

    l.new(alpha2.outputs[0], baseout.inputs[-1])

    return


def comicLineartNodeDivided():
    g_line = createLineartGroup()
    front = comicLineartNode(g_line, num=1, suffix="_front")
    middle = comicLineartNode(g_line, num=2, suffix="_middle")
    back = comicLineartNode(g_line, num=3, suffix="_back")

    BS_LOCATION_X = 1000
    BS_LOCATION_Y = -600 + 2000

    # nodes
    s = bpy.context.scene

    s.use_nodes = True
    m = bpy.data.materials
    n = s.node_tree.nodes
    l = s.node_tree.links
    g = bpy.data.node_groups

    g_alphaline = createAlphaOverLineartGroup()
    #base_group = n.new("CompositorNodeGroup")
    #base_group.node_tree = g_alphaline

    y = 0
    before = None
    alpha = n.new("CompositorNodeGroup")
    alpha.node_tree = g_alphaline
    alpha.location = (300 + BS_LOCATION_X, y + BS_LOCATION_Y+ 300)
    l.new(middle.outputs[3], alpha.inputs[2])
    l.new(front.outputs[3], alpha.inputs[3])
    l.new(front.outputs[4], alpha.inputs[0])
    l.new(middle.outputs[4], alpha.inputs[1])

    alpha2 = n.new("CompositorNodeGroup")
    alpha2.node_tree = g_alphaline
    alpha2.location = (BS_LOCATION_X + 600, y + BS_LOCATION_Y + 600)
    l.new(alpha.outputs[1], alpha2.inputs[3])
    l.new(back.outputs[4], alpha2.inputs[1])
    l.new(back.outputs[3], alpha2.inputs[2])
    l.new(alpha.outputs[0], alpha2.inputs[0])

    output = n.new("CompositorNodeComposite")
    output.location = (900 + BS_LOCATION_X, y + BS_LOCATION_Y + 400)
    l.new(alpha2.outputs[1], output.inputs[0])

    # output to image files
    import os
    lineout = n.new("CompositorNodeOutputFile")
    lineout.name = "line out"
    lineout.location = (900 + BS_LOCATION_X, BS_LOCATION_Y + 700)
    lineout.base_path = os.path.expanduser("~/Desktop/rendering/1")
    lineout.file_slots.new("rendering_lineart")
    l.new(alpha2.outputs[0], lineout.inputs[-1])

    grayout = n.new("CompositorNodeOutputFile")
    grayout.name = "base out"
    grayout.location = (900 + BS_LOCATION_X, BS_LOCATION_Y + 1000)
    grayout.base_path = os.path.expanduser("~/Desktop/rendering/1")
    grayout.file_slots.new("rendering_shadow")
    l.new(alpha2.outputs[1], grayout.inputs[-1])

    viewer = n.new("CompositorNodeViewer")
    viewer.location = (900+ BS_LOCATION_X, BS_LOCATION_Y)
    l.new(alpha2.outputs[1], viewer.inputs[0])

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
        comicLineartNodeDivided()
        baseLayerNodeDivided()
        #objectJoin()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ComicLineartNode)


def unregister():
    bpy.utils.unregister_class(ComicLineartNode)


if __name__ == "__main__":
    register()

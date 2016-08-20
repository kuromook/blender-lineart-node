# this script makes convert setting to monochrome lineart for comics
# use for Blender Render (no support cycles Render )

#Copyright (c) 2014 Shunnich Fujiwara
#Released under the MIT license
#http://opensource.org/licenses/mit-license.php

import bpy

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
    setAlphaMerge.location = (700, -200)

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
    alphaOver.use_premultiply = True

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


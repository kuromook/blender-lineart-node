import bpy

def baseLayer():
    s = bpy.context.scene
    r= s.render.layers.new( "BaseLayer")

    BS_LOCATION_X = 0
    BS_LOCATION_Y = 3000

    s.render.layers["BaseLayer"].use_pass_material_index = True

    # nodes
    s.use_nodes = True
    m = bpy.data.materials
    n = s.node_tree.nodes
    l = s.node_tree.links
    g = bpy.data.node_groups
    out = n['Composite']

    c = n.new(type="CompositorNodeRLayers")
    c.location = (0, BS_LOCATION_Y + 1000)
    c.name = "BaseLayer"
    c.layer = 'BaseLayer'

    idMaskList = [1,2,3,4]

    for i in idMaskList:
        id_mask = n.new(type='CompositorNodeIDMask')
        id_mask.index = i
        id_mask.location = (300, BS_LOCATION_Y + i*200)

        l.new(c.outputs["IndexMA"], id_mask.inputs[0])
        mix = n.new(type='CompositorNodeMixRGB')
        mix.location = (600, BS_LOCATION_Y + i*200)
        val = 1.0-i*0.1
        mix.inputs[2].default_value = (val, val, val, 1)

        l.new(id_mask.outputs[0], mix.inputs[0])

        if i == 2:
            multi = n.new(type='CompositorNodeMixRGB')
            multi.blend_type = 'MULTIPLY'
            multi.location = (300 + i*300, BS_LOCATION_Y + i*200)
            l.new(mix.outputs[0], multi.inputs[1])
            l.new(pre_mix.outputs[0], multi.inputs[2])
            pre_multi = multi

        if i > 2:
            multi = n.new(type='CompositorNodeMixRGB')
            multi.blend_type = 'MULTIPLY'
            multi.location = (300 + i*300, BS_LOCATION_Y + i*200)
            l.new(mix.outputs[0], multi.inputs[1])
            l.new(pre_multi.outputs[0], multi.inputs[2])
            pre_multi = multi

        pre_mix = mix

    out.location = (600 + len(idMaskList)*300, BS_LOCATION_Y + len(idMaskList)* 200)
    l.new(pre_multi.outputs[0],out.inputs[0])

    import os
    baseout = n.new("CompositorNodeOutputFile")
    baseout.name = "base out"
    baseout.location = (600 + len(idMaskList)*300, BS_LOCATION_Y + len(idMaskList) * 200 - 400)
    baseout.base_path = os.path.expanduser("~/Desktop/rendering/b")
    baseout.file_slots.new("rendering")
    l.new(pre_multi.outputs[0], baseout.inputs[-1])


def testMaterials():
    a = bpy.data.materials.new("a")
    b = bpy.data.materials.new("b")
    c = bpy.data.materials.new("c")
    a.pass_index = 1
    b.pass_index = 1
    c.pass_index = 1

    addMaterial(addCube("A",0,0,0),a)
    addMaterial(addCube("B",2,2,1),b)
    addMaterial(addCube("C",-2,2,1),c)
    allClearNodes()

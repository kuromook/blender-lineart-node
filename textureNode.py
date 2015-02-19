import bpy

def textureNode():
    def controlTex(flag=True):
        bpy.context.scene.render.layers["RenderLayer"].use_pass_object_index = flag

        ary = [i for i in bpy.data.objects if i.type =="MESH"]
        ary = [i for i in ary if i.pass_index != 0]
        for o in ary:
            o.active_material.use_shadeless = flag
            o.active_material.use_textures[0] = flag
        return

    controlTex()
    s = bpy.context.scene
    BS_LOCATION_Y = -2000
    # nodes
    s.use_nodes = True
    m = bpy.data.materials
    n = s.node_tree.nodes
    l = s.node_tree.links
    g = bpy.data.node_groups

    import os
    texout = n.new("CompositorNodeOutputFile")
    texout.name = "tex out"
    texout.location = (200, BS_LOCATION_Y + 600)
    texout.base_path = os.path.expanduser("~/Desktop/rendering/t")
    texout.file_slots.new("rendering")

    c = n.new(type="CompositorNodeRLayers")
    c.location = (0, BS_LOCATION_Y)
    c.layer = 'RenderLayer'

    i=1
    id_mask = n.new(type='CompositorNodeIDMask')
    id_mask.index = i
    id_mask.location = (200, BS_LOCATION_Y + i*(-200))

    setAlpha = n.new("CompositorNodeSetAlpha")
    setAlpha.location = (400, BS_LOCATION_Y + i*(-200))

    l.new(c.outputs["IndexOB"],id_mask.inputs[0])
    l.new(id_mask.outputs[0], setAlpha.inputs[1])
    l.new(c.outputs[0], setAlpha.inputs[0])

    l.new(setAlpha.outputs[0], texout.inputs[1])
    bpy.ops.render.render()

    n.remove(setAlpha)
    n.remove(id_mask)
    n.remove(texout)
    n.remove(c)
    controlTex(False)



################### add on setting section###########################
bl_info = {
    "name": "Comic Texture　Node",
    "category": "Object",
}

import bpy


class ComicTextureNode(bpy.types.Operator):
    """Texture render exporter"""
    bl_idname = "textureexport.comic"
    bl_label = "comic texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context): 
        bpy.context.scene.render.engine = 'BLENDER_RENDER'     
        textureNode()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ComicTextureNode)


def unregister():
    bpy.utils.unregister_class(ComicTextureNode)


if __name__ == "__main__":
    register()

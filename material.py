import bpy

# world setting
bpy.context.scene.world.light_settings.use_ambient_occlusion = True
bpy.context.scene.world.light_settings.samples = 16
bpy.context.scene.world.light_settings.use_falloff = True


# make material
name = "toon"
m = bpy.data.materials.new(name)

m.diffuse_shader = 'TOON'
m.diffuse_intensity = 0.4
m.diffuse_toon_size = 1.4
m.diffuse_toon_smooth = 0.04
m.specular_intensity = 0
m.emit = 0.5

# use plastic or metal
#m.specular_shader = 'TOON'

m.diffuse_shader = 'TOON'
m.diffuse_intensity = 1.0
m.diffuse_toon_size = 1.4
m.diffuse_toon_smooth = 0.0
m.specular_intensity = 0
m.emit = 0.0

m.diffuse_color = (1,1,1)

# node edit
m.use_nodes = True

n = m.node_tree.nodes
l = m.node_tree.links

material = n.new("ShaderNodeExtendedMaterial")
color_ramp = n.new("ShaderNodeValToRGB")
mix = n.new("ShaderNodeMixRGB")
mixOut = n.new("ShaderNodeMixRGB")

#material = n["Material"]
output = n["Output"]

material.material = m
output.location = (1200,400)
mix.location = (700,300)
color_ramp.location = (400,100)
material.location = (200,200)
mixOut.location = (1000,30)
mix.blend_type = "MULTIPLY"
mix.inputs[0].default_value = 1

l.new(material.outputs["Color"],mix.inputs["Color1"])
l.new(material.outputs[3], color_ramp.inputs["Fac"])
l.new(color_ramp.outputs["Color"], mix.inputs["Color2"])
l.new(mix.outputs["Color"], mixOut.inputs[0])

mixOut.inputs["Color1"].default_value = (0.2, 0.2, 0.3,1)
mixOut.inputs["Color2"].default_value= (0.5, 0.5, 0.7,1)

l.new(mixOut.outputs[0], output.inputs[0])


try:
    note = n.new("GenericNoteNode")
    note.location = (400, 600)
    note.text = "this node tree is for non photo realistic"
except RuntimeError:
    pass

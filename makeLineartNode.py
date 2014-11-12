# this script convert setting to monochrome lineart for comics
import bpy

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

rgb2Bw.location = (200, 100)
val2Rgb.location = (400, 100)
alpha.location = (900,300)
setAlpha.location = (700, 500)

l.new(render.outputs[0], rgb2Bw.inputs[0])
l.new(rgb2Bw.outputs[0], val2Rgb.inputs[0])
l.new(val2Rgb.outputs[0], setAlpha.inputs[0])
l.new(render.outputs['Alpha'], setAlpha.inputs[1])
l.new(setAlpha.outputs[0],alpha.inputs[1])

l.new(freestyleRender.outputs[0], alpha.inputs[2])
l.new(alpha.outputs[0], composite.inputs[0])


# gray setting
val2Rgb.color_ramp.interpolation = 'CONSTANT'
#val2Rgb.color_ramp.color_mode="HSV"
#val2Rgb.color_ramp.hue_interpolation = 'near'


val2Rgb.color_ramp.elements[1].color = (1, 1, 1, 1)
val2Rgb.color_ramp.elements[0].color = (0.279524, 0.279524, 0.279524, 1)
val2Rgb.color_ramp.elements[1].position=0.08
val2Rgb.color_ramp.elements[1].position=0.0

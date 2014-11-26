# this script convert setting to monochrome lineart for comics
import bpy

def comicLineartNode():
    # this script convert setting to monochrome lineart for comics
     
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


    # nodes
    s.use_nodes = True
        

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
    l.new(freestyleRender.outputs["Image"],composite.inputs["Image"])
    import os
    path = os.path.expanduser("~/Desktop/rendering/")
    bpy.data.scenes['Scene'].render.filepath = path + "line.jpg"
    bpy.ops.render.render( write_still=True ) 

# create Nodes for comic like 
def materialNodes(m,isWhite=True):
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links

    # create nodes
    material = n.new("ShaderNodeExtendedMaterial")
    color_ramp = n.new("ShaderNodeValToRGB")
    output = n.new("ShaderNodeOutput")
    mix = n.new("ShaderNodeMixRGB")
    color=n.new("ShaderNodeRGB")

    # set location
    material.location = (0,-100)
    color_ramp.location = (300,-200)
    output.location = (600,-200)
    mix.location = (400,100)
    color.location = (0,500)
    color.outputs[0].default_value = (1, 1, 1, 1)

    color_ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    color_ramp.color_ramp.elements[0].color = (0,0,0, 1)
    color_ramp.color_ramp.elements[0].position=0.2
    color_ramp.color_ramp.elements[1].position=0.0

    # TODO set color ramp by isWhite option
    # connect links
    if not isWhite:
        l.new(material.outputs["Alpha"], color_ramp.inputs["Fac"])
        l.new(color_ramp.outputs["Color"],output.inputs[0])
    else:
        l.new(color.outputs["Color"], mix.inputs[0])
        l.new(material.outputs["Alpha"], mix.inputs[1])
        l.new(mix.outputs["Color"],output.inputs[0])

    return


# clear Nodes and clear all Nodes
def clearNodes(m):
    m.use_nodes = True
    n = m.node_tree.nodes
    for i in n:
        n.remove(i)
    m.use_nodes = False

def allClearNodes():
    mats = bpy.data.materials
    for mb in mats:    
        clearNodes(mb)
    return


# make Images
def makeComicMaterials(num):
    mats = bpy.data.materials
    for i,v in enumerate(mats):
        if i is num:
            materialNodes(v,isWhite=False)
        else:
            materialNodes(v)

def saveImageFilesEachMaterials():
    s = bpy.context.scene

    s.render.image_settings.file_format = 'PNG'

    s.render.alpha_mode = 'TRANSPARENT'
    s.render.image_settings.color_mode = 'RGBA'

    import os
    mats = bpy.data.materials
    for i,v in enumerate(mats):
        makeComicMaterials(i)
        path = os.path.expanduser("~/Desktop/rendering/")
        bpy.data.scenes['Scene'].render.filepath = path  + v.name + "_image.png"
        bpy.ops.render.render( write_still=True ) 
        allClearNodes()

# add primitive cube
def addCube(name, x,y,z):
    verts = [(1.0, 1.0, -1.0),  
             (1.0, -1.0, -1.0),  
            (-1.0, -1.0, -1.0),  
            (-1.0, 1.0, -1.0),  
             (1.0, 1.0, 1.0),  
             (1.0, -1.0, 1.0),  
            (-1.0, -1.0, 1.0),  
            (-1.0, 1.0, 1.0)]  
      
    faces = [(0, 1, 2, 3),  
             (4, 7, 6, 5),  
             (0, 4, 5, 1),  
             (1, 5, 6, 2),  
             (2, 6, 7, 3),  
             (4, 0, 3, 7)]  
      
    mesh_data = bpy.data.meshes.new(name)  
    mesh_data.from_pydata(verts, [], faces)  
    cube_object = bpy.data.objects.new(name, mesh_data)
    cube_object.location = (x,y,z) 
    scene = bpy.context.scene    
    scene.objects.link(cube_object) 
    return cube_object


def addMaterial(o,m):
    o.data.materials.append(m)
    return o

def makeComicResource():
    saveImageFilesEachMaterials()
    comicLineartNode()

addMaterial(addCube("A",0,0,0),bpy.data.materials.new("a"))
addMaterial(addCube("B",2,2,1),bpy.data.materials.new("b"))
addMaterial(addCube("C",-2,2,1),bpy.data.materials.new("c"))
allClearNodes()

#mats = bpy.data.materials
#for m in mats:
#    materialNodes(m,True)

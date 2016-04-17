def makeObjMap:
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

renderLayers = getRLayers()
y = 0
before = None
for layer in renderLayers:
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

#n.new("CompositorNodeGroup")
#g.new("new nodes", "CompositorNodeTree")
